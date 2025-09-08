import 'package:flutter/material.dart';
import 'dart:io';

class ForceUpdateScreen extends StatefulWidget {
  @override
  _ForceUpdateScreenState createState() => _ForceUpdateScreenState();
}

class _ForceUpdateScreenState extends State<ForceUpdateScreen>
    with TickerProviderStateMixin {
  late AnimationController _danceController;
  late AnimationController _bounceController;
  late AnimationController _pulseController;
  
  late Animation<double> _danceAnimation;
  late Animation<double> _bounceAnimation;
  late Animation<double> _pulseAnimation;

  bool get isAndroid => Platform.isAndroid;
  bool get isIOS => Platform.isIOS;

  @override
  void initState() {
    super.initState();
    
    // Controlador para la animación de baile
    _danceController = AnimationController(
      duration: Duration(milliseconds: 1500),
      vsync: this,
    );
    
    // Controlador para la animación de rebote
    _bounceController = AnimationController(
      duration: Duration(milliseconds: 800),
      vsync: this,
    );
    
    // Controlador para la animación de pulso
    _pulseController = AnimationController(
      duration: Duration(seconds: 1),
      vsync: this,
    );

    // Animación de baile (rotación y movimiento)
    _danceAnimation = Tween<double>(
      begin: -0.1,
      end: 0.1,
    ).animate(CurvedAnimation(
      parent: _danceController,
      curve: Curves.elasticInOut,
    ));

    // Animación de rebote
    _bounceAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _bounceController,
      curve: Curves.bounceOut,
    ));

    // Animación de pulso para el texto
    _pulseAnimation = Tween<double>(
      begin: 0.8,
      end: 1.2,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));

    // Iniciar animaciones
    _startAnimations();
  }

  void _startAnimations() {
    // Animación continua de baile
    _danceController.repeat(reverse: true);
    
    // Animación de rebote cada 2 segundos
    _bounceController.repeat(reverse: true);
    
    // Animación de pulso continua
    _pulseController.repeat(reverse: true);
  }

  @override
  void dispose() {
    _danceController.dispose();
    _bounceController.dispose();
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: isAndroid ? Colors.green[50] : Colors.grey[50],
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: isAndroid ? [
              Colors.green[100]!,
              Colors.lightGreen[50]!,
              Colors.green[50]!,
            ] : [
              Colors.grey[100]!,
              Colors.grey[50]!,
              Colors.white,
            ],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: EdgeInsets.all(24),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(height: 40),
                  
                  // Icono de actualización
                  Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      color: isAndroid ? Colors.green[200] : Colors.grey[200],
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: (isAndroid ? Colors.green : Colors.grey).withOpacity(0.3),
                          blurRadius: 20,
                          offset: Offset(0, 10),
                        ),
                      ],
                    ),
                    child: Icon(
                      Icons.system_update,
                      size: 60,
                      color: isAndroid ? Colors.green[800] : Colors.grey[800],
                    ),
                  ),
                  
                  SizedBox(height: 40),
                  
                  // Título principal
                  AnimatedBuilder(
                    animation: _pulseAnimation,
                    builder: (context, child) {
                      return Transform.scale(
                        scale: _pulseAnimation.value,
                        child: Text(
                          'ACTUALIZACIÓN REQUERIDA',
                          style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: isAndroid ? Colors.green[800] : Colors.grey[800],
                            letterSpacing: 1.5,
                          ),
                        ),
                      );
                    },
                  ),
                  
                  SizedBox(height: 20),
                  
                  // Subtítulo
                  Text(
                    'Una nueva versión está disponible',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                      color: isAndroid ? Colors.green[700] : Colors.grey[700],
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  SizedBox(height: 8),
                  
                  Text(
                    'Actualiza la app para disfrutar de las últimas funciones',
                    style: TextStyle(
                      fontSize: 16,
                      color: isAndroid ? Colors.green[600] : Colors.grey[600],
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  SizedBox(height: 40),
                  
                  // Animación del Android/Apple bailando
                  Container(
                    height: 200,
                    width: double.infinity,
                    child: Stack(
                      children: [
                        // Suelo
                        Positioned(
                          bottom: 0,
                          left: 0,
                          right: 0,
                          child: Container(
                            height: 40,
                            decoration: BoxDecoration(
                              color: isAndroid ? Colors.green[300] : Colors.grey[300],
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Center(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                children: List.generate(8, (index) {
                                  return Container(
                                    width: 4,
                                    height: 20,
                                    color: isAndroid ? Colors.green[400] : Colors.grey[400],
                                  );
                                }),
                              ),
                            ),
                          ),
                        ),
                        
                        // Android/Apple bailando
                        AnimatedBuilder(
                          animation: _danceAnimation,
                          builder: (context, child) {
                            return Positioned(
                              left: MediaQuery.of(context).size.width / 2 - 40,
                              bottom: 40,
                              child: Transform.rotate(
                                angle: _danceAnimation.value,
                                child: Transform.translate(
                                  offset: Offset(0, _bounceAnimation.value * -10),
                                  child: isAndroid ? _buildAndroid() : _buildApple(),
                                ),
                              ),
                            );
                          },
                        ),
                        
                        // Partículas de celebración
                        ...List.generate(6, (index) {
                          return AnimatedBuilder(
                            animation: _bounceController,
                            builder: (context, child) {
                              final delay = index * 0.2;
                              final animationValue = (_bounceController.value + delay) % 1.0;
                              return Positioned(
                                left: MediaQuery.of(context).size.width / 2 - 20 + (index * 15),
                                bottom: 60 + (animationValue * 30),
                                child: Opacity(
                                  opacity: 1 - animationValue,
                                  child: Container(
                                    width: 4,
                                    height: 4,
                                    decoration: BoxDecoration(
                                      color: isAndroid ? Colors.green[600] : Colors.grey[600],
                                      shape: BoxShape.circle,
                                    ),
                                  ),
                                ),
                              );
                            },
                          );
                        }),
                      ],
                    ),
                  ),
                  
                  SizedBox(height: 40),
                  
                  // Mensaje de actualización
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: (isAndroid ? Colors.green : Colors.grey).withOpacity(0.2),
                          blurRadius: 10,
                          offset: Offset(0, 5),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        Icon(
                          Icons.store,
                          color: isAndroid ? Colors.green[600] : Colors.grey[600],
                          size: 32,
                        ),
                        SizedBox(height: 12),
                        Text(
                          'Ve a la tienda de aplicaciones',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: isAndroid ? Colors.green[800] : Colors.grey[800],
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          isAndroid 
                            ? 'Google Play Store'
                            : 'App Store',
                          style: TextStyle(
                            fontSize: 14,
                            color: isAndroid ? Colors.green[600] : Colors.grey[600],
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                  
                  SizedBox(height: 40),
                  
                  // Botón de actualizar
                  Container(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: () {
                        // TODO: Implementar lógica de actualización
                        _showUpdateDialog();
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: isAndroid ? Colors.green[600] : Colors.grey[600],
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        elevation: 8,
                        shadowColor: (isAndroid ? Colors.green : Colors.grey).withOpacity(0.3),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.download,
                            size: 24,
                          ),
                          SizedBox(width: 12),
                          Text(
                            'Actualizar la App',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  SizedBox(height: 20),
                  
                  // Texto de estado
                  Text(
                    '¡No te pierdas las nuevas funciones!',
                    style: TextStyle(
                      fontSize: 14,
                      color: isAndroid ? Colors.green[500] : Colors.grey[500],
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                  
                  SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildAndroid() {
    return Container(
      width: 80,
      height: 100,
      child: Stack(
        children: [
          // Cuerpo del Android
          Positioned(
            bottom: 0,
            left: 20,
            child: Container(
              width: 40,
              height: 60,
              decoration: BoxDecoration(
                color: Colors.green[600],
                borderRadius: BorderRadius.circular(20),
              ),
            ),
          ),
          
          // Cabeza del Android
          Positioned(
            bottom: 55,
            left: 25,
            child: Container(
              width: 30,
              height: 30,
              decoration: BoxDecoration(
                color: Colors.green[600],
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          // Antenas del Android
          Positioned(
            bottom: 80,
            left: 30,
            child: Container(
              width: 3,
              height: 15,
              decoration: BoxDecoration(
                color: Colors.green[800],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          
          Positioned(
            bottom: 80,
            right: 30,
            child: Container(
              width: 3,
              height: 15,
              decoration: BoxDecoration(
                color: Colors.green[800],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          
          // Ojos del Android
          Positioned(
            bottom: 65,
            left: 32,
            child: Container(
              width: 4,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.white,
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          Positioned(
            bottom: 65,
            right: 32,
            child: Container(
              width: 4,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.white,
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          // Sonrisa del Android
          Positioned(
            bottom: 60,
            left: 35,
            child: Container(
              width: 10,
              height: 5,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(5),
                  bottomRight: Radius.circular(5),
                ),
              ),
            ),
          ),
          
          // Brazos del Android
          Positioned(
            bottom: 40,
            left: 10,
            child: Container(
              width: 8,
              height: 20,
              decoration: BoxDecoration(
                color: Colors.green[600],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
          
          Positioned(
            bottom: 40,
            right: 10,
            child: Container(
              width: 8,
              height: 20,
              decoration: BoxDecoration(
                color: Colors.green[600],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
          
          // Piernas del Android
          Positioned(
            bottom: 0,
            left: 25,
            child: Container(
              width: 8,
              height: 25,
              decoration: BoxDecoration(
                color: Colors.green[600],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
          
          Positioned(
            bottom: 0,
            right: 25,
            child: Container(
              width: 8,
              height: 25,
              decoration: BoxDecoration(
                color: Colors.green[600],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildApple() {
    return Container(
      width: 80,
      height: 100,
      child: Stack(
        children: [
          // Cuerpo de la manzana
          Positioned(
            bottom: 0,
            left: 20,
            child: Container(
              width: 40,
              height: 50,
              decoration: BoxDecoration(
                color: Colors.grey[600],
                borderRadius: BorderRadius.circular(20),
              ),
            ),
          ),
          
          // Cabeza de la manzana
          Positioned(
            bottom: 45,
            left: 25,
            child: Container(
              width: 30,
              height: 30,
              decoration: BoxDecoration(
                color: Colors.grey[600],
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          // Tallo de la manzana
          Positioned(
            bottom: 70,
            left: 35,
            child: Container(
              width: 3,
              height: 10,
              decoration: BoxDecoration(
                color: Colors.green[700],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          
          // Hoja de la manzana
          Positioned(
            bottom: 75,
            left: 30,
            child: Container(
              width: 8,
              height: 6,
              decoration: BoxDecoration(
                color: Colors.green[600],
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
          
          // Ojos de la manzana
          Positioned(
            bottom: 60,
            left: 32,
            child: Container(
              width: 3,
              height: 3,
              decoration: BoxDecoration(
                color: Colors.white,
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          Positioned(
            bottom: 60,
            right: 32,
            child: Container(
              width: 3,
              height: 3,
              decoration: BoxDecoration(
                color: Colors.white,
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          // Sonrisa de la manzana
          Positioned(
            bottom: 55,
            left: 35,
            child: Container(
              width: 10,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(4),
                  bottomRight: Radius.circular(4),
                ),
              ),
            ),
          ),
          
          // Brazos de la manzana
          Positioned(
            bottom: 35,
            left: 10,
            child: Container(
              width: 6,
              height: 15,
              decoration: BoxDecoration(
                color: Colors.grey[600],
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
          
          Positioned(
            bottom: 35,
            right: 10,
            child: Container(
              width: 6,
              height: 15,
              decoration: BoxDecoration(
                color: Colors.grey[600],
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
          
          // Piernas de la manzana
          Positioned(
            bottom: 0,
            left: 30,
            child: Container(
              width: 6,
              height: 20,
              decoration: BoxDecoration(
                color: Colors.grey[600],
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
          
          Positioned(
            bottom: 0,
            right: 30,
            child: Container(
              width: 6,
              height: 20,
              decoration: BoxDecoration(
                color: Colors.grey[600],
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showUpdateDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          title: Row(
            children: [
              Icon(
                Icons.info_outline,
                color: isAndroid ? Colors.green[600] : Colors.grey[600],
              ),
              SizedBox(width: 8),
              Text('Actualización'),
            ],
          ),
          content: Text(
            'Esta función abrirá la tienda de aplicaciones para que puedas actualizar la app.',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Cancelar'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
                // TODO: Implementar apertura de tienda
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: isAndroid ? Colors.green[600] : Colors.grey[600],
                foregroundColor: Colors.white,
              ),
              child: Text('Ir a la Tienda'),
            ),
          ],
        );
      },
    );
  }
}
