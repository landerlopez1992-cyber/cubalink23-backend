import 'package:google_sign_in/google_sign_in.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter/foundation.dart';

class GoogleAuthService {
  static final GoogleAuthService _instance = GoogleAuthService._internal();
  factory GoogleAuthService() => _instance;
  GoogleAuthService._internal();

  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile', 'openid'],
    serverClientId: '514921114205-e17864v7035843lebaptp8j9n90to9vl.apps.googleusercontent.com',
  );

  final SupabaseClient _supabase = Supabase.instance.client;

  /// Inicia sesión con Google
  Future<AuthResponse?> signInWithGoogle() async {
    try {
      print('🔐 === INICIANDO LOGIN CON GOOGLE ===');
      
      // Iniciar el proceso de Google Sign-In
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      
      if (googleUser == null) {
        print('❌ Usuario canceló el login con Google');
        return null;
      }

      print('✅ Usuario Google seleccionado: ${googleUser.email}');

      // Obtener los tokens de autenticación
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      
      print('🔍 Debug tokens:');
      print('   - Access Token: ${googleAuth.accessToken != null ? "✅ OK" : "❌ NULL"}');
      print('   - ID Token: ${googleAuth.idToken != null ? "✅ OK" : "❌ NULL"}');
      
      if (googleAuth.accessToken == null || googleAuth.idToken == null) {
        print('❌ No se pudieron obtener los tokens de Google');
        print('   - Access Token: ${googleAuth.accessToken}');
        print('   - ID Token: ${googleAuth.idToken}');
        return null;
      }

      print('✅ Tokens de Google obtenidos exitosamente');

      // Autenticar con Supabase usando los tokens de Google
      final AuthResponse response = await _supabase.auth.signInWithIdToken(
        provider: OAuthProvider.google,
        idToken: googleAuth.idToken!,
        accessToken: googleAuth.accessToken!,
      );

      if (response.user != null) {
        print('✅ Login con Google exitoso:');
        print('   - Usuario ID: ${response.user!.id}');
        print('   - Email: ${response.user!.email}');
        print('   - Nombre: ${response.user!.userMetadata?['full_name']}');
        print('   - Avatar: ${response.user!.userMetadata?['avatar_url']}');
      } else {
        print('❌ Error en la respuesta de Supabase');
      }

      return response;
    } catch (e) {
      print('❌ Error durante login con Google: $e');
      rethrow;
    }
  }

  /// Cierra sesión de Google
  Future<void> signOut() async {
    try {
      print('🔐 === CERRANDO SESIÓN GOOGLE ===');
      
      // Cerrar sesión en Supabase
      await _supabase.auth.signOut();
      
      // Cerrar sesión en Google
      await _googleSignIn.signOut();
      
      print('✅ Sesión cerrada exitosamente');
    } catch (e) {
      print('❌ Error al cerrar sesión: $e');
      rethrow;
    }
  }

  /// Verifica si el usuario está logueado con Google
  Future<bool> isSignedIn() async {
    try {
      return await _googleSignIn.isSignedIn();
    } catch (e) {
      print('❌ Error verificando estado de sesión: $e');
      return false;
    }
  }

  /// Obtiene el usuario actual de Google
  Future<GoogleSignInAccount?> getCurrentUser() async {
    try {
      return _googleSignIn.currentUser;
    } catch (e) {
      print('❌ Error obteniendo usuario actual: $e');
      return null;
    }
  }

  /// Obtiene información del usuario de Supabase
  User? getSupabaseUser() {
    try {
      return _supabase.auth.currentUser;
    } catch (e) {
      print('❌ Error obteniendo usuario de Supabase: $e');
      return null;
    }
  }

  /// Verifica si el usuario está autenticado en Supabase
  bool isSupabaseAuthenticated() {
    try {
      return _supabase.auth.currentUser != null;
    } catch (e) {
      print('❌ Error verificando autenticación de Supabase: $e');
      return false;
    }
  }

  /// Obtiene el stream de cambios de autenticación
  Stream<AuthState> get authStateChanges => _supabase.auth.onAuthStateChange;
}

import 'package:flutter/foundation.dart';

class GoogleAuthService {
  static final GoogleAuthService _instance = GoogleAuthService._internal();
  factory GoogleAuthService() => _instance;
  GoogleAuthService._internal();

  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile', 'openid'],
    serverClientId: '514921114205-e17864v7035843lebaptp8j9n90to9vl.apps.googleusercontent.com',
  );

  final SupabaseClient _supabase = Supabase.instance.client;

  /// Inicia sesión con Google
  Future<AuthResponse?> signInWithGoogle() async {
    try {
      print('🔐 === INICIANDO LOGIN CON GOOGLE ===');
      
      // Iniciar el proceso de Google Sign-In
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      
      if (googleUser == null) {
        print('❌ Usuario canceló el login con Google');
        return null;
      }

      print('✅ Usuario Google seleccionado: ${googleUser.email}');

      // Obtener los tokens de autenticación
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      
      print('🔍 Debug tokens:');
      print('   - Access Token: ${googleAuth.accessToken != null ? "✅ OK" : "❌ NULL"}');
      print('   - ID Token: ${googleAuth.idToken != null ? "✅ OK" : "❌ NULL"}');
      
      if (googleAuth.accessToken == null || googleAuth.idToken == null) {
        print('❌ No se pudieron obtener los tokens de Google');
        print('   - Access Token: ${googleAuth.accessToken}');
        print('   - ID Token: ${googleAuth.idToken}');
        return null;
      }

      print('✅ Tokens de Google obtenidos exitosamente');

      // Autenticar con Supabase usando los tokens de Google
      final AuthResponse response = await _supabase.auth.signInWithIdToken(
        provider: OAuthProvider.google,
        idToken: googleAuth.idToken!,
        accessToken: googleAuth.accessToken!,
      );

      if (response.user != null) {
        print('✅ Login con Google exitoso:');
        print('   - Usuario ID: ${response.user!.id}');
        print('   - Email: ${response.user!.email}');
        print('   - Nombre: ${response.user!.userMetadata?['full_name']}');
        print('   - Avatar: ${response.user!.userMetadata?['avatar_url']}');
      } else {
        print('❌ Error en la respuesta de Supabase');
      }

      return response;
    } catch (e) {
      print('❌ Error durante login con Google: $e');
      rethrow;
    }
  }

  /// Cierra sesión de Google
  Future<void> signOut() async {
    try {
      print('🔐 === CERRANDO SESIÓN GOOGLE ===');
      
      // Cerrar sesión en Supabase
      await _supabase.auth.signOut();
      
      // Cerrar sesión en Google
      await _googleSignIn.signOut();
      
      print('✅ Sesión cerrada exitosamente');
    } catch (e) {
      print('❌ Error al cerrar sesión: $e');
      rethrow;
    }
  }

  /// Verifica si el usuario está logueado con Google
  Future<bool> isSignedIn() async {
    try {
      return await _googleSignIn.isSignedIn();
    } catch (e) {
      print('❌ Error verificando estado de sesión: $e');
      return false;
    }
  }

  /// Obtiene el usuario actual de Google
  Future<GoogleSignInAccount?> getCurrentUser() async {
    try {
      return _googleSignIn.currentUser;
    } catch (e) {
      print('❌ Error obteniendo usuario actual: $e');
      return null;
    }
  }

  /// Obtiene información del usuario de Supabase
  User? getSupabaseUser() {
    try {
      return _supabase.auth.currentUser;
    } catch (e) {
      print('❌ Error obteniendo usuario de Supabase: $e');
      return null;
    }
  }

  /// Verifica si el usuario está autenticado en Supabase
  bool isSupabaseAuthenticated() {
    try {
      return _supabase.auth.currentUser != null;
    } catch (e) {
      print('❌ Error verificando autenticación de Supabase: $e');
      return false;
    }
  }

  /// Obtiene el stream de cambios de autenticación
  Stream<AuthState> get authStateChanges => _supabase.auth.onAuthStateChange;
}
