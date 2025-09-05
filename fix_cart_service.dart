
// ARREGLO PARA CART SERVICE - lib/services/cart_service.dart

class CartService extends ChangeNotifier {
  // ... código existente ...

  /// ARREGLO: Cargar carrito automáticamente al inicializar
  Future<void> initializeCart() async {
    try {
      print('🛒 Inicializando carrito...');
      
      final client = SupabaseConfig.client;
      final user = client.auth.currentUser;
      
      if (user != null) {
        print('👤 Usuario autenticado, cargando carrito...');
        await loadFromSupabase();
      } else {
        print('⚠️ Usuario no autenticado, carrito vacío');
        _items.clear();
        notifyListeners();
      }
    } catch (e) {
      print('❌ Error inicializando carrito: $e');
      _items.clear();
      notifyListeners();
    }
  }

  /// ARREGLO: Mejorar loadFromSupabase con mejor manejo de errores
  Future<void> loadFromSupabase() async {
    try {
      _isLoading = true;
      notifyListeners();
      
      final client = SupabaseConfig.client;
      final user = client.auth.currentUser;
      
      if (user == null) {
        print('⚠️ Usuario no autenticado, no se puede cargar carrito');
        _items.clear();
        return;
      }
      
      print('📦 Cargando carrito para usuario: ${user.id}');
      
      // Intentar cargar desde user_carts primero
      final response = await client
          .from('user_carts')
          .select('items')
          .eq('user_id', user.id)
          .maybeSingle();
      
      if (response != null && response['items'] != null) {
        final itemsData = response['items'] as List<dynamic>? ?? [];
        
        _items.clear();
        _items.addAll(
          itemsData.map((itemData) => CartItem.fromJson(itemData as Map<String, dynamic>))
        );
        
        print('✅ Carrito cargado desde user_carts: ${_items.length} items');
      } else {
        // Fallback: cargar desde cart_items
        print('🔄 user_carts vacío, intentando cart_items...');
        await _loadFromCartItems();
      }
      
    } catch (e) {
      print('❌ Error cargando carrito desde Supabase: $e');
      _items.clear();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// ARREGLO: Método auxiliar para cargar desde cart_items
  Future<void> _loadFromCartItems() async {
    try {
      final client = SupabaseConfig.client;
      final user = client.auth.currentUser;
      
      if (user == null) return;
      
      final response = await client
          .from('cart_items')
          .select('*')
          .eq('user_id', user.id);
      
      _items.clear();
      _items.addAll(
        response.map((itemData) => CartItem(
          id: itemData['product_id'] ?? itemData['id'],
          name: itemData['product_name'] ?? '',
          price: (itemData['product_price'] ?? 0.0).toDouble(),
          quantity: itemData['quantity'] ?? 1,
          imageUrl: itemData['product_image_url'] ?? '',
          type: itemData['product_type'] ?? 'store',
          weight: itemData['weight'],
        ))
      );
      
      print('✅ Carrito cargado desde cart_items: ${_items.length} items');
      
      // Migrar a user_carts para futuras cargas
      await _saveToSupabase();
      
    } catch (e) {
      print('❌ Error cargando desde cart_items: $e');
    }
  }

  /// ARREGLO: Mejorar _saveToSupabase con mejor manejo de errores
  Future<void> _saveToSupabase() async {
    try {
      final client = SupabaseConfig.client;
      final user = client.auth.currentUser;
      
      if (user == null) {
        print('⚠️ Usuario no autenticado, no se puede guardar carrito');
        return;
      }
      
      print('💾 Guardando carrito para usuario: ${user.id}');
      
      await client
          .from('user_carts')
          .upsert({
            'user_id': user.id,
            'items': _items.map((item) => item.toJson()).toList(),
            'updated_at': DateTime.now().toIso8601String(),
          });
      
      print('✅ Carrito guardado exitosamente');
      
    } catch (e) {
      print('❌ Error guardando carrito: $e');
    }
  }
}
