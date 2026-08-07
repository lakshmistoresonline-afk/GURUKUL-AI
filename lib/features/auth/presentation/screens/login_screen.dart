import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import '../bloc/auth_bloc.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isPasswordVisible = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter both email and password')),
      );
      return;
    }

    context.read<AuthBloc>().add(AuthLoginRequested(email, password));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(DesignSystem.spacingLg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 60),
              const Center(
                child: Hero(
                  tag: 'app_logo',
                  child: Icon(Icons.school, size: 80, color: DesignSystem.primary),
                ),
              ),
              const SizedBox(height: 24),
              Text(
                'Welcome Back!',
                textAlign: TextAlign.center,
                style: DesignSystem.h1.copyWith(fontSize: 32),
              ),
              const SizedBox(height: 8),
              Text(
                'Sign in to continue your learning journey',
                textAlign: TextAlign.center,
                style: DesignSystem.bodySmall.copyWith(fontSize: 16),
              ),
              const SizedBox(height: 48),
              TextField(
                controller: _emailController,
                decoration: InputDecoration(
                  labelText: 'Email Address',
                  prefixIcon: const Icon(Icons.email_outlined),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                  ),
                ),
                keyboardType: TextInputType.emailAddress,
              ),
              const SizedBox(height: 20),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Password',
                  prefixIcon: const Icon(Icons.lock_outline),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _isPasswordVisible ? Icons.visibility_off : Icons.visibility,
                    ),
                    onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible),
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                  ),
                ),
                obscureText: !_isPasswordVisible,
              ),
              const SizedBox(height: 12),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: () {},
                  child: const Text('Forgot Password?'),
                ),
              ),
              const SizedBox(height: 32),
              FilledButton(
                onPressed: _handleLogin,
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                  ),
                ),
                child: const Text('Login', style: TextStyle(fontSize: 18)),
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text("Don't have an account?"),
                  TextButton(
                    onPressed: () {},
                    child: const Text('Sign Up', style: TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
