import 'package:flutter/material.dart';
import 'package:cubalink23/services/cart_service.dart';
import 'package:cubalink23/services/favorites_service.dart';
import 'package:cubalink23/models/cart_item.dart';
import 'package:cubalink23/screens/shopping/shipping_screen.dart';
import 'package:cubalink23/screens/shopping/favorites_screen.dart';
import 'package:cubalink23/services/auth_guard_service.dart';
import 'package:cubalink23/widgets/vendor_logo.dart';
import 'package:cubalink23/widgets/weight_shipping_display.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({Key? key}) : super(key: key);

  @override
  _CartScreenState createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  final CartService _cartService = CartService();
  final FavoritesService _favoritesService = FavoritesService.instance;

  @override
  void initState() {
    super.initState();
    _cartService.addListener(_onCartChanged);
    _checkAuthAndLoadCart();
  }

  /// Obtener peso en libras del item del carrito
  double _getWeightInLb(CartItem item) {
    // Primero intentar usar weightLb si está disponible (más preciso)
    if (item.weightLb != null) {
      return item.weightLb as double;
    }
    
    // Fallback al peso original
    if (item.weight is double) {
      // Asumir que ya está en libras si es double
      return item.weight as double;
    } else if (item.weight is String) {
      // Intentar parsear el peso desde string
      final weightStr = item.weight.toString().toLowerCase();
      final weightRegex = RegExp(r'(\d+(?:\.\d+)?)');
      final match = weightRegex.firstMatch(weightStr);
      
      if (match != null) {
        final value = double.tryParse(match.group(1)!) ?? 1.1;
        
        if (weightStr.contains('lb') || weightStr.contains('pound')) {
          return value; // Ya está en libras
        } else if (weightStr.contains('kg')) {
          return value * 2.20462; // Convert kg to lbs
        } else if (weightStr.contains('oz') || weightStr.contains('ounce')) {
          return value * 0.0625; // Convert oz to lbs
        } else if (weightStr.contains('g') && !weightStr.contains('kg')) {
          return value * 0.00220462; // Convert g to lbs
        }
      }
    }
    return 1.1; // Default weight en libras
  }

  /// Verificar si es un vendedor externo (Amazon, Walmart, etc.)
  bool _isExternalVendor(String? vendorId) {
    if (vendorId == null) return false;
    return ['amazon', 'walmart', 'ebay', 'homedepot', 'shein'].contains(vendorId.toLowerCase());
  }

  /// Construir widget de peso para productos de la tienda (solo peso, sin envío)
  Widget _buildStoreProductWeight(CartItem item) {
    final weightLb = _getWeightInLb(item);
    
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.fitness_center,
            size: 14,
            color: Colors.grey[600],
          ),
          SizedBox(width: 4),
          Text(
            '${weightLb.toStringAsFixed(1)} lb',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: Colors.grey[700],
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _checkAuthAndLoadCart() async {
    final hasAuth = await AuthGuardService.instance.requireAuth(context, serviceName: 'el Carrito de Compras');
    if (hasAuth) {
      _cartService.loadFromSupabase();
    } else {
      // Si no está autenticado, volver atrás
      Navigator.pop(context);
    }
  }

  @override
  void dispose() {
    _cartService.removeListener(_onCartChanged);
    super.dispose();
  }

  void _onCartChanged() {
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        backgroundColor: Color(0xFF232F3E),
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Carrito de Compras',
          style: TextStyle(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          if (_cartService.items.isNotEmpty)
            IconButton(
              icon: Icon(Icons.delete_outline, color: Colors.white),
              onPressed: _showClearCartDialog,
            ),
        ],
      ),
      body: _cartService.isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(
                    valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFFF9900)),
                  ),
                  SizedBox(height: 16),
                  Text(
                    'Cargando carrito...',
                    style: TextStyle(
                      fontSize: 16,
                      color: Color(0xFF232F3E),
                    ),
                  ),
                ],
              ),
            )
          : _buildCartContent(),
      bottomNavigationBar: _cartService.items.isNotEmpty
          ? _buildCheckoutButton()
          : null,
    );
  }

  Widget _buildEmptyCart() {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                color: Color(0xFFFF9900).withOpacity( 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.shopping_cart_outlined,
                size: 60,
                color: Color(0xFFFF9900),
              ),
            ),
            SizedBox(height: 24),
            Text(
              'Tu carrito está vacío',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Color(0xFF232F3E),
              ),
            ),
            SizedBox(height: 12),
            Text(
              'Agrega productos desde nuestras tiendas',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 32),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFFF9900),
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Text(
                'Continuar Comprando',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyCartContent() {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: Color(0xFFFF9900).withOpacity( 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.shopping_cart_outlined,
                size: 40,
                color: Color(0xFFFF9900),
              ),
            ),
            SizedBox(height: 16),
            Text(
              'Tu carrito está vacío',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Color(0xFF232F3E),
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Agrega productos desde nuestras tiendas',
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFFF9900),
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: Text(
                'Ir a la Tienda',
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCartContent() {
    return Column(
      children: [
        // Resumen del carrito
        Container(
          margin: EdgeInsets.all(16),
          padding: EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity( 0.1),
                blurRadius: 4,
                offset: Offset(0, 2),
              ),
            ],
          ),
          child: Row(
            children: [
              Icon(Icons.shopping_cart, color: Color(0xFF232F3E)),
              SizedBox(width: 12),
              Text(
                '${_cartService.itemCount} producto${_cartService.itemCount != 1 ? 's' : ''} en tu carrito',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF232F3E),
                ),
              ),
            ],
          ),
        ),
        
        // Lista de productos o estado vacío
        Expanded(
          child: _cartService.items.isEmpty
              ? _buildEmptyCartContent()
              : ListView.builder(
                  padding: EdgeInsets.symmetric(horizontal: 16),
                  itemCount: _cartService.items.length,
                  itemBuilder: (context, index) {
                    final item = _cartService.items[index];
                    return _buildCartItem(item);
                  },
                ),
        ),
        
        // Resumen de precios (solo si hay productos)
        if (_cartService.items.isNotEmpty) _buildPriceSummary(),
        
        // Sección de favoritos (siempre visible)
        _buildFavoritesSection(),
      ],
    );
  }

  Widget _buildCartItem(CartItem item) {
    return Container(
      margin: EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity( 0.1),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Imagen del producto
            Stack(
              children: [
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.grey[200]!),
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: item.imageUrl.isNotEmpty
                        ? Image.network(
                            item.imageUrl,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return Icon(
                                item.type == 'recharge' ? Icons.phone : Icons.image,
                                color: Colors.grey[400],
                                size: 32,
                              );
                            },
                          )
                        : Icon(
                            item.type == 'recharge' ? Icons.phone : Icons.image,
                            color: Colors.grey[400],
                            size: 32,
                          ),
                  ),
                ),
                // Logo del vendedor
                if (item.vendorId != null && item.vendorId!.isNotEmpty)
                  Positioned(
                    top: 0,
                    left: 0,
                    child: CartVendorLogo(
                      vendorId: item.vendorId,
                      size: 18.0,
                    ),
                  ),
              ],
            ),
            SizedBox(width: 16),
            
            // Información del producto
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item.name,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF232F3E),
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  if (item.description != null) ...[
                    SizedBox(height: 4),
                    Text(
                      item.description!,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                  
                  // Weight and shipping information (solo para productos de Amazon/Walmart)
                  if (item.weight != null && _isExternalVendor(item.vendorId))
                    Padding(
                      padding: EdgeInsets.only(top: 4),
                      child: WeightShippingDisplay(
                        weightLb: _getWeightInLb(item),
                        originalWeight: item.weight.toString(),
                        destination: 'cuba',
                        vendorId: item.vendorId,
                        showShippingCost: true,
                      ),
                    ),
                  
                  // Solo mostrar peso para productos de la tienda (sin envío)
                  if (item.weight != null && !_isExternalVendor(item.vendorId))
                    Padding(
                      padding: EdgeInsets.only(top: 4),
                      child: _buildStoreProductWeight(item),
                    ),
                  
                  SizedBox(height: 8),
                  
                  // Precio y controles
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        '\$${item.price.toStringAsFixed(2)}',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFB12704),
                        ),
                      ),
                      _buildQuantityControls(item),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuantityControls(CartItem item) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey[300]!),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildQuantityButton(
            icon: Icons.remove,
            onPressed: () => _updateQuantity(item, item.quantity - 1),
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Text(
              '${item.quantity}',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w500,
                color: Color(0xFF232F3E),
              ),
            ),
          ),
          _buildQuantityButton(
            icon: Icons.add,
            onPressed: () => _updateQuantity(item, item.quantity + 1),
          ),
        ],
      ),
    );
  }

  Widget _buildQuantityButton({required IconData icon, required VoidCallback onPressed}) {
    return InkWell(
      onTap: onPressed,
      borderRadius: BorderRadius.circular(6),
      child: Container(
        padding: EdgeInsets.all(8),
        child: Icon(
          icon,
          size: 16,
          color: Color(0xFF232F3E),
        ),
      ),
    );
  }

  Widget _buildPriceSummary() {
    double subtotal = _cartService.subtotal;
    
    return Container(
      margin: EdgeInsets.all(16),
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Resumen del pedido',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Color(0xFF232F3E),
            ),
          ),
          SizedBox(height: 16),
          
          _buildPriceRow('Subtotal', subtotal),
          
          Divider(height: 24, color: Colors.grey[300]),
          
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Total',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF232F3E),
                ),
              ),
              Text(
                '\$${subtotal.toStringAsFixed(2)}',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFB12704),
                ),
              ),
            ],
          ),
          
          SizedBox(height: 12),
          Container(
            padding: EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.blue[50],
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.blue[200]!),
            ),
            child: Row(
              children: [
                Icon(Icons.info_outline, color: Colors.blue[600], size: 16),
                SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'El costo de envío se calculará en la siguiente pantalla según el método seleccionado.',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.blue[700],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPriceRow(String label, double amount, {String? subtitle}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey[700],
              ),
            ),
            Text(
              '\$${amount.toStringAsFixed(2)}',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w500,
                color: Color(0xFF232F3E),
              ),
            ),
          ],
        ),
        if (subtitle != null) ...[
          SizedBox(height: 2),
          Text(
            subtitle,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey[500],
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildCheckoutButton() {
    return Container(
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity( 0.1),
            blurRadius: 10,
            offset: Offset(0, -5),
          ),
        ],
      ),
      child: SafeArea(
        child: SizedBox(
          width: double.infinity,
          height: 50,
          child: ElevatedButton(
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => ShippingScreen(),
                ),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Color(0xFFFF9900),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              elevation: 0,
            ),
            child: Text(
              'Proceder al Envío - \$${_cartService.subtotal.toStringAsFixed(2)}',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _updateQuantity(CartItem item, int newQuantity) {
    if (newQuantity <= 0) {
      _showRemoveItemDialog(item);
    } else {
      _cartService.updateQuantity(item.id, item.type, newQuantity);
    }
  }

  void _showRemoveItemDialog(CartItem item) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Eliminar producto'),
        content: Text('¿Estás seguro que deseas eliminar "${item.name}" del carrito?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              _cartService.removeItem(item.id, item.type);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: Text('Eliminar'),
          ),
        ],
      ),
    );
  }

  void _showClearCartDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Vaciar carrito'),
        content: Text('¿Estás seguro que deseas eliminar todos los productos del carrito?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              _cartService.clearCart();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: Text('Vaciar'),
          ),
        ],
      ),
    );
  }

  Widget _buildFavoritesSection() {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: _getRecentFavorites(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Container(
            height: 60,
            child: Center(
              child: CircularProgressIndicator(
                color: Color(0xFF232F3E),
                strokeWidth: 2,
              ),
            ),
          );
        }

        final favorites = snapshot.data ?? [];
        if (favorites.isEmpty) {
          return SizedBox.shrink();
        }

        return Container(
          margin: EdgeInsets.all(16),
          padding: EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.1),
                blurRadius: 4,
                offset: Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(Icons.favorite, color: Colors.red, size: 20),
                      SizedBox(width: 8),
                      Text(
                        'Productos Favoritos',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF232F3E),
                        ),
                      ),
                    ],
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => FavoritesScreen(),
                        ),
                      );
                    },
                    child: Text('Ver todos'),
                  ),
                ],
              ),
              SizedBox(height: 12),
              SizedBox(
                height: 120,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: favorites.take(5).length,
                  itemBuilder: (context, index) {
                    final favorite = favorites[index];
                    return _buildFavoriteItem(favorite);
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildFavoriteItem(Map<String, dynamic> favorite) {
    return Container(
      width: 100,
      margin: EdgeInsets.only(right: 12),
      child: Column(
        children: [
          // Product image
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Container(
              width: 80,
              height: 60,
              color: Colors.grey[200],
              child: favorite['imageUrl'] != null && favorite['imageUrl'].isNotEmpty
                  ? Image.network(
                      favorite['imageUrl'],
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) =>
                          Icon(Icons.image_not_supported, color: Colors.grey[400]),
                    )
                  : Icon(Icons.image_not_supported, color: Colors.grey[400]),
            ),
          ),
          SizedBox(height: 4),
          // Product name
          Text(
            favorite['name'] ?? 'Producto',
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.w500,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 2),
          // Price
          Text(
            '\$${favorite['price']?.toStringAsFixed(2) ?? '0.00'}',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              color: Color(0xFF232F3E),
            ),
          ),
          // Add to cart button
          SizedBox(height: 4),
          GestureDetector(
            onTap: () => _addFavoriteToCart(favorite),
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: Color(0xFF232F3E),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                Icons.add_shopping_cart,
                color: Colors.white,
                size: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<List<Map<String, dynamic>>> _getRecentFavorites() async {
    await _favoritesService.initialize();
    return _favoritesService.getRecentFavorites(limit: 5);
  }

  void _addFavoriteToCart(Map<String, dynamic> favorite) {
    final cartItem = {
      'id': favorite['id'],
      'title': favorite['name'],
      'price': favorite['price'],
      'imageUrl': favorite['imageUrl'],
      'store': favorite['store'],
      'brand': favorite['brand'],
      'quantity': 1,
    };

    _cartService.addAmazonProduct(cartItem);

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.check_circle, color: Colors.white),
            SizedBox(width: 8),
            Expanded(
              child: Text('${favorite['name']} agregado al carrito'),
            ),
          ],
        ),
        backgroundColor: Colors.green,
        duration: Duration(seconds: 2),
      ),
    );
  }
}