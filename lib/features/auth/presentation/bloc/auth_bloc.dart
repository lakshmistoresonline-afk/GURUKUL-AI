import 'package:flutter_bloc/flutter_bloc.dart';
import '../../data/auth_repository.dart';
import '../../domain/models/user_model.dart';

abstract class AuthEvent {}
class AuthUserChanged extends AuthEvent {
  final UserModel? user;
  AuthUserChanged(this.user);
}
class AuthLogoutRequested extends AuthEvent {}
class AuthLoginRequested extends AuthEvent {
  final String email;
  final String password;
  AuthLoginRequested(this.email, this.password);
}


abstract class AuthState {}
class AuthInitial extends AuthState {}
class AuthAuthenticated extends AuthState {
  final UserModel user;
  AuthAuthenticated(this.user);
}
class AuthUnauthenticated extends AuthState {}

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository _authRepository;

  AuthBloc(this._authRepository) : super(AuthAuthenticated(UserModel(
          uid: 'test_student_uid',
          email: 'student@gurukul.ai',
          name: 'Scholar',
          role: UserRole.student,
          classId: '5',
        ))) {
    // Repository listener disabled for testing bypass
    /*
    _authRepository.user.listen((user) {
      if (user != null) {
        // In a real app, fetch UserModel from Firestore here
        // For now, we'll emit a dummy student user
        add(AuthUserChanged(UserModel(
          uid: user.uid,
          email: user.email ?? '',
          name: 'Scholar',
          role: UserRole.student,
          classId: '5',
        )));
      } else {
        add(AuthUserChanged(null));
      }
    });
    */

    on<AuthUserChanged>((event, emit) {
      if (event.user != null) {
        emit(AuthAuthenticated(event.user!));
      } else {
        emit(AuthUnauthenticated());
      }
    });

    on<AuthLogoutRequested>((event, emit) async {
      await _authRepository.signOut();
    });

    on<AuthLoginRequested>((event, emit) async {
      try {
        await _authRepository.signIn(email: event.email, password: event.password);
        // Note: AuthUserChanged will be triggered if the app is listening to authStateChanges
        // In this implementation, we might need to manually fetch the user or rely on the stream.
      } catch (e) {
        emit(AuthUnauthenticated());
      }
    });

    // Note: In a real app, we would listen to authStateChanges and
    // then fetch the UserModel from Firestore.
  }
}
