
// Script para arreglar mapeo de imágenes en Flutter
// Agregar a lib/services/store_service.dart

/// Arreglar mapeo de imágenes en getAllProducts
Future<List<StoreProduct>> getAllProducts() async {
  try {
    print('🔍 Obteniendo todos los productos...');
    
    if (_client == null) {
      print('⚠️ Supabase no disponible, retornando productos por defecto');
      return _getAllDefaultProducts();
    }
    
    print('🔍 Ejecutando query a store_products...');
    final response = await _client!
      .from('store_products')
      .select('*')
      .eq('is_active', true)
      .order('name');

    print('📊 Respuesta de productos: \$response');

    final products = <StoreProduct>[];
    for (final item in response) {
      try {
        print('🔄 Procesando producto: \${item['name']}');
        
        // ARREGLO: Mapear correctamente las imágenes
        String imageUrl = '';
        if (item['image_url'] != null && item['image_url'].toString().isNotEmpty) {
          imageUrl = item['image_url'].toString();
        } else if (item['images'] != null && item['images'] is List && item['images'].isNotEmpty) {
          imageUrl = item['images'][0].toString();
        }
        
        // Crear producto con imagen corregida
        final product = StoreProduct(
          id: item['id']?.toString() ?? '',
          name: item['name'] ?? '',
          description: item['description'] ?? '',
          price: (item['price'] ?? 0.0).toDouble(),
          imageUrl: imageUrl, // Usar imagen corregida
          categoryId: item['category'] ?? item['category_id'] ?? '',
          unit: item['unit'] ?? 'unidad',
          weight: (item['weight'] ?? 0.0).toDouble(),
          isAvailable: item['is_active'] ?? true,
          stock: item['stock'] ?? 0,
          availableProvinces: List<String>.from(item['available_provinces'] ?? []),
          deliveryMethod: 'express',
          createdAt: item['created_at'] != null ? DateTime.parse(item['created_at']) : null,
        );
        
        products.add(product);
        print('✅ Producto procesado: \${product.name} - Imagen: \${product.imageUrl}');
        
      } catch (e) {
        print('⚠️ Error parsing product: \$e');
      }
    }

    print('✅ \${products.length} productos obtenidos');
    return products;
  } catch (e) {
    print('❌ Error obteniendo productos: \$e');
    print('📋 Usando productos por defecto como fallback');
    return _getAllDefaultProducts();
  }
}
