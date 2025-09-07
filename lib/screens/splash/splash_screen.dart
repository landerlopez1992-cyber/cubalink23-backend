import 'package:flutter/material.dart';
import 'dart:async';
import 'package:cubalink23/screens/welcome/welcome_screen.dart';

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with TickerProviderStateMixin {
  late AnimationController _logoAnimationController;
  late AnimationController _progressAnimationController;
  late Animation<double> _logoAnimation;
  late Animation<double> _progressAnimation;
  
  double _progress = 0.0;
  Timer? _progressTimer;
  Timer? _navigationTimer;

  @override
  void initState() {
    super.initState();
    print('🎬 SplashScreen initState() llamado');
    
    try {
      // Configurar animaciones
      _logoAnimationController = AnimationController(
        duration: Duration(milliseconds: 1500),
        vsync: this,
      );
      
      _progressAnimationController = AnimationController(
        duration: Duration(seconds: 1), // Reducido a 1 segundo para debug
        vsync: this,
      );
      
      _logoAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
        CurvedAnimation(parent: _logoAnimationController, curve: Curves.easeInOut),
      );
      
      _progressAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
        CurvedAnimation(parent: _progressAnimationController, curve: Curves.linear),
      );
      
      print('✅ Animaciones configuradas correctamente');
      
      // Iniciar animaciones
      _startSplashSequence();
    } catch (e, stackTrace) {
      print('❌ Error en initState de SplashScreen: $e');
      print('❌ Stack trace: $stackTrace');
      // Navegar inmediatamente si hay error
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _navigateToWelcome();
      });
    }
  }

  void _startSplashSequence() {
    print('🎬 Iniciando secuencia de splash screen...');
    
    // Animar logo primero
    _logoAnimationController.forward();
    print('▶️ Animación de logo iniciada');
    
    // Después de 500ms, iniciar la barra de progreso
    Timer(Duration(milliseconds: 500), () {
      if (mounted) {
        print('📊 Iniciando animación de progreso...');
        _progressAnimationController.forward();
        
        // Actualizar progreso cada 100ms para efecto suave
        _progressTimer = Timer.periodic(Duration(milliseconds: 100), (timer) {
          if (mounted) {
            setState(() {
              _progress = _progressAnimationController.value;
            });
          } else {
            timer.cancel();
          }
        });
      }
    });
    
    // Navegar después de 2 segundos para mostrar animación completa
    _navigationTimer = Timer(Duration(milliseconds: 2000), () {
      if (mounted) {
        _navigateToWelcome();
      }
    });
  }
  
  void _navigateToWelcome() {
    if (!mounted) {
      print('❌ Widget no está montado, navegación cancelada');
      return;
    }
    
    print('🚀 ===== NAVEGANDO A WELCOME =====');
    
    try {
      // Navegar directamente usando MaterialPageRoute para evitar problemas de contexto
      print('🔧 Navegando directamente a WelcomeScreen...');
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (context) => WelcomeScreen(),
          settings: RouteSettings(name: '/welcome'),
        ),
      );
      print('✅ Navegación exitosa a WelcomeScreen');
    } catch (e) {
      print('❌ Error navegando a WelcomeScreen: $e');
      
      // Fallback: Intentar con ruta nombrada
      try {
        print('🔧 Intentando fallback con ruta nombrada...');
        Navigator.of(context).pushReplacementNamed('/welcome');
        print('✅ Navegación exitosa con ruta nombrada');
      } catch (e2) {
        print('❌ Error total en navegación: $e2');
        print('⚠️ NAVEGACIÓN COMPLETAMENTE FALLIDA');
      }
    }
  }

  @override
  void dispose() {
    _logoAnimationController.dispose();
    _progressAnimationController.dispose();
    _progressTimer?.cancel();
    _navigationTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    print('🏗️ SplashScreen build() llamado');
    
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.primary,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Spacer(flex: 2),
            
            // Logo con animación
            AnimatedBuilder(
              animation: _logoAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _logoAnimation.value,
                  child: Opacity(
                    opacity: _logoAnimation.value,
                    child: Container(
                      width: 150,
                      height: 150,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity( 0.3),
                            blurRadius: 20,
                            offset: Offset(0, 10),
                          ),
                        ],
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(20),
                        child: Image.asset(
                          'assets/images/assets_task_01k3m7yveaebmtdrdnybpe7ngv_1756247471_img_1.webp',
                          fit: BoxFit.contain,
                          errorBuilder: (context, error, stackTrace) {
                            print('⚠️ Error cargando imagen del logo: $error');
                            // Fallback si no se encuentra la imagen
                            return Container(
                              width: 150,
                              height: 150,
                              decoration: BoxDecoration(
                                color: Theme.of(context).colorScheme.onPrimary,
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: Icon(
                                Icons.phone_android,
                                size: 60,
                                color: Theme.of(context).colorScheme.primary,
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
            
            Spacer(),
            
            // Título de la app
            AnimatedBuilder(
              animation: _logoAnimation,
              builder: (context, child) {
                return Opacity(
                  opacity: _logoAnimation.value,
                  child: Text(
                    'CubaLink23',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Theme.of(context).colorScheme.onPrimary,
                      letterSpacing: 1.2,
                    ),
                  ),
                );
              },
            ),
            
            SizedBox(height: 8),
            
            // Subtítulo
            AnimatedBuilder(
              animation: _logoAnimation,
              builder: (context, child) {
                return Opacity(
                  opacity: _logoAnimation.value * 0.8,
                  child: Text(
                    'Recargas Telefónicas',
                    style: TextStyle(
                      fontSize: 16,
                      color: Theme.of(context).colorScheme.onPrimary.withOpacity( 0.9),
                      letterSpacing: 0.5,
                    ),
                  ),
                );
              },
            ),
            
            Spacer(),
            
            // Barra de progreso
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 60),
              child: Column(
                children: [
                  // Texto "Cargando..."
                  Text(
                    'Cargando${_getLoadingDots()}',
                    style: TextStyle(
                      fontSize: 16,
                      color: Theme.of(context).colorScheme.onPrimary.withOpacity( 0.9),
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  
                  SizedBox(height: 16),
                  
                  // Barra de progreso
                  Container(
                    height: 6,
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.onPrimary.withOpacity( 0.3),
                      borderRadius: BorderRadius.circular(3),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(3),
                      child: LinearProgressIndicator(
                        value: _progress,
                        backgroundColor: Colors.transparent,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          Theme.of(context).colorScheme.onPrimary,
                        ),
                      ),
                    ),
                  ),
                  
                  SizedBox(height: 8),
                  
                  // Porcentaje
                  Text(
                    '${(_progress * 100).toInt()}%',
                    style: TextStyle(
                      fontSize: 14,
                      color: Theme.of(context).colorScheme.onPrimary.withOpacity( 0.8),
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
            
            Spacer(),
          ],
        ),
      ),
    );
  }

  String _getLoadingDots() {
    int dotCount = ((_progress * 12) % 4).toInt();
    return '.' * (dotCount + 1);
  }
}