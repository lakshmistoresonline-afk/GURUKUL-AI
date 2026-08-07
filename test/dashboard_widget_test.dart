import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/dashboard_screen.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/core/telemetry/telemetry_service.dart';
import 'package:project_gurukul_ai/features/auth/data/auth_repository.dart';

// Simple Mocks to satisfy Dependency Injection and Provider requirements
class MockFrameworkRepository extends FrameworkRepository {
  @override
  Future<List<String>> getSubjects(int classLevel) async => ['Mathematics'];
  @override
  Future<void> init() async {}
}

class MockThemeService extends ThemeService {
  MockThemeService() : super(GetIt.instance());
  @override
  Color getSubjectColor(String subject) => Colors.blue;
}

class MockTelemetryService extends TelemetryService {
  MockTelemetryService() : super(GetIt.instance(), GetIt.instance());
  @override
  void logImpression({required String pageId, required String type}) {}
}

class FakeAuthBloc extends Bloc<AuthEvent, AuthState> implements AuthBloc {
  FakeAuthBloc() : super(AuthInitial());
}

void main() {
  setUp(() {
    final sl = GetIt.instance;
    sl.registerLazySingleton<FrameworkRepository>(() => MockFrameworkRepository());
    sl.registerLazySingleton<ThemeService>(() => MockThemeService());
    sl.registerLazySingleton<TelemetryService>(() => MockTelemetryService());
  });

  tearDown(() {
    GetIt.instance.reset();
  });

  testWidgets('Dashboard Screen Smoke Test', (WidgetTester tester) async {
    // This test ensures the dashboard can be pumped without crashing due to missing dependencies
    await tester.pumpWidget(MaterialApp(
      home: BlocProvider<AuthBloc>(
        create: (_) => FakeAuthBloc(),
        child: const DashboardScreen(classLevel: 5),
      ),
    ));

    expect(find.byType(DashboardScreen), findsOneWidget);
  });
}
