abstract class Failure {
  final String message;
  Failure(this.message);
}

class ServerFailure extends Failure {
  ServerFailure([String? message]) : super(message ?? "A server error occurred. Please try again.");
}

class NetworkFailure extends Failure {
  NetworkFailure([String? message]) : super(message ?? "No internet connection detected.");
}

class CacheFailure extends Failure {
  CacheFailure([String? message]) : super(message ?? "Unable to retrieve local data.");
}

class AuthFailure extends Failure {
  AuthFailure([String? message]) : super(message ?? "Authentication failed. Please log in again.");
}

class InputFailure extends Failure {
  InputFailure([String? message]) : super(message ?? "Invalid input provided.");
}
