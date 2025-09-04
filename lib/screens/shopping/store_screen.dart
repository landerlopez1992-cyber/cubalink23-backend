import 'package:flutter/material.dart';
import 'package:cubalink23/models/product_category.dart';
import 'package:cubalink23/models/store_product.dart';
import 'package:cubalink23/services/store_service.dart';
import 'package:cubalink23/services/cart_service.dart';
import 'package:cubalink23/screens/shopping/store_category_screen.dart';
import 'package:cubalink23/screens/shopping/product_details_screen.dart';

class StoreScreen extends StatefulWidget {
  @override
  _StoreScreenState createState() => _StoreScreenState();
}

class _StoreScreenState extends State<StoreScreen> {
  final StoreService _storeService = StoreService();
  final CartService _cartService = CartService();
  
  List<ProductCategory> _realCategories = [];
  List<StoreProduct> _realProducts = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initializeStore();
  }

  Future<void> _initializeStore() async {
    try {
      print('🏪 Inicializando tienda...');
      
      // Initialize store service with default categories
      await _storeService.initializeDefaultCategories();
      
      // Load real categories and products from Supabase
      print('📋 Cargando categorías...');
      final categories = await _storeService.getCategories();
      print('✅ Categorías cargadas: ${categories.length}');
      
      print('📦 Cargando productos...');
      final products = await _storeService.getAllProducts();
      print('✅ Productos cargados: ${products.length}');
      
      if (mounted) {
        print('🔄 Actualizando estado de la UI...');
        setState(() {
          _realCategories = categories;
          _realProducts = products;
          _isLoading = false;
        });
        print('🎉 Tienda inicializada correctamente');
        print('📊 Estado final - Categories: ${_realCategories.length}, Products: ${_realProducts.length}, Loading: $_isLoading');
      } else {
        print('⚠️ Widget no está montado, no se puede actualizar el estado');
      }
    } catch (e) {
      print('❌ Error inicializando tienda: $e');
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _addToCart(StoreProduct product) {
    final cartItem = {
      'id': 'store_${product.id}',
      'name': product.name,
      'price': product.price,
      'image': product.imageUrl,
      'type': 'store_product',
      'unit': product.unit,
      'quantity': 1,
    };

    _cartService.addFoodProduct(cartItem);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${product.name} añadido al carrito'),
        duration: Duration(seconds: 2),
        backgroundColor: Theme.of(context).colorScheme.primary,
        action: SnackBarAction(
          label: 'Ver Carrito',
          textColor: Colors.white,
          onPressed: () {
            Navigator.pushNamed(context, '/cart');
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    print('🏗️ StoreScreen build() llamado - isLoading: $_isLoading, categories: ${_realCategories.length}, products: ${_realProducts.length}');
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.primary,
        elevation: 0,
        title: Text(
          'Tienda',
          style: TextStyle(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
        iconTheme: IconThemeData(color: Colors.white),
        actions: [
          IconButton(
            onPressed: () {
              Navigator.pushNamed(context, '/cart');
            },
            icon: Stack(
              children: [
                Icon(Icons.shopping_cart, color: Colors.white, size: 26),
                if (_cartService.itemCount > 0)
                  Positioned(
                    right: 0,
                    top: 0,
                    child: Container(
                      padding: EdgeInsets.all(4),
                      decoration: BoxDecoration(
                        color: Colors.orange,
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white, width: 1),
                      ),
                      constraints: BoxConstraints(minWidth: 16, minHeight: 16),
                      child: Text(
                        _cartService.itemCount > 9 ? '9+' : _cartService.itemCount.toString(),
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
      body: _isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Cargando tienda...'),
                ],
              ),
            )
          : _realCategories.isEmpty && _realProducts.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error_outline, size: 64, color: Colors.grey),
                      SizedBox(height: 16),
                      Text('No se pudieron cargar los datos'),
                      SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: _initializeStore,
                        child: Text('Reintentar'),
                      ),
                    ],
                  ),
                )
              : SingleChildScrollView(
                  physics: BouncingScrollPhysics(),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Banner informativo
                      _buildInfoBanner(),
                      
                      // Categorías
                      _buildCategoriesSection(),
                      
                      // Productos destacados
                      _buildFeaturedProductsSection(),
                      
                      SizedBox(height: 20),
                    ],
                  ),
                ),
    );
  }

  Widget _buildInfoBanner() {
    return Container(
      margin: EdgeInsets.all(16),
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Colors.green.shade600,
            Colors.green.shade400,
          ],
        ),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.green.withOpacity( 0.3),
            blurRadius: 8,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.local_shipping, color: Colors.white, size: 24),
              SizedBox(width: 8),
              Text(
                'Entrega Rápida',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          Text(
            '📦 Entrega Express: Pinar del Río hasta Camagüey\\n🚢 Entrega por Barco: Todas las provincias',
            style: TextStyle(
              color: Colors.white.withOpacity( 0.9),
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoriesSection() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.category, color: Theme.of(context).colorScheme.primary, size: 24),
              SizedBox(width: 8),
              Text(
                'Categorías',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
            ],
          ),
          SizedBox(height: 16),
          GridView.builder(
            shrinkWrap: true,
            physics: NeverScrollableScrollPhysics(),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              childAspectRatio: 1.2,
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
            ),
            itemCount: _realCategories.length,
            itemBuilder: (context, index) {
              final category = _realCategories[index];
              return _buildCategoryCard(category);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryCard(ProductCategory category) {
    final iconData = _getCategoryIcon(category.iconName);
    
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => StoreCategoryScreen(category: category),
          ),
        );
      },
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity( 0.1),
              blurRadius: 8,
              offset: Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primary.withOpacity( 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                iconData,
                size: 32,
                color: Theme.of(context).colorScheme.primary,
              ),
            ),
            SizedBox(height: 12),
            Text(
              category.name,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 4),
            Text(
              category.description,
              style: TextStyle(
                fontSize: 11,
                color: Colors.grey.shade600,
              ),
              textAlign: TextAlign.center,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeaturedProductsSection() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(height: 24),
          Row(
            children: [
              Icon(Icons.star, color: Colors.orange, size: 24),
              SizedBox(width: 8),
              Text(
                'Productos Destacados',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
            ],
          ),
          SizedBox(height: 16),
          if (_realProducts.isEmpty)
            Container(
              height: 120,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.inventory_2_outlined, size: 48, color: Colors.grey.shade400),
                    SizedBox(height: 8),
                    Text(
                      'No hay productos disponibles',
                      style: TextStyle(
                        color: Colors.grey.shade600,
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Text(
                      'Los productos aparecerán aquí cuando estén disponibles',
                      style: TextStyle(
                        color: Colors.grey.shade500,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ),
            )
          else
            Container(
              height: 220,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: _realProducts.take(10).length,
                itemBuilder: (context, index) {
                  final product = _realProducts[index];
                  return _buildRealProductCard(product);
                },
              ),
            ),
        ],
      ),
    );
  }


  Widget _buildRealProductCard(StoreProduct product) {
    return GestureDetector(
      onTap: () {
        // Convert StoreProduct to Map for compatibility with ProductDetailsScreen
        final productMap = {
          'id': product.id,
          'name': product.name,
          'description': product.description,
          'price': product.price,
          'image': product.imageUrl,
          'unit': product.unit,
          'stock': product.stock,
          'isAvailable': product.isAvailable,
          'categoryId': product.categoryId,
          'deliveryMethod': product.deliveryMethod,
          'availableProvinces': product.availableProvinces,
          'weight': product.weight,
        };
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ProductDetailsScreen(product: productMap),
          ),
        );
      },
      child: Container(
        width: 160,
        margin: EdgeInsets.only(right: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity( 0.1),
              blurRadius: 8,
              offset: Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.vertical(top: Radius.circular(12)),
                  child: Container(
                    height: 100,
                    width: double.infinity,
                    child: product.imageUrl.isNotEmpty 
                      ? Image.network(
                          product.imageUrl,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) => _buildAppLogoPlaceholder(),
                        )
                      : _buildAppLogoPlaceholder(),
                  ),
                ),
                if (!product.isAvailable)
                  Positioned(
                    top: 8,
                    left: 8,
                    child: Container(
                      padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        'AGOTADO',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
              ],
            ),
            Expanded(
              child: Padding(
                padding: EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      product.name,
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                        color: Colors.black87,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '\$${product.price.toStringAsFixed(2)}',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Theme.of(context).colorScheme.primary,
                              ),
                            ),
                            Text(
                              'por ${product.unit}',
                              style: TextStyle(
                                fontSize: 10,
                                color: Colors.grey.shade600,
                              ),
                            ),
                          ],
                        ),
                        if (product.isAvailable)
                          Container(
                            width: 32,
                            height: 32,
                            decoration: BoxDecoration(
                              color: Theme.of(context).colorScheme.primary,
                              shape: BoxShape.circle,
                            ),
                            child: IconButton(
                              padding: EdgeInsets.zero,
                              onPressed: () => _addToCart(product),
                              icon: Icon(
                                Icons.add,
                                color: Colors.white,
                                size: 18,
                              ),
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData _getCategoryIcon(String iconName) {
    print('🎨 Getting icon for: $iconName');
    switch (iconName.toLowerCase()) {
      case 'restaurant': return Icons.restaurant;
      case 'devices': return Icons.devices;
      case 'spa': return Icons.spa;
      case 'local_drink': return Icons.local_drink;
      case 'hardware': return Icons.hardware;
      case 'build': return Icons.build;
      case 'construction': return Icons.construction;
      case 'local_pharmacy': return Icons.local_pharmacy;
      case 'healing': return Icons.healing;
      case 'phone_android': return Icons.phone_android;
      case 'shopping_bag': return Icons.shopping_bag;
      case 'home': return Icons.home;
      case 'fitness_center': return Icons.fitness_center;
      case 'motorcycle': return Icons.motorcycle;
      case 'store': return Icons.store;
      case 'alimentos': return Icons.restaurant;
      case 'materiales': return Icons.construction;
      case 'ferretería': return Icons.build;
      case 'farmacia': return Icons.healing;
      case 'electrónicos': return Icons.phone_android;
      case 'ropa': return Icons.shopping_bag;
      case 'motos': return Icons.motorcycle;
      default: 
        print('⚠️ Icon not found for: $iconName, using default');
        return Icons.store;
    }
  }

  Widget _buildAppLogoPlaceholder() {
    return Container(
      color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.store,
            size: 40,
            color: Theme.of(context).colorScheme.primary,
          ),
          SizedBox(height: 4),
          Text(
            'CubaLink23',
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ],
      ),
    );
  }
}