import 'package:cubalink23/models/user.dart' as UserModel;
import 'package:cubalink23/services/supabase_auth_service.dart';

/// Main authentication service that delegates to Supabase
class AuthService {
  static AuthService? _instance;
  static AuthService get instance => _instance ??= AuthService._();
  
  AuthService._();
  
  final SupabaseAuthService _supabaseAuth = SupabaseAuthService.instance;
  
  /// Get current user
  UserModel.User? get currentUser => _supabaseAuth.currentUser;
  
  /// Get user balance
  double get userBalance => _supabaseAuth.userBalance;
  
  /// Check if user is logged in
  Future<bool> isUserLoggedIn() async {
    return await _supabaseAuth.isUserLoggedIn();
  }
  
  /// Register user
  Future<UserModel.User?> registerUser({
    required String email,
    required String password,
    required String name,
    required String phone,
    required String country,
    required String city,
  }) async {
    return await _supabaseAuth.registerUser(
      email: email,
      password: password,
      name: name,
      phone: phone,
      country: country,
      city: city,
    );
  }
  
  /// Login user
  Future<UserModel.User?> loginUser({
    required String email,
    required String password,
  }) async {
    return await _supabaseAuth.loginUser(
      email: email,
      password: password,
    );
  }
  
  /// Logout user
  Future<void> logoutUser() async {
    await _supabaseAuth.logoutUser();
  }
  
  /// Check if user is suspended
  Future<bool> isUserSuspended(String userId) async {
    return await _supabaseAuth.isUserSuspended(userId);
  }
  
  /// Update user balance
  Future<void> updateUserBalance(double newBalance) async {
    await _supabaseAuth.updateUserBalance(newBalance);
  }
  
  /// Load current user data
  Future<void> loadCurrentUserData() async {
    await _supabaseAuth.loadCurrentUserData();
  }
  
  /// Change password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    await _supabaseAuth.changePassword(
      currentPassword: currentPassword,
      newPassword: newPassword,
    );
  }
  
  /// Update user profile
  Future<void> updateUserProfile({
    String? name,
    String? phone,
    String? address,
    String? country,
    String? city,
  }) async {
    await _supabaseAuth.updateUserProfile(
      name: name,
      phone: phone,
      address: address,
      country: country,
      city: city,
    );
  }
  
  /// Sign out (alias for logout)
  Future<void> signOut() async {
    await _supabaseAuth.signOut();
  }
  
  /// Notify that user has used a service
  Future<void> notifyServiceUsed() async {
    await _supabaseAuth.notifyServiceUsed();
  }
  
  // Constructor factory for compatibility
  factory AuthService() => instance;
}