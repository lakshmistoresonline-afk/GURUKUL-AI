import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/dashboard_screen.dart';

class MockFrameworkRepository extends FrameworkRepository {
  @override
  Future<List<String>> getSubjects(int classLevel) async {
    return ['Mathematics', 'EVS'];
  }
}

void main() {
  setUp(() {
    final sl = GetIt.instance;
    if (!sl.isRegistered<FrameworkRepository>()) {
      sl.registerLazySingleton<FrameworkRepository>(() => MockFrameworkRepository());
    }
  });

  tearDown(() {
    GetIt.instance.reset();
  });

  testWidgets('Dashboard displays subjects', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(
      home: DashboardScreen(classLevel: 5),
    ));

    expect(find.text('Gurukul AI - Class 5'), findsOneWidget);

    // Wait for FutureBuilder
    await tester.pumpAndSettle();

    expect(find.text('Mathematics'), findsOneWidget);
    expect(find.text('EVS'), findsOneWidget);
  });
}
