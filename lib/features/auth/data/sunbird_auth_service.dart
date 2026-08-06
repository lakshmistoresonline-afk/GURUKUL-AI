import 'package:firebase_auth/firebase_auth.dart';

abstract class ISunbirdAuthService {
  Future<UserCredential?> login(String username, String password);
  Future<void> logout();
  Future<Map<String, dynamic>> getUserProfile(String userId);
}

class SunbirdAuthService implements ISunbirdAuthService {
  final FirebaseAuth _firebaseAuth;

  SunbirdAuthService({FirebaseAuth? firebaseAuth})
      : _firebaseAuth = firebaseAuth ?? FirebaseAuth.instance;

  @override
  Future<UserCredential?> login(String username, String password) async {
    // In a real implementation, this would call Sunbird Lern API:
    // POST /api/auth/v1/login
    // For now, we wrap Firebase Auth to maintain the contract
    try {
      return await _firebaseAuth.signInWithEmailAndPassword(
        email: '$username@gurukul.ai',
        password: password
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> logout() async {
    await _firebaseAuth.signOut();
  }

  @override
  Future<Map<String, dynamic>> getUserProfile(String userId) async {
    // Call GET /api/user/v1/read/:userId
    return {
      'userId': userId,
      'firstName': 'Student',
      'lastName': 'User',
      'organisations': ['Gurukul_AI_Org'],
    };
  }
}
