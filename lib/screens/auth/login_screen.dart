import 'package:flutter/material.dart';
import 'package:cubalink23/services/auth_service_bypass.dart';
import 'package:cubalink23/screens/auth/register_screen.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _identifierController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;
  bool _isEmailLogin = true; // true para email, false para teléfono

  Future<void> _login() async {
    print('🔐 === INICIANDO PROCESO LOGIN ===');
    setState(() => _isLoading = true);

    try {
      if (_isEmailLogin) {
        print('🔐 Login con email seleccionado');
        // Validar campos para login con email
        if (_identifierController.text.isEmpty || _passwordController.text.isEmpty) {
          print('❌ Campos vacíos detectados');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Por favor completa todos los campos'),
              backgroundColor: Colors.orange,
            ),
          );
          setState(() => _isLoading = false);
          return;
        }
        
        String email = _identifierController.text.trim();
        String password = _passwordController.text;
        
        print('🔐 Intentando login con:');
        print('   - Email: $email');
        print('   - Password length: ${password.length}');
        
        // Login con email y contraseña
        final user = await AuthServiceBypass.instance.loginUser(
          email: email,
          password: password,
        );
        
        print('🔐 Resultado del login: ${user != null ? 'EXITOSO' : 'FALLIDO'}');
        
        if (user != null) {
          print('✅ Usuario logueado exitosamente: ${user.name}');
          // Navegar a la pantalla principal
          Navigator.pushReplacementNamed(context, '/welcome');
        } else {
          print('❌ Login fallido');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Credenciales incorrectas'),
              backgroundColor: Colors.red,
            ),
          );
        }
      } else {
        print('🔐 Login con teléfono seleccionado');
        // Validar campos para login con teléfono
        if (_identifierController.text.isEmpty || _passwordController.text.isEmpty) {
          print('❌ Campos vacíos detectados');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Por favor completa todos los campos'),
              backgroundColor: Colors.orange,
            ),
          );
          setState(() => _isLoading = false);
          return;
        }
        
        String phone = _identifierController.text.trim();
        String password = _passwordController.text;
        
        print('🔐 Intentando login con:');
        print('   - Teléfono: $phone');
        print('   - Password length: ${password.length}');
        
        // Login con teléfono y contraseña
        final user = await AuthServiceBypass.instance.loginUser(
          phone: phone,
          password: password,
        );
        
        print('🔐 Resultado del login: ${user != null ? 'EXITOSO' : 'FALLIDO'}');
        
        if (user != null) {
          print('✅ Usuario logueado exitosamente: ${user.name}');
          // Navegar a la pantalla principal
          Navigator.pushReplacementNamed(context, '/welcome');
        } else {
          print('❌ Login fallido');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Credenciales incorrectas'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    } catch (e) {
      print('❌ Error durante el login: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error durante el login: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      body: SingleChildScrollView(
        child: Center(
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 150,
                  height: 150,
                  child: Image.asset(
                    'assets/images/assets_task_01k3m7yveaebmtdrdnybpe7ngv_1756247471_img_1.webp',
                    fit: BoxFit.contain,
                    errorBuilder: (context, error, stackTrace) {
                      // Fallback si no se encuentra la imagen
                      return Container(
                        width: 120,
                        height: 120,
                        decoration: BoxDecoration(
                          color: Theme.of(context).primaryColor,
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          Icons.person,
                          size: 60,
                          color: Colors.white,
                        ),
                      );
                    },
                  ),
                ),
                SizedBox(height: 30),
                Text(
                  'CubaLink23',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'Inicia sesión en tu cuenta',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey[600],
                  ),
                ),
                SizedBox(height: 40),
                
                // Selector de tipo de login
                Container(
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(25),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: GestureDetector(
                          onTap: () {
                            setState(() {
                              _isEmailLogin = true;
                            });
                          },
                          child: Container(
                            padding: EdgeInsets.symmetric(vertical: 12),
                            decoration: BoxDecoration(
                              color: _isEmailLogin ? Theme.of(context).primaryColor : Colors.transparent,
                              borderRadius: BorderRadius.circular(25),
                            ),
                            child: Text(
                              'Email',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: _isEmailLogin ? Colors.white : Colors.grey[600],
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ),
                      ),
                      Expanded(
                        child: GestureDetector(
                          onTap: () {
                            setState(() {
                              _isEmailLogin = false;
                            });
                          },
                          child: Container(
                            padding: EdgeInsets.symmetric(vertical: 12),
                            decoration: BoxDecoration(
                              color: !_isEmailLogin ? Theme.of(context).primaryColor : Colors.transparent,
                              borderRadius: BorderRadius.circular(25),
                            ),
                            child: Text(
                              'Teléfono',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: !_isEmailLogin ? Colors.white : Colors.grey[600],
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 30),
                
                // Campo de identificador
                TextField(
                  controller: _identifierController,
                  keyboardType: _isEmailLogin ? TextInputType.emailAddress : TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: _isEmailLogin ? 'Email' : 'Teléfono',
                    prefixIcon: Icon(_isEmailLogin ? Icons.email : Icons.phone),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey[50],
                  ),
                ),
                SizedBox(height: 20),
                
                // Campo de contraseña
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'Contraseña',
                    prefixIcon: Icon(Icons.lock),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey[50],
                  ),
                ),
                SizedBox(height: 30),
                
                // Botón de login
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _login,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Theme.of(context).primaryColor,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: _isLoading
                        ? CircularProgressIndicator(color: Colors.white)
                        : Text(
                            'Iniciar Sesión',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                  ),
                ),
                SizedBox(height: 20),
                
                // Enlace a registro
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      '¿No tienes cuenta? ',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                    GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => RegisterScreen()),
                        );
                      },
                      child: Text(
                        'Regístrate',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).primaryColor,
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 20), // Espacio adicional para evitar overflow
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _identifierController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
