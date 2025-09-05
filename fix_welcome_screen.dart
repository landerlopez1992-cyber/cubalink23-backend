
// ARREGLO PARA WELCOME SCREEN - lib/screens/welcome/welcome_screen_fixed.dart

class _WelcomeScreenFixedState extends State<WelcomeScreenFixed> {
  // ... código existente ...

  @override
  void initState() {
    super.initState();
    print('🚀 WelcomeScreenFixed - INICIANDO DE FORMA NO BLOQUEANTE');
    
    // Mostrar UI inmediatamente con valores por defecto
    setState(() {
      _isLoading = false;
      _currentBalance = 0.0;
      _categories = _getDefaultCategoriesMap();
      _bestSellers = _getDefaultProductsMap();
    });
    
    // ARREGLO: Configurar CartService y cargar carrito
    _cartService.addListener(_updateCartCount);
    _initializeCart();
    
    // Cargar datos en background SIN BLOQUEAR la UI
    _loadDataInBackground();
    
    print('✅ WelcomeScreenFixed - UI MOSTRADA INMEDIATAMENTE');
  }

  /// ARREGLO: Inicializar carrito correctamente
  Future<void> _initializeCart() async {
    try {
      print('🛒 Inicializando carrito en WelcomeScreen...');
      await _cartService.initializeCart();
      _updateCartCount();
      print('✅ Carrito inicializado: ${_cartService.itemCount} items');
    } catch (e) {
      print('❌ Error inicializando carrito: $e');
    }
  }

  /// ARREGLO: Mejorar _loadCartItemsCount
  Future<void> _loadCartItemsCount() async {
    try {
      print('🛒 Cargando conteo de carrito...');
      
      // Asegurar que el carrito esté cargado
      if (_cartService.itemCount == 0) {
        await _cartService.loadFromSupabase();
      }
      
      if (mounted) {
        setState(() {
          _cartItemsCount = _cartService.itemCount;
        });
        print('✅ Conteo de carrito actualizado: $_cartItemsCount');
      }
    } catch (e) {
      print('❌ Error cargando conteo de carrito: $e');
    }
  }

  /// ARREGLO: Mejorar _updateCartCount
  void _updateCartCount() {
    if (mounted) {
      setState(() {
        _cartItemsCount = _cartService.itemCount;
      });
      print('🛒 Carrito actualizado: $_cartItemsCount productos');
    }
  }
}
