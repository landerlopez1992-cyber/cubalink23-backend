import 'package:flutter/material.dart';
import 'package:cubalink23/models/product_category.dart';
import 'package:cubalink23/models/store_product.dart';
import 'package:cubalink23/services/store_service.dart';
import 'package:cubalink23/services/cart_service.dart';

class StoreCategoryScreen extends StatefulWidget {
  final ProductCategory? category;
  final String? categoryName;

  StoreCategoryScreen({this.category, this.categoryName});

  @override
  _StoreCategoryScreenState createState() => _StoreCategoryScreenState();
}

class _StoreCategoryScreenState extends State<StoreCategoryScreen> {
  final StoreService _storeService = StoreService();
  final CartService _cartService = CartService();
  
  List<StoreProduct> _products = [];
  List<Map<String, dynamic>> _subcategories = [];
  bool _isLoading = true;
  String _selectedProvince = 'La Habana';
  bool _showingSubcategories = true;
  String _currentCategoryName = '';

  @override
  void initState() {
    super.initState();
    _currentCategoryName = widget.categoryName ?? widget.category?.name ?? '';
    _loadSubcategoriesAndProducts();
  }

  Future<void> _loadSubcategoriesAndProducts() async {
    try {
      // Cargar subcategorías basadas en el nombre de la categoría
      await _loadSubcategories(_currentCategoryName);
      
      // Cargar algunos productos destacados de la categoría general
      await _loadFeaturedProducts(_currentCategoryName);
      
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    } catch (e) {
      print('Error cargando datos: $e');
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _loadSubcategories(String categoryName) async {
    try {
      // Cargar subcategorías reales desde Supabase
      _subcategories = await _storeService.getSubcategoriesByName(categoryName);
      print('✅ Subcategorías cargadas: ${_subcategories.length}');
    } catch (e) {
      print('❌ Error cargando subcategorías: $e');
      _subcategories = [];
    }
  }

  Future<void> _loadFeaturedProducts(String categoryName) async {
    try {
      // Cargar productos reales desde Supabase
      _products = await _storeService.getProductsByCategoryName(categoryName);
      print('✅ Productos cargados: ${_products.length}');
    } catch (e) {
      print('❌ Error cargando productos: $e');
      _products = [];
    }
  }

  void _addToCart(StoreProduct product) {
    // Verificar si se puede entregar en la provincia seleccionada
    if (!_storeService.canDeliverTo(_selectedProvince, product.deliveryMethod)) {
      _showDeliveryAlert(product);
      return;
    }

    final cartItem = {
      'id': 'store_${product.id}',
      'name': product.name,
      'price': product.price,
      'image': product.imageUrl,
      'type': 'store_product',
      'unit': product.unit,
      'quantity': 1,
      'weight': product.weight,
      'categoryId': product.categoryId,
      'deliveryProvince': _selectedProvince,
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


  void _showDeliveryAlert(StoreProduct product) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.local_shipping_outlined, color: Colors.orange),
            SizedBox(width: 8),
            Text('Entrega No Disponible'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Este producto no se puede entregar en $_selectedProvince con el método de entrega ${product.deliveryMethod}.',
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 12),
            if (product.deliveryMethod == 'express') ...[
              Text(
                'Entrega Express disponible en:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 4),
              ...StoreService.expressProvinces.map((province) => 
                Text('• $province', style: TextStyle(fontSize: 14))),
            ] else ...[
              Text(
                'Entrega por Barco disponible en todas las provincias.',
                style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green),
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Entendido'),
          ),
          if (product.deliveryMethod == 'express')
            TextButton(
              onPressed: () {
                Navigator.pop(context);
                _showProvinceSelector();
              },
              child: Text('Cambiar Provincia'),
            ),
        ],
      ),
    );
  }

  void _showProvinceSelector() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Container(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Seleccionar Provincia de Entrega',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            Container(
              height: 300,
              child: ListView.builder(
                itemCount: StoreService.allProvinces.length,
                itemBuilder: (context, index) {
                  final province = StoreService.allProvinces[index];
                  final isSelected = province == _selectedProvince;
                  final isExpressAvailable = StoreService.expressProvinces.contains(province);
                  
                  return ListTile(
                    title: Text(province),
                    subtitle: Text(
                      isExpressAvailable ? 'Express + Barco' : 'Solo Barco',
                      style: TextStyle(
                        color: isExpressAvailable ? Colors.green : Colors.orange,
                        fontSize: 12,
                      ),
                    ),
                    trailing: isSelected 
                        ? Icon(Icons.check, color: Theme.of(context).colorScheme.primary)
                        : null,
                    onTap: () {
                      setState(() {
                        _selectedProvince = province;
                      });
                      Navigator.pop(context);
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.primary,
        elevation: 0,
        title: Text(
          _currentCategoryName,
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
      body: Column(
        children: [
          // Selector de provincia
          _buildProvinceSelector(),
          
          // Contenido principal
          Expanded(
            child: _isLoading
                ? Center(child: CircularProgressIndicator())
                : _showingSubcategories
                    ? _buildSubcategoriesAndProducts()
                    : _buildProductsList(),
          ),
        ],
      ),
    );
  }

  Widget _buildProvinceSelector() {
    return Container(
      color: Theme.of(context).colorScheme.primary.withOpacity( 0.1),
      padding: EdgeInsets.all(16),
      child: Row(
        children: [
          Icon(Icons.location_on, color: Theme.of(context).colorScheme.primary),
          SizedBox(width: 8),
          Text(
            'Entregar en: ',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
          Expanded(
            child: GestureDetector(
              onTap: _showProvinceSelector,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: Theme.of(context).colorScheme.primary,
                    width: 1,
                  ),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: Text(
                        _selectedProvince,
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                    Icon(Icons.keyboard_arrow_down, size: 20),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }


  Widget _buildSubcategoriesAndProducts() {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Subcategorías
          if (_subcategories.isNotEmpty) ...[
            Text(
              'Subcategorías',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Theme.of(context).colorScheme.primary,
              ),
            ),
            SizedBox(height: 16),
            GridView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 1.3,
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
              ),
              itemCount: _subcategories.length,
              itemBuilder: (context, index) {
                final subcategory = _subcategories[index];
                return _buildSubcategoryCard(subcategory);
              },
            ),
            SizedBox(height: 24),
          ],
          
          // Productos destacados
          if (_products.isNotEmpty) ...[
            Text(
              'Productos Destacados',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Theme.of(context).colorScheme.primary,
              ),
            ),
            SizedBox(height: 16),
            ..._products.map((product) => _buildProductCard(product)),
          ],
        ],
      ),
    );
  }

  Widget _buildSubcategoryCard(Map<String, dynamic> subcategory) {
    return GestureDetector(
      onTap: () {
        // Aquí podrías navegar a una pantalla de productos específicos
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Cargando productos de ${subcategory['name']}...'),
            duration: Duration(seconds: 2),
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
                color: Color(subcategory['color']).withOpacity( 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                subcategory['icon'],
                size: 32,
                color: Color(subcategory['color']),
              ),
            ),
            SizedBox(height: 12),
            Text(
              subcategory['name'],
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProductCard(StoreProduct product) {
    final canDeliver = _storeService.canDeliverTo(_selectedProvince, product.deliveryMethod);
    
    return Container(
      margin: EdgeInsets.only(bottom: 16),
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
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Row(
          children: [
            // Imagen del producto
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Container(
                width: 80,
                height: 80,
                child: product.imageUrl.isNotEmpty 
                  ? Image.network(
                      product.imageUrl,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) => _buildAppLogoPlaceholder(),
                    )
                  : _buildAppLogoPlaceholder(),
              ),
            ),
            SizedBox(width: 16),
            
            // Información del producto
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product.name,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.black87,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  SizedBox(height: 4),
                  Text(
                    product.description,
                    style: TextStyle(
                      fontSize: 13,
                      color: Colors.grey.shade600,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  SizedBox(height: 8),
                  Row(
                    children: [
                      Text(
                        '\$${product.price.toStringAsFixed(2)}',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                      ),
                      Text(
                        ' por ${product.unit}',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey.shade600,
                        ),
                      ),
                      Spacer(),
                      if (!canDeliver)
                        Icon(
                          Icons.local_shipping_outlined,
                          color: Colors.orange,
                          size: 16,
                        ),
                    ],
                  ),
                  if (!canDeliver)
                    Padding(
                      padding: EdgeInsets.only(top: 4),
                      child: Text(
                        'No disponible en $_selectedProvince',
                        style: TextStyle(
                          fontSize: 11,
                          color: Colors.orange,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                ],
              ),
            ),
            
            // Botón agregar al carrito
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: canDeliver
                    ? Theme.of(context).colorScheme.primary
                    : Colors.grey.shade300,
                shape: BoxShape.circle,
              ),
              child: IconButton(
                padding: EdgeInsets.zero,
                onPressed: canDeliver ? () => _addToCart(product) : null,
                icon: Icon(
                  Icons.add,
                  color: canDeliver ? Colors.white : Colors.grey.shade500,
                  size: 20,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProductsList() {
    return ListView.builder(
      padding: EdgeInsets.all(16),
      itemCount: _products.length,
      itemBuilder: (context, index) {
        final product = _products[index];
        final canDeliver = _storeService.canDeliverTo(_selectedProvince, product.deliveryMethod);
        
        return Container(
          margin: EdgeInsets.only(bottom: 16),
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
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                // Imagen del producto
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    width: 80,
                    height: 80,
                    child: product.imageUrl.isNotEmpty 
                      ? Image.network(
                          product.imageUrl,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) => _buildAppLogoPlaceholder(),
                        )
                      : _buildAppLogoPlaceholder(),
                  ),
                ),
                SizedBox(width: 16),
                
                // Información del producto
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        product.name,
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: Colors.black87,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      SizedBox(height: 4),
                      Text(
                        product.description,
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.grey.shade600,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      SizedBox(height: 8),
                      Row(
                        children: [
                          Text(
                            '\$${product.price.toStringAsFixed(2)}',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Theme.of(context).colorScheme.primary,
                            ),
                          ),
                          Text(
                            ' por ${product.unit}',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey.shade600,
                            ),
                          ),
                          Spacer(),
                          if (!canDeliver)
                            Icon(
                              Icons.local_shipping_outlined,
                              color: Colors.orange,
                              size: 16,
                            ),
                        ],
                      ),
                      if (!canDeliver)
                        Padding(
                          padding: EdgeInsets.only(top: 4),
                          child: Text(
                            'No disponible en $_selectedProvince',
                            style: TextStyle(
                              fontSize: 11,
                              color: Colors.orange,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
                
                // Botón agregar al carrito
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: canDeliver
                        ? Theme.of(context).colorScheme.primary
                        : Colors.grey.shade300,
                    shape: BoxShape.circle,
                  ),
                  child: IconButton(
                    padding: EdgeInsets.zero,
                    onPressed: canDeliver ? () => _addToCart(product) : null,
                    icon: Icon(
                      Icons.add,
                      color: canDeliver ? Colors.white : Colors.grey.shade500,
                      size: 20,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildAppLogoPlaceholder() {
    return Container(
      color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.store,
            size: 32,
            color: Theme.of(context).colorScheme.primary,
          ),
          SizedBox(height: 2),
          Text(
            'CubaLink23',
            style: TextStyle(
              fontSize: 8,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ],
      ),
    );
  }
}