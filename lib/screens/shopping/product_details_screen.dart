import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:share_plus/share_plus.dart';
import 'package:cubalink23/services/cart_service.dart';
import 'package:cubalink23/services/favorites_service.dart';
import 'package:cubalink23/models/amazon_product.dart';
import 'package:cubalink23/models/walmart_product.dart';
import 'package:cubalink23/services/shipping_calculator.dart';

class ProductDetailsScreen extends StatefulWidget {
  final String? productId;
  final String? productTitle;
  final double? productPrice;
  final String? productImage;
  final String? productDescription;
  final double? productRating;
  final int? productReviews;
  final String? productBrand;
  final bool isFromAmazon;
  final bool isFromWalmart;
  final AmazonProduct? amazonProduct;
  final WalmartProduct? walmartProduct;
  final Map<String, dynamic>? product; // Legacy support

  const ProductDetailsScreen({
    Key? key,
    this.productId,
    this.productTitle,
    this.productPrice,
    this.productImage,
    this.productDescription,
    this.productRating,
    this.productReviews,
    this.productBrand,
    this.isFromAmazon = false,
    this.isFromWalmart = false,
    this.amazonProduct,
    this.walmartProduct,
    this.product,
  }) : super(key: key);

  @override
  _ProductDetailsScreenState createState() => _ProductDetailsScreenState();
}

class _ProductDetailsScreenState extends State<ProductDetailsScreen> {
  final CartService _cartService = CartService();
  final FavoritesService _favoritesService = FavoritesService.instance;
  int _quantity = 1;
  int _selectedImageIndex = 0;
  bool _isFavorite = false;
  

  @override
  void initState() {
    super.initState();
    _checkFavoriteStatus();
  }

  /// Obtener peso en libras del producto
  double _getWeightInLb() {
    if (widget.walmartProduct?.weight != null) {
      // Convertir de kg a libras
      return widget.walmartProduct!.getEstimatedWeightKg() * 2.20462;
    } else if (widget.amazonProduct?.weight != null) {
      // Convertir de kg a libras
      return (widget.amazonProduct!.weightKg ?? 0.5) * 2.20462;
    }
    return 1.1; // Default weight en libras (0.5 kg = 1.1 lb)
  }

  /// Obtener ID del vendedor
  String? _getVendorId() {
    if (widget.isFromAmazon) return 'amazon';
    if (widget.isFromWalmart) return 'walmart';
    return 'admin'; // Default to admin/store
  }

  /// Verificar si es un vendedor externo (Amazon, Walmart, etc.)
  bool _isExternalVendor(String? vendorId) {
    if (vendorId == null) return false;
    return ['amazon', 'walmart', 'ebay', 'homedepot', 'shein'].contains(vendorId.toLowerCase());
  }
  
  void _checkFavoriteStatus() async {
    await _favoritesService.initialize();
    final productId = widget.productId ?? widget.product?['id'] ?? 'unknown';
    setState(() {
      _isFavorite = _favoritesService.isFavorite(productId);
    });
  }


  @override
  Widget build(BuildContext context) {
    // Support both new and legacy formats
    final String title = widget.productTitle ?? widget.product?['title'] ?? widget.product?['name'] ?? 'Producto';
    final double price = widget.productPrice ?? widget.product?['price']?.toDouble() ?? 0.0;
    final String imageUrl = widget.productImage ?? widget.product?['image'] ?? widget.product?['imageUrl'] ?? '';
    final String description = widget.productDescription ?? widget.product?['description'] ?? 'Sin descripción disponible';
    final double rating = widget.productRating ?? widget.product?['rating']?.toDouble() ?? 0.0;
    final int reviews = widget.productReviews ?? widget.product?['reviewsCount'] ?? 0;
    
    // Get images from different product types
    List<String> images = [];
    if (widget.walmartProduct != null) {
      images = widget.walmartProduct!.images.isNotEmpty ? widget.walmartProduct!.images : [imageUrl];
    } else if (widget.amazonProduct != null) {
      images = widget.amazonProduct!.images.isNotEmpty ? widget.amazonProduct!.images : [imageUrl];
    } else {
      images = [imageUrl];
    }
    images = images.where((img) => img.isNotEmpty).toList();
    if (images.isEmpty) images = [imageUrl];
    
    // Get store colors
    Color primaryColor;
    
    if (widget.isFromWalmart) {
      primaryColor = Color(0xFF004C91);
    } else if (widget.isFromAmazon) {
      primaryColor = Color(0xFFFF9900);
    } else {
      primaryColor = Theme.of(context).colorScheme.primary;
    }

    // Calculate discount
    double? originalPrice;
    String? discountText;
    if (widget.walmartProduct?.originalPrice != null && widget.walmartProduct!.originalPrice! > price) {
      originalPrice = widget.walmartProduct!.originalPrice;
      final discount = widget.walmartProduct!.getDiscountPercentage();
      if (discount != null) discountText = '-${discount.toInt()}%';
    } else if (widget.amazonProduct?.originalPrice != null && widget.amazonProduct!.originalPrice! > price) {
      originalPrice = widget.amazonProduct!.originalPrice;
      // Calculate discount for Amazon if needed
      final discount = ((widget.amazonProduct!.originalPrice! - price) / widget.amazonProduct!.originalPrice!) * 100;
      if (discount > 0) discountText = '-${discount.toInt()}%';
    }

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          // Clean App Bar with Image
          SliverAppBar(
            expandedHeight: 400,
            pinned: true,
            backgroundColor: Colors.white,
            elevation: 0,
            leading: Container(
              margin: EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: IconButton(
                icon: Icon(Icons.close, color: Colors.black, size: 24),
                onPressed: () => Navigator.pop(context),
              ),
            ),
            actions: [
              // Share Button
              Container(
                margin: EdgeInsets.only(right: 8, top: 8, bottom: 8),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: IconButton(
                  icon: Icon(Icons.share, color: Colors.black, size: 24),
                  onPressed: () => _shareProduct(),
                ),
              ),
              // Favorite Button
              Container(
                margin: EdgeInsets.only(right: 16, top: 8, bottom: 8),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: IconButton(
                  icon: Icon(
                    _isFavorite ? Icons.favorite : Icons.favorite_border,
                    color: _isFavorite ? Colors.red : Colors.black,
                    size: 24,
                  ),
                  onPressed: () => _toggleFavorite(),
                ),
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                color: Colors.grey[50],
                child: Stack(
                  fit: StackFit.expand,
                  children: [
                    // Clean Product Image
                    PageView.builder(
                      itemCount: images.length,
                      onPageChanged: (index) {
                        setState(() {
                          _selectedImageIndex = index;
                        });
                      },
                      itemBuilder: (context, index) {
                        return Hero(
                          tag: 'product-${widget.productId ?? title}',
                          child: Container(
                            padding: EdgeInsets.all(40),
                            child: Image.network(
                              images[index],
                              fit: BoxFit.contain,
                              errorBuilder: (context, error, stackTrace) =>
                                  Container(
                                    decoration: BoxDecoration(
                                      color: Colors.grey[100],
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                    child: Column(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(
                                          Icons.image_not_supported,
                                          size: 60,
                                          color: Colors.grey[400],
                                        ),
                                        SizedBox(height: 16),
                                        Text(
                                          'Imagen no disponible',
                                          style: TextStyle(
                                            color: Colors.grey[600],
                                            fontSize: 16,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                            ),
                          ),
                        );
                      },
                    ),
                    // Simple page indicators
                    if (images.length > 1)
                      Positioned(
                        bottom: 20,
                        left: 0,
                        right: 0,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: images.asMap().entries.map((entry) {
                            return Container(
                              width: 8,
                              height: 8,
                              margin: EdgeInsets.symmetric(horizontal: 4),
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: _selectedImageIndex == entry.key
                                    ? Colors.black
                                    : Colors.grey[300],
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ),
          // Clean Product Details Content
          SliverToBoxAdapter(
            child: Container(
              color: Colors.white,
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Product Title - Clean and Simple
                    Text(
                      title,
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                        height: 1.3,
                      ),
                    ),
                    
                    SizedBox(height: 8),
                    
                    // Product Description/Details
                    if (description.isNotEmpty)
                      Text(
                        description,
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                          height: 1.4,
                        ),
                      ),
                    
                    SizedBox(height: 16),
                    
                    // Simple Rating Section
                    if (rating > 0 || reviews > 0)
                      Row(
                        children: [
                          ...List.generate(5, (index) {
                            return Icon(
                              index < rating.floor() ? Icons.star : Icons.star_border,
                              color: Colors.amber,
                              size: 20,
                            );
                          }),
                          SizedBox(width: 8),
                          Text(
                            '${rating.toStringAsFixed(1)} (${reviews} reseñas)',
                            style: TextStyle(
                              color: Colors.grey[600],
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    
                    if (rating > 0 || reviews > 0) SizedBox(height: 20),
                    
                    // Simple Price Section
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        if (originalPrice != null) ...[
                          Text(
                            '\$${originalPrice.toStringAsFixed(2)}',
                            style: TextStyle(
                              fontSize: 16,
                              decoration: TextDecoration.lineThrough,
                              color: Colors.grey.shade500,
                            ),
                          ),
                          SizedBox(width: 8),
                        ],
                        Text(
                          '\$${price.toStringAsFixed(2)}',
                          style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: Colors.black,
                          ),
                        ),
                        if (discountText != null) ...[
                          SizedBox(width: 12),
                          Container(
                            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: Colors.red,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              discountText,
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                    
                    SizedBox(height: 24),
                    
                    // Simple Stock Status
                    Row(
                      children: [
                        Icon(
                          Icons.check_circle,
                          color: Colors.green,
                          size: 20,
                        ),
                        SizedBox(width: 8),
                        Text(
                          'En Stock',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.green,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                    
                    SizedBox(height: 24),
                    
                    // Simple Quantity Selector
                    Row(
                      children: [
                        Text(
                          'Cantidad:',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        SizedBox(width: 16),
                        Container(
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey.shade300),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Row(
                            children: [
                              IconButton(
                                onPressed: _quantity > 1 ? () {
                                  setState(() {
                                    _quantity--;
                                  });
                                } : null,
                                icon: Icon(Icons.remove),
                                iconSize: 20,
                              ),
                              Container(
                                width: 40,
                                alignment: Alignment.center,
                                child: Text(
                                  _quantity.toString(),
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                              IconButton(
                                onPressed: () {
                                  setState(() {
                                    _quantity++;
                                  });
                                },
                                icon: Icon(Icons.add),
                                iconSize: 20,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    
                    SizedBox(height: 32),
                    
                    // Simple Description Section
                    if (description.isNotEmpty) ...[
                      Text(
                        'Descripción',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.black87,
                        ),
                      ),
                      SizedBox(height: 12),
                      Text(
                        description,
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.grey.shade700,
                          height: 1.5,
                        ),
                      ),
                      SizedBox(height: 32),
                    ],
                    
                    // Simple Action Button
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton(
                        onPressed: () => _addToCart(),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: primaryColor,
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          elevation: 2,
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.shopping_cart, size: 24),
                            SizedBox(width: 8),
                            Text(
                              'Agregar al carrito - \$${(price * _quantity).toStringAsFixed(2)}',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    
                    SizedBox(height: 32),
                    
                    // Related Products Section - "También compraron"
                    _buildRelatedProductsSection(),
                    
                    SizedBox(height: 32),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _addToCart() {
    // Calcular precio final para productos de Amazon/Walmart
    double finalPrice = widget.productPrice ?? widget.product?['price']?.toDouble() ?? 0.0;
    String? vendorId = _getVendorId();
    
    if (_isExternalVendor(vendorId)) {
      final weightLb = _getWeightInLb();
      final priceCalculation = ProductCostCalculator.calculateFinalPrice(
        basePrice: finalPrice,
        vendorId: vendorId!,
        weightLb: weightLb,
        zipCode: '33470', // Nuestra bodega
      );
      finalPrice = priceCalculation.finalPrice;
    }
    
    Map<String, dynamic> cartItem = {
      'id': widget.productId ?? widget.product?['id'] ?? 'unknown',
      'title': widget.productTitle ?? widget.product?['title'] ?? widget.product?['name'] ?? 'Producto',
      'price': finalPrice, // Precio final ya incluye envío y taxes
      'imageUrl': widget.productImage ?? widget.product?['image'] ?? widget.product?['imageUrl'] ?? '',
      'store': widget.isFromWalmart ? 'Walmart' : widget.isFromAmazon ? 'Amazon' : widget.product?['store'] ?? 'Tienda',
      'brand': widget.productBrand ?? widget.product?['brand'] ?? 'Desconocido',
      'quantity': _quantity,
      'vendorId': vendorId, // Agregar vendorId para identificar el vendedor
    };

    // Add weight information if available
    if (widget.walmartProduct?.weight != null) {
      cartItem['weight'] = widget.walmartProduct!.weight;
      cartItem['weightLb'] = widget.walmartProduct!.getEstimatedWeightKg() * 2.20462; // Convert to lbs
    } else if (widget.amazonProduct?.weight != null) {
      cartItem['weight'] = widget.amazonProduct!.weight;
      cartItem['weightLb'] = widget.amazonProduct!.weightKg != null 
          ? widget.amazonProduct!.weightKg! * 2.20462 // Convert kg to lbs
          : 1.1; // Default weight in lbs
    }

    // Add rating and reviews if available
    if (widget.productRating != null) cartItem['rating'] = widget.productRating;
    if (widget.productReviews != null) cartItem['reviewsCount'] = widget.productReviews;

    for (int i = 0; i < _quantity; i++) {
      _cartService.addAmazonProduct(cartItem);
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.check_circle, color: Colors.white),
            SizedBox(width: 8),
            Expanded(
              child: Text('$_quantity producto(s) agregado(s) al carrito'),
            ),
          ],
        ),
        backgroundColor: widget.isFromWalmart ? Color(0xFF004C91) : widget.isFromAmazon ? Color(0xFFFF9900) : Theme.of(context).colorScheme.primary,
        duration: Duration(seconds: 2),
      ),
    );

    // Navigate back or show success
    Navigator.pop(context);
  }

  void _shareProduct() {
    final String title = widget.productTitle ?? widget.product?['title'] ?? widget.product?['name'] ?? 'Producto';
    final double price = widget.productPrice ?? widget.product?['price']?.toDouble() ?? 0.0;
    final String storeName = widget.isFromWalmart ? 'Walmart' : widget.isFromAmazon ? 'Amazon' : widget.product?['store'] ?? 'Tienda';
    
    final String shareText = '''
🛍️ ¡Mira este producto en CubaLink23!

📦 $title
💰 Precio: \$${price.toStringAsFixed(2)}
🏪 Tienda: $storeName

Descarga CubaLink23 para más productos increíbles:
https://cubalink23.com
''';

    Share.share(
      shareText,
      subject: 'Producto: $title',
    );
  }

  void _toggleFavorite() async {
    final String title = widget.productTitle ?? widget.product?['title'] ?? widget.product?['name'] ?? 'Producto';
    final String productId = widget.productId ?? widget.product?['id'] ?? 'unknown';
    final double price = widget.productPrice ?? widget.product?['price']?.toDouble() ?? 0.0;
    final String imageUrl = widget.productImage ?? widget.product?['image'] ?? widget.product?['imageUrl'] ?? '';
    final String description = widget.productDescription ?? widget.product?['description'] ?? 'Sin descripción disponible';
    final String brand = widget.productBrand ?? widget.product?['brand'] ?? 'Desconocido';
    final String storeName = widget.isFromWalmart ? 'Walmart' : widget.isFromAmazon ? 'Amazon' : widget.product?['store'] ?? 'Tienda';
    
    // Create product map for favorites
    final productMap = FavoritesService.createProductMap(
      id: productId,
      name: title,
      price: price,
      imageUrl: imageUrl,
      description: description,
      category: widget.product?['category'] ?? 'General',
      store: storeName,
      brand: brand,
      rating: widget.productRating ?? widget.product?['rating']?.toDouble(),
      reviewsCount: widget.productReviews ?? widget.product?['reviewsCount'],
    );
    
    // Toggle favorite status
    final success = await _favoritesService.toggleFavorite(productMap);
    
    if (success) {
      setState(() {
        _isFavorite = _favoritesService.isFavorite(productId);
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              Icon(
                _isFavorite ? Icons.favorite : Icons.favorite_border,
                color: Colors.white,
              ),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  _isFavorite 
                    ? 'Agregado a favoritos: $title'
                    : 'Removido de favoritos: $title'
                ),
              ),
            ],
          ),
          backgroundColor: _isFavorite ? Colors.red : Colors.grey[600],
          duration: Duration(seconds: 2),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error al actualizar favoritos'),
          backgroundColor: Colors.red,
          duration: Duration(seconds: 2),
        ),
      );
    }
  }

  Widget _buildRelatedProductsSection() {
    // Sample related products data - you can replace this with real data
    final relatedProducts = [
      {
        'name': 'Macarrones (Coditos)',
        'weight': '500 g',
        'price': 3.13,
        'image': 'https://via.placeholder.com/80x80/FFE0B2/000000?text=Macarrones',
      },
      {
        'name': 'Galletas Dulces',
        'weight': '20 unidades',
        'price': 2.50,
        'image': 'https://via.placeholder.com/80x80/E1F5FE/000000?text=Galletas',
      },
      {
        'name': 'Aceite de Cocina',
        'weight': '900ml',
        'price': 4.20,
        'image': 'https://via.placeholder.com/80x80/F3E5F5/000000?text=Aceite',
      },
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Section Title
        Text(
          'También compraron',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.black87,
          ),
        ),
        
        SizedBox(height: 16),
        
        // Related Products List
        ...relatedProducts.map((product) => _buildRelatedProductItem(product)).toList(),
      ],
    );
  }

  Widget _buildRelatedProductItem(Map<String, dynamic> product) {
    return Container(
      margin: EdgeInsets.only(bottom: 12),
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Colors.grey[200]!,
          width: 1,
        ),
      ),
      child: Row(
        children: [
          // Checkbox
          Container(
            width: 20,
            height: 20,
            decoration: BoxDecoration(
              border: Border.all(color: Colors.grey[400]!),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Icon(
              Icons.check,
              size: 16,
              color: Colors.transparent,
            ),
          ),
          
          SizedBox(width: 12),
          
          // Product Info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  product['name'],
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  product['weight'],
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '\$${product['price'].toStringAsFixed(2)}',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                ),
              ],
            ),
          ),
          
          // Product Image and Add Button
          Stack(
            children: [
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(8),
                  color: Colors.white,
                  border: Border.all(color: Colors.grey[300]!),
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Image.network(
                    product['image'],
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) =>
                        Container(
                          color: Colors.grey[200],
                          child: Icon(
                            Icons.image_not_supported,
                            color: Colors.grey[400],
                            size: 24,
                          ),
                        ),
                  ),
                ),
              ),
              // Add Button
              Positioned(
                bottom: -2,
                right: -2,
                child: Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primary,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2),
                  ),
                  child: Icon(
                    Icons.add,
                    color: Colors.white,
                    size: 16,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}