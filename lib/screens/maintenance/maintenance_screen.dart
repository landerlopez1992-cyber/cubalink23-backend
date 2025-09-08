import 'package:flutter/material.dart';

class MaintenanceScreen extends StatefulWidget {
  @override
  _MaintenanceScreenState createState() => _MaintenanceScreenState();
}

class _MaintenanceScreenState extends State<MaintenanceScreen>
    with TickerProviderStateMixin {
  late AnimationController _workerController;
  late AnimationController _shovelController;
  late AnimationController _pulseController;
  
  late Animation<double> _workerAnimation;
  late Animation<double> _shovelAnimation;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    
    // Controlador para la animación del obrero
    _workerController = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    );
    
    // Controlador para la animación de la pala
    _shovelController = AnimationController(
      duration: Duration(milliseconds: 800),
      vsync: this,
    );
    
    // Controlador para la animación de pulso
    _pulseController = AnimationController(
      duration: Duration(seconds: 1),
      vsync: this,
    );

    // Animación del obrero (movimiento de izquierda a derecha)
    _workerAnimation = Tween<double>(
      begin: -50.0,
      end: 50.0,
    ).animate(CurvedAnimation(
      parent: _workerController,
      curve: Curves.easeInOut,
    ));

    // Animación de la pala (movimiento de excavación)
    _shovelAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _shovelController,
      curve: Curves.easeInOut,
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
    // Animación continua del obrero
    _workerController.repeat(reverse: true);
    
    // Animación de la pala cada 2 segundos
    _shovelController.repeat(reverse: true);
    
    // Animación de pulso continua
    _pulseController.repeat(reverse: true);
  }

  @override
  void dispose() {
    _workerController.dispose();
    _shovelController.dispose();
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.orange[50],
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.orange[100]!,
              Colors.amber[50]!,
              Colors.yellow[50]!,
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
                  
                  // Icono de construcción
                  Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      color: Colors.orange[200],
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.orange.withOpacity(0.3),
                          blurRadius: 20,
                          offset: Offset(0, 10),
                        ),
                      ],
                    ),
                    child: Icon(
                      Icons.construction,
                      size: 60,
                      color: Colors.orange[800],
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
                          'MANTENIMIENTO',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.orange[800],
                            letterSpacing: 2,
                          ),
                        ),
                      );
                    },
                  ),
                  
                  SizedBox(height: 20),
                  
                  // Subtítulo
                  Text(
                    'Estamos dándole mantenimiento al sistema',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                      color: Colors.orange[700],
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  SizedBox(height: 8),
                  
                  Text(
                    'para agregar nuevas funciones y servicios',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.orange[600],
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  SizedBox(height: 40),
                  
                  // Animación del obrero trabajando
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
                              color: Colors.brown[300],
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Center(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                children: List.generate(8, (index) {
                                  return Container(
                                    width: 4,
                                    height: 20,
                                    color: Colors.brown[400],
                                  );
                                }),
                              ),
                            ),
                          ),
                        ),
                        
                        // Obrero animado
                        AnimatedBuilder(
                          animation: _workerAnimation,
                          builder: (context, child) {
                            return Positioned(
                              left: MediaQuery.of(context).size.width / 2 - 30 + _workerAnimation.value,
                              bottom: 40,
                              child: _buildWorker(),
                            );
                          },
                        ),
                        
                        // Pala animada
                        AnimatedBuilder(
                          animation: _shovelAnimation,
                          builder: (context, child) {
                            return Positioned(
                              left: MediaQuery.of(context).size.width / 2 - 15 + _workerAnimation.value,
                              bottom: 60 + (_shovelAnimation.value * 20),
                              child: _buildShovel(),
                            );
                          },
                        ),
                        
                        // Partículas de tierra
                        ...List.generate(5, (index) {
                          return AnimatedBuilder(
                            animation: _shovelController,
                            builder: (context, child) {
                              final delay = index * 0.2;
                              final animationValue = (_shovelController.value + delay) % 1.0;
                              return Positioned(
                                left: MediaQuery.of(context).size.width / 2 - 10 + _workerAnimation.value + (index * 10),
                                bottom: 80 + (animationValue * 40),
                                child: Opacity(
                                  opacity: 1 - animationValue,
                                  child: Container(
                                    width: 3,
                                    height: 3,
                                    decoration: BoxDecoration(
                                      color: Colors.brown[600],
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
                  
                  // Mensaje de espera
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.orange.withOpacity(0.2),
                          blurRadius: 10,
                          offset: Offset(0, 5),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        Icon(
                          Icons.schedule,
                          color: Colors.orange[600],
                          size: 32,
                        ),
                        SizedBox(height: 12),
                        Text(
                          'Espere unos minutos',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.orange[800],
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'En breve estará disponible el sistema',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.orange[600],
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                  
                  SizedBox(height: 40),
                  
                  // Indicador de carga
                  Container(
                    width: 200,
                    height: 6,
                    decoration: BoxDecoration(
                      color: Colors.orange[200],
                      borderRadius: BorderRadius.circular(3),
                    ),
                    child: AnimatedBuilder(
                      animation: _pulseController,
                      builder: (context, child) {
                        return Container(
                          width: 200 * _pulseAnimation.value,
                          height: 6,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [Colors.orange[400]!, Colors.orange[600]!],
                            ),
                            borderRadius: BorderRadius.circular(3),
                          ),
                        );
                      },
                    ),
                  ),
                  
                  SizedBox(height: 20),
                  
                  // Texto de estado
                  Text(
                    'Trabajando en mejoras...',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.orange[500],
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

  Widget _buildWorker() {
    return Container(
      width: 60,
      height: 80,
      child: Stack(
        children: [
          // Cuerpo del obrero
          Positioned(
            bottom: 0,
            left: 15,
            child: Container(
              width: 30,
              height: 50,
              decoration: BoxDecoration(
                color: Colors.blue[600],
                borderRadius: BorderRadius.circular(15),
              ),
            ),
          ),
          
          // Cabeza
          Positioned(
            bottom: 45,
            left: 20,
            child: Container(
              width: 20,
              height: 20,
              decoration: BoxDecoration(
                color: Colors.orange[200],
                shape: BoxShape.circle,
              ),
            ),
          ),
          
          // Casco
          Positioned(
            bottom: 48,
            left: 18,
            child: Container(
              width: 24,
              height: 12,
              decoration: BoxDecoration(
                color: Colors.yellow[600],
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          
          // Brazos
          Positioned(
            bottom: 30,
            left: 5,
            child: Container(
              width: 8,
              height: 25,
              decoration: BoxDecoration(
                color: Colors.orange[200],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
          
          Positioned(
            bottom: 30,
            right: 5,
            child: Container(
              width: 8,
              height: 25,
              decoration: BoxDecoration(
                color: Colors.orange[200],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
          
          // Piernas
          Positioned(
            bottom: 0,
            left: 18,
            child: Container(
              width: 8,
              height: 30,
              decoration: BoxDecoration(
                color: Colors.blue[800],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
          
          Positioned(
            bottom: 0,
            right: 18,
            child: Container(
              width: 8,
              height: 30,
              decoration: BoxDecoration(
                color: Colors.blue[800],
                borderRadius: BorderRadius.circular(4),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildShovel() {
    return Transform.rotate(
      angle: _shovelAnimation.value * 0.3,
      child: Container(
        width: 30,
        height: 40,
        child: Stack(
          children: [
            // Mango de la pala
            Positioned(
              bottom: 0,
              left: 12,
              child: Container(
                width: 6,
                height: 30,
                decoration: BoxDecoration(
                  color: Colors.brown[600],
                  borderRadius: BorderRadius.circular(3),
                ),
              ),
            ),
            
            // Cabeza de la pala
            Positioned(
              top: 0,
              left: 8,
              child: Container(
                width: 14,
                height: 12,
                decoration: BoxDecoration(
                  color: Colors.grey[600],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
