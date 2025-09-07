import 'package:flutter/material.dart';
import 'package:cubalink23/services/auth_service_bypass.dart';
import 'package:cubalink23/screens/auth/login_screen.dart';
import 'package:cubalink23/screens/auth/register_screen.dart';

class AuthGuardService {
  static AuthGuardService? _instance;
  static AuthGuardService get instance => _instance ??= AuthGuardService._();
  AuthGuardService._();

  /// Verifica si el usuario puede acceder a un servicio
  /// Si no está registrado, muestra un diálogo pidiendo login/registro
  /// Returns true si puede acceder, false si no
  bool checkServiceAccess(BuildContext context, {String? serviceName}) {
    final isLoggedIn = AuthServiceBypass.instance.isSignedIn;
    
    if (isLoggedIn) {
      return true;
    }

    // No está logueado, mostrar diálogo sin await
    _showAuthRequiredDialog(context, serviceName: serviceName);
    return false;
  }

  /// Verifica si el usuario está autenticado
  /// Si no lo está, muestra un diálogo pidiendo login/registro
  /// Returns true si está autenticado, false si no
  Future<bool> requireAuth(BuildContext context, {String? serviceName}) async {
    final isLoggedIn = await AuthServiceBypass.instance.isUserLoggedIn();
    
    if (isLoggedIn) {
      return true;
    }

    // No está logueado, mostrar diálogo
    return await _showAuthRequiredDialog(context, serviceName: serviceName);
  }

  Future<bool> _showAuthRequiredDialog(BuildContext context, {String? serviceName}) async {
    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        title: Row(
          children: [
            Container(
              padding: EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.lock_outline,
                color: Theme.of(context).primaryColor,
                size: 24,
              ),
            ),
            SizedBox(width: 12),
            Expanded(
              child: Text(
                'Registro Requerido',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.onSurface,
                ),
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              serviceName != null
                  ? 'Para usar $serviceName debes crear una cuenta y iniciar sesión.'
                  : 'Para usar este servicio debes crear una cuenta y iniciar sesión.',
              style: TextStyle(
                fontSize: 16,
                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                height: 1.4,
              ),
            ),
            SizedBox(height: 16),
            Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor.withOpacity(0.05),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: Theme.of(context).primaryColor.withOpacity(0.2),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.info_outline,
                    color: Theme.of(context).primaryColor,
                    size: 20,
                  ),
                  SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Es gratis y toma menos de 1 minuto',
                      style: TextStyle(
                        fontSize: 14,
                        color: Theme.of(context).primaryColor,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text(
              'Cancelar',
              style: TextStyle(
                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.6),
              ),
            ),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context, false);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => LoginScreen()),
              );
            },
            child: Text('Iniciar Sesión'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context, false);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => RegisterScreen()),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Theme.of(context).primaryColor,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            child: Text('Registrarse'),
          ),
        ],
      ),
    );

    return result ?? false;
  }

  /// Método específico para Amazon - permite una búsqueda, pero requiere auth para más
  static int _amazonSearchCount = 0;
  
  Future<bool> requireAuthForAmazon(BuildContext context, {required String action}) async {
    final isLoggedIn = await AuthServiceBypass.instance.isUserLoggedIn();
    
    if (isLoggedIn) {
      return true;
    }

    // Si es la primera búsqueda, permitir
    if (action == 'search' && _amazonSearchCount == 0) {
      _amazonSearchCount++;
      return true;
    }

    // Si ya buscó una vez o está intentando agregar al carrito, requerir auth
    return await _showAmazonAuthDialog(context, action: action);
  }

  Future<bool> _showAmazonAuthDialog(BuildContext context, {required String action}) async {
    String message;
    switch (action) {
      case 'search':
        message = 'Ya realizaste una búsqueda. Para continuar navegando en Amazon necesitas crear una cuenta.';
        break;
      case 'add_to_cart':
        message = 'Para agregar productos al carrito necesitas crear una cuenta y iniciar sesión.';
        break;
      default:
        message = 'Para usar esta función de Amazon necesitas crear una cuenta y iniciar sesión.';
    }

    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        title: Row(
          children: [
            Container(
              padding: EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.orange.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.shopping_cart_outlined,
                color: Colors.orange,
                size: 24,
              ),
            ),
            SizedBox(width: 12),
            Expanded(
              child: Text(
                'Amazon Shopping',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.onSurface,
                ),
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              message,
              style: TextStyle(
                fontSize: 16,
                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                height: 1.4,
              ),
            ),
            SizedBox(height: 16),
            Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.green.withOpacity(0.05),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: Colors.green.withOpacity(0.2),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.local_offer_outlined,
                    color: Colors.green,
                    size: 20,
                  ),
                  SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Obtén acceso completo a todas las compras',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.green,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text(
              'Cancelar',
              style: TextStyle(
                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.6),
              ),
            ),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context, false);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => LoginScreen()),
              );
            },
            child: Text('Iniciar Sesión'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context, false);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => RegisterScreen()),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            child: Text('Registrarse'),
          ),
        ],
      ),
    );

    return result ?? false;
  }

  /// Resetea el contador de búsquedas de Amazon (útil para testing)
  void resetAmazonSearchCount() {
    _amazonSearchCount = 0;
  }
}