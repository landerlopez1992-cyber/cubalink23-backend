import 'package:flutter/foundation.dart';
import 'package:cubalink23/models/cart_item.dart';
import 'package:cubalink23/models/amazon_product.dart';
import 'package:cubalink23/supabase/supabase_config.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class CartService extends ChangeNotifier {
  static final CartService _instance = CartService._internal();
  factory CartService() => _instance;
  CartService._internal();

  final List<CartItem> _items = [];
  bool _isLoading = false;

  List<CartItem> get items => List.unmodifiable(_items);
  bool get isLoading => _isLoading;
  int get itemCount => _items.fold(0, (total, item) => total + item.quantity);
  double get subtotal => _items.fold(0, (total, item) => total + item.totalPrice);

  /// ARREGLO: Inicializar carrito automáticamente
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

  // ✅ CÁLCULO DE ENVÍO USANDO PESO REAL DE API - FÓRMULA: peso × $5.50 + $10
  double calculateShipping() {
    double totalWeight = _items.fold(0, (total, item) {
      double itemWeight = _getItemWeight(item);
      return total + (itemWeight * item.quantity);
    });
    
    print('📦 Calculando envío para peso total: ${totalWeight.toStringAsFixed(3)} kg');
    
    // FÓRMULA EXACTA: peso × $5.50 por kg + $10 de comisión base
    double shippingCost = (totalWeight * 5.50) + 10.0;
    
    print('💰 Costo de envío calculado: \$${shippingCost.toStringAsFixed(2)} (${totalWeight.toStringAsFixed(3)} kg × \$5.50 + \$10)');
    
    return shippingCost;
  }

  /// Obtener peso del item, usando peso real de la API o estimado
  double _getItemWeight(CartItem item) {
    // 1. PRIORIDAD: Usar peso real extraído de la API de Amazon
    if (item.weight != null) {
      // Verificar si el peso viene en formato "X.XXX kg" y extraer el número
      if (item.weight is String) {
        String weightStr = item.weight.toString();
        if (weightStr.contains('PESO_NO_DISPONIBLE')) {
          print('⚠️ Producto sin peso disponible: ${item.name}');
          return _getEstimatedWeight(item);
        }
        
        // Extraer número del peso en formato "X.XXX kg"
        RegExp numberPattern = RegExp(r'([0-9]+\.?[0-9]*)');
        RegExpMatch? match = numberPattern.firstMatch(weightStr);
        if (match != null) {
          double? parsedWeight = double.tryParse(match.group(1) ?? '0');
          if (parsedWeight != null && parsedWeight > 0) {
            print('✅ Usando peso real de API: ${parsedWeight.toStringAsFixed(3)} kg para ${item.name}');
            return parsedWeight;
          }
        }
      } else if (item.weight is double && item.weight! > 0) {
        print('✅ Usando peso real: ${item.weight!.toStringAsFixed(3)} kg para ${item.name}');
        return item.weight!;
      }
    }
    
    // 2. FALLBACK: Usar peso estimado por categoría
    print('⚠️ Usando peso estimado para: ${item.name}');
    return _getEstimatedWeight(item);
  }
  
  // Peso estimado basado en categoría del producto - MÁS REALISTA
  double _getEstimatedWeight(CartItem item) {
    // ✅ VERIFICAR SI ES UN GENERADOR ESPECÍFICAMENTE
    String nameLower = item.name.toLowerCase();
    if (nameLower.contains('generador') || nameLower.contains('generator') || 
        nameLower.contains('westinghouse') || nameLower.contains('champion')) {
      
      // Estimar peso basado en potencia mencionada en el nombre
      if (nameLower.contains('12500') || nameLower.contains('9500')) {
        return 103.0; // Generador grande Westinghouse WGen9500
      } else if (nameLower.contains('4750') || nameLower.contains('3800')) {
        return 58.0; // Generador mediano Champion
      } else if (nameLower.contains('4500') || nameLower.contains('3600')) {
        return 48.0; // Generador inversor Westinghouse iGen4500
      } else {
        return 45.0; // Generador promedio
      }
    }
    
    // ✅ PESOS ESTIMADOS POR CATEGORÍA MÁS PRECISOS
    switch (item.category?.toLowerCase()) {
      case 'electronics':
      case 'electrónicos':
        // Teléfonos: 0.2kg, Tablets: 0.5kg, Auriculares: 0.3kg
        if (nameLower.contains('iphone') || nameLower.contains('samsung') || nameLower.contains('pixel')) {
          return 0.22; // Peso promedio smartphone
        } else if (nameLower.contains('ipad') || nameLower.contains('tablet')) {
          return 0.59; // Peso promedio tablet
        } else if (nameLower.contains('auricular') || nameLower.contains('headphone') || nameLower.contains('airpods')) {
          return 0.28; // Peso promedio auriculares
        }
        return 0.5; // Electrónicos en general
        
      case 'computers':
      case 'computadoras':
        // MacBooks: 1.24kg, Laptops gaming: 2.5kg, Desktops: 8kg
        if (nameLower.contains('macbook') || nameLower.contains('air')) {
          return 1.24; // MacBook Air
        } else if (nameLower.contains('gaming') || nameLower.contains('alienware')) {
          return 2.8; // Laptop gaming
        } else if (nameLower.contains('desktop') || nameLower.contains('tower')) {
          return 8.5; // Desktop PC
        }
        return 2.0; // Laptops en general
        
      case 'fashion':
      case 'moda':
        // Zapatillas: 0.8kg, Jeans: 0.6kg, Chaquetas: 0.4kg
        if (nameLower.contains('zapatilla') || nameLower.contains('nike') || nameLower.contains('adidas')) {
          return 0.8; // Zapatillas deportivas
        } else if (nameLower.contains('jean') || nameLower.contains('pantalon')) {
          return 0.6; // Jeans/pantalones
        } else if (nameLower.contains('chaqueta') || nameLower.contains('jacket')) {
          return 0.4; // Chaquetas
        }
        return 0.3; // Ropa en general
        
      case 'home & kitchen':
      case 'casa y cocina':
        // Instant Pot: 5.8kg, Licuadoras: 2.2kg, Aspiradoras: 3.1kg
        if (nameLower.contains('instant pot') || nameLower.contains('olla')) {
          return 5.8; // Instant Pot
        } else if (nameLower.contains('ninja') || nameLower.contains('licuadora')) {
          return 2.2; // Licuadoras
        } else if (nameLower.contains('dyson') || nameLower.contains('aspiradora')) {
          return 3.1; // Aspiradoras
        }
        return 1.5; // Electrodomésticos en general
        
      case 'books':
      case 'libros':
        return 0.4; // Peso promedio libro
        
      case 'sports':
      case 'deportes':
        // Apple Watch: 0.052kg, Fitbit: 0.029kg, Esterillas: 1.2kg
        if (nameLower.contains('watch') || nameLower.contains('reloj')) {
          return 0.052; // Smartwatches
        } else if (nameLower.contains('fitbit') || nameLower.contains('tracker')) {
          return 0.029; // Fitness trackers
        } else if (nameLower.contains('yoga') || nameLower.contains('esterilla')) {
          return 1.2; // Esterillas de yoga
        }
        return 0.8; // Productos deportivos en general
        
      case 'toys':
      case 'juguetes':
        // LEGO sets: 2.1kg promedio
        if (nameLower.contains('lego')) {
          return 2.1; // Sets LEGO
        }
        return 0.6; // Juguetes en general
        
      case 'beauty':
      case 'belleza':
        return 0.15; // Productos de belleza
        
      case 'tools & home improvement':
      case 'tools':
      case 'herramientas':
        // Taladros: 1.6kg, Generadores: peso variable (ya manejado arriba)
        if (nameLower.contains('taladro') || nameLower.contains('drill')) {
          return 1.6; // Taladros inalámbricos
        }
        return 2.5; // Herramientas en general
        
      case 'pet supplies':
      case 'mascotas':
        // Comida para mascotas puede ser muy pesada
        if (nameLower.contains('15kg') || nameLower.contains('15 kg')) {
          return 15.0; // Alimento de 15kg
        } else if (nameLower.contains('10kg') || nameLower.contains('10 kg')) {
          return 10.0; // Alimento de 10kg
        }
        return 1.5; // Productos para mascotas en general
        
      default:
        return 0.5; // Peso por defecto
    }
  }

  double get total => subtotal + calculateShipping();

  /// Verificar si hay productos sin peso especificado de la API
  bool hasUnknownWeights() {
    return _items.any((item) {
      // Si no hay peso, obviamente es desconocido
      if (item.weight == null) return true;
      
      // Si el peso es un string que indica no disponible
      if (item.weight is String && item.weight.toString().contains('PESO_NO_DISPONIBLE')) {
        return true;
      }
      
      // Si el peso es 0 o negativo, considerarlo desconocido
      if (item.weight is double && item.weight! <= 0) {
        return true;
      }
      
      return false; // El peso es válido
    });
  }

  void addItem(CartItem item) {
    final existingIndex = _items.indexWhere((existing) => existing.id == item.id && existing.type == item.type);
    
    if (existingIndex >= 0) {
      _items[existingIndex] = _items[existingIndex].copyWith(
        quantity: _items[existingIndex].quantity + item.quantity,
      );
    } else {
      _items.add(item);
    }
    
    notifyListeners();
    _saveToSupabase();
  }

  void addAmazonProduct(dynamic product, {int quantity = 1}) {
    // Handle both AmazonProduct objects and Map<String, dynamic>
    CartItem cartItem;
    
    if (product is AmazonProduct) {
      cartItem = CartItem(
        id: product.asin,
        name: product.title,
        price: product.price,
        imageUrl: product.mainImage,
        quantity: quantity,
        type: 'amazon',
        description: product.description,
        weight: product.weightKg,
        category: product.category,
        additionalData: {
          'asin': product.asin,
          'rating': product.rating,
          'reviewCount': product.reviewCount,
          'isAvailable': product.isAvailable,
        },
      );
    } else if (product is Map<String, dynamic>) {
      // Handle store product data from new shopping screens
      cartItem = CartItem(
        id: product['id'] ?? 'unknown',
        name: product['title'] ?? product['name'] ?? 'Unknown Product',
        price: (product['price'] ?? 0.0).toDouble(),
        imageUrl: product['imageUrl'] ?? '',
        quantity: product['quantity'] ?? quantity,
        type: product['store']?.toLowerCase() ?? 'amazon',
        description: product['description'] ?? '',
        weight: product['weight']?.toDouble(),
        category: product['category'],
        additionalData: {
          'store': product['store'] ?? 'Amazon',
          'rating': product['rating'],
        },
      );
    } else {
      throw ArgumentError('Product must be either AmazonProduct or Map<String, dynamic>');
    }
    
    addItem(cartItem);
  }

  void addRecharge(String phoneNumber, String operator, String country, double amount) {
    final cartItem = CartItem(
      id: 'recharge_${DateTime.now().millisecondsSinceEpoch}',
      name: 'Recarga $operator - $phoneNumber',
      price: amount,
      imageUrl: 'https://via.placeholder.com/100x100/2196F3/FFFFFF?text=Recarga',
      quantity: 1,
      type: 'recharge',
      description: 'Recarga telefónica a $phoneNumber',
      category: 'recharge',
      additionalData: {
        'phoneNumber': phoneNumber,
        'operator': operator,
        'country': country,
      },
    );
    
    addItem(cartItem);
  }

  void addFoodProduct(Map<String, dynamic> productData) {
    final cartItem = CartItem(
      id: productData['id'],
      name: productData['name'],
      price: productData['price'].toDouble(),
      imageUrl: productData['image'],
      quantity: productData['quantity'],
      type: 'food_product',
      description: 'Producto alimenticio - ${productData['name']}',
      category: 'food',
      weight: _getFoodProductWeight(productData['name']),
      additionalData: {
        'unit': productData['unit'],
        'productType': 'food',
      },
    );
    
    addItem(cartItem);
  }

  double _getFoodProductWeight(String productName) {
    // Pesos estimados para productos alimenticios por libra
    String nameLower = productName.toLowerCase();
    
    if (nameLower.contains('arroz') && nameLower.contains('5')) {
      return 2.27; // 5 libras = 2.27 kg
    } else if (nameLower.contains('carne') || nameLower.contains('lomo') || 
               nameLower.contains('cabeza') || nameLower.contains('patas')) {
      return 0.45; // 1 libra = 0.45 kg (precio por libra)
    }
    
    return 0.45; // Default: 1 libra
  }

  void removeItem(String id, String type) {
    _items.removeWhere((item) => item.id == id && item.type == type);
    notifyListeners();
    _saveToSupabase();
  }

  void updateQuantity(String id, String type, int quantity) {
    final index = _items.indexWhere((item) => item.id == id && item.type == type);
    if (index >= 0) {
      if (quantity <= 0) {
        _items.removeAt(index);
      } else {
        _items[index] = _items[index].copyWith(quantity: quantity);
      }
      notifyListeners();
      _saveToSupabase();
    }
  }

  void clearCart() {
    _items.clear();
    notifyListeners();
    _saveToSupabase();
  }

  /// ARREGLO: Limpiar carrito al cerrar sesión
  void clearCartOnLogout() {
    print('🚪 Limpiando carrito al cerrar sesión...');
    _items.clear();
    notifyListeners();
    // No guardamos en Supabase porque el usuario se está desconectando
    print('✅ Carrito limpiado localmente');
  }

  /// ARREGLO: Cambiar de usuario (limpiar carrito anterior y cargar nuevo)
  Future<void> switchUser() async {
    print('🔄 Cambiando de usuario...');
    
    // Primero limpiar carrito actual
    _items.clear();
    notifyListeners();
    
    // Luego cargar carrito del nuevo usuario
    await initializeCart();
    
    print('✅ Cambio de usuario completado');
  }

  Future<void> _saveToSupabase() async {
    try {
      final client = SupabaseConfig.client;
      final user = client.auth.currentUser;
      if (user != null) {
        // ARREGLO: Usar cart_items en lugar de user_carts
        // Primero limpiar carrito existente
        await client
            .from('cart_items')
            .delete()
            .eq('user_id', user.id);
        
        // Luego insertar todos los items
        if (_items.isNotEmpty) {
          final itemsData = _items.map((item) => {
            'user_id': user.id,
            'product_id': item.id,
            'product_name': item.name,
            'product_price': item.price,
            'product_image_url': item.imageUrl,
            'product_type': item.type,
            'quantity': item.quantity,
            'weight': item.weight,
          }).toList();
          
          await client
              .from('cart_items')
              .insert(itemsData);
        }
        
        print('✅ Carrito guardado en cart_items: ${_items.length} items');
      }
    } catch (e) {
      print('❌ Error saving cart to Supabase: $e');
    }
  }

  Future<void> loadFromSupabase() async {
    try {
      _isLoading = true;
      notifyListeners();
      
      final client = SupabaseConfig.client;
      final user = client.auth.currentUser;
      if (user != null) {
        print('📦 Cargando carrito para usuario: ${user.id}');
        
        // ARREGLO: Cargar desde cart_items en lugar de user_carts
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
      } else {
        print('⚠️ Usuario no autenticado, carrito vacío');
        _items.clear();
      }
    } catch (e) {
      print('❌ Error loading cart from Supabase: $e');
      _items.clear();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}