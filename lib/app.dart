import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'core/di/injection.dart';
import 'features/auth/presentation/bloc/auth_bloc.dart';
import 'features/student/presentation/screens/dashboard_screen.dart';
import 'features/auth/presentation/screens/login_screen.dart';

class GurukulApp extends StatelessWidget {
  const GurukulApp({super.key});

  @override
  Widget build(BuildContext context) {
    try {
      return BlocProvider(
        create: (context) => sl<AuthBloc>(),
        child: MaterialApp(
          title: 'Gurukul AI',
          debugShowCheckedModeBanner: false,
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: const Color(0xFF2563EB),
              surface: const Color(0xFFF8FAFC),
              brightness: Brightness.light,
            ),
            useMaterial3: true,
            cardTheme: CardThemeData(
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
                side: BorderSide(color: Colors.grey.shade200),
              ),
            ),
            appBarTheme: const AppBarTheme(
              centerTitle: false,
              backgroundColor: Color(0xFFF8FAFC),
              elevation: 0,
            ),
          ),
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: const Color(0xFF2563EB),
              brightness: Brightness.dark,
            ),
            useMaterial3: true,
            cardTheme: const CardThemeData(
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.all(Radius.circular(20)),
              ),
            ),
          ),
          themeMode: ThemeMode.system,
          home: BlocBuilder<AuthBloc, AuthState>(
            builder: (context, state) {
              if (state is AuthAuthenticated) {
                return DashboardScreen(classLevel: state.user.classId != null ? int.parse(state.user.classId!) : 5);
              }
              return const LoginScreen();
            },
          ),
        ),
      );
    } catch (e) {
      return MaterialApp(
        home: Scaffold(
          body: Center(
            child: Text('App Crash: $e'),
          ),
        ),
      );
    }
  }
}
