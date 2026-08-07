import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/dashboard_screen.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/core/telemetry/telemetry_service.dart';
import 'package:project_gurukul_ai/core/storage/local_storage_service.dart';
import 'package:logger/logger.dart';
import 'package:project_gurukul_ai/features/curriculum/data/mastery_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/mastery.dart';
import 'package:project_gurukul_ai/features/ai/domain/services/voice_service.dart';
import 'package:project_gurukul_ai/features/ai/data/ai_tutor_service.dart';
import 'package:project_gurukul_ai/features/gamification/data/gamification_repository.dart';
import 'package:project_gurukul_ai/features/gamification/domain/services/daily_challenge_service.dart';

// Simple Mocks to satisfy Dependency Injection and Provider requirements
class MockFrameworkRepository extends FrameworkRepository {
  @override
  Future<List<String>> getSubjects(int classLevel) async => ['Mathematics'];
  @override
  Future<void> init() async {}
}

class MockThemeService implements ThemeService {
  @override
  Color getSubjectColor(String subject) => Colors.blue;
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockTelemetryService implements TelemetryService {
  @override
  void logImpression({required String pageId, required String type}) {}
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockLocalStorageService implements LocalStorageService {
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockLogger implements Logger {
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockMasteryRepository implements MasteryRepository {
  @override
  Future<List<Mastery>> getStudentMastery(String studentId) async => [];
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockVoiceService implements VoiceService {
  @override
  Future<bool> init() async => true;
  @override
  Future<void> startListening(Function(String) onResult) async {}
  @override
  Future<void> stopListening() async {}
  @override
  Future<void> speak(String text) async {}
  @override
  Future<void> stopSpeaking() async {}
}

class MockAiTutorService implements AiTutorService {
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockGamificationRepository implements GamificationRepository {
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class MockDailyChallengeService implements DailyChallengeService {
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClient implements HttpClient {
  @override
  bool autoUncompress = true;
  @override
  Duration? connectionTimeout;
  @override
  Duration idleTimeout = const Duration(seconds: 15);
  @override
  int? maxConnectionsPerHost;
  @override
  String? userAgent;

  @override
  Future<HttpClientRequest> getUrl(Uri url) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> openUrl(String method, Uri url) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> get(String host, int port, String path) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> post(String host, int port, String path) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> put(String host, int port, String path) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> delete(String host, int port, String path) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> patch(String host, int port, String path) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> head(String host, int port, String path) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> postUrl(Uri url) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> putUrl(Uri url) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> deleteUrl(Uri url) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> patchUrl(Uri url) async => _MockHttpClientRequest();
  @override
  Future<HttpClientRequest> headUrl(Uri url) async => _MockHttpClientRequest();

  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClientRequest implements HttpClientRequest {
  @override
  Encoding encoding = utf8;
  @override
  bool followRedirects = true;
  @override
  int maxRedirects = 5;
  @override
  bool persistentConnection = true;
  @override
  final HttpHeaders headers = _MockHttpHeaders();

  @override
  void add(List<int> data) {}
  @override
  Future<HttpClientResponse> close() async => _MockHttpClientResponse();
  @override
  Future<HttpClientResponse> get done async => _MockHttpClientResponse();

  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClientResponse extends Stream<List<int>> implements HttpClientResponse {
  @override
  final HttpHeaders headers = _MockHttpHeaders();
  @override
  final int statusCode = 200;
  @override
  final String reasonPhrase = "OK";
  @override
  final int contentLength = _transparentPixel.length;
  @override
  HttpClientResponseCompressionState get compressionState => HttpClientResponseCompressionState.notCompressed;

  static const List<int> _transparentPixel = [
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
    0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
    0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
    0x42, 0x60, 0x82
  ];

  @override
  StreamSubscription<List<int>> listen(void Function(List<int> event)? onData,
      {Function? onError, void Function()? onDone, bool? cancelOnError}) {
    return Stream<List<int>>.fromIterable([_transparentPixel]).listen(onData,
        onError: onError, onDone: onDone, cancelOnError: cancelOnError);
  }

  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpHeaders implements HttpHeaders {
  @override
  List<String>? operator [](String name) => [];
  @override
  void add(String name, Object value, {bool preserveHeaderCase = false}) {}
  @override
  void set(String name, Object value, {bool preserveHeaderCase = false}) {}
  @override
  ContentType? get contentType => ContentType.binary;
  @override
  noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
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
    sl.registerLazySingleton<LocalStorageService>(() => MockLocalStorageService());
    sl.registerLazySingleton<Logger>(() => MockLogger());
    sl.registerLazySingleton<MasteryRepository>(() => MockMasteryRepository());
    sl.registerLazySingleton<VoiceService>(() => MockVoiceService());
    sl.registerLazySingleton<AiTutorService>(() => MockAiTutorService());
    sl.registerLazySingleton<GamificationRepository>(() => MockGamificationRepository());
    sl.registerLazySingleton<DailyChallengeService>(() => MockDailyChallengeService());
  });

  tearDown(() {
    GetIt.instance.reset();
  });

  testWidgets('Dashboard Screen Smoke Test', (WidgetTester tester) async {
    // Set a large viewport to avoid overflows in test environment
    tester.view.physicalSize = const Size(1200, 2000);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    // This test ensures the dashboard can be pumped without crashing due to missing dependencies
    await HttpOverrides.runZoned(() async {
      await tester.pumpWidget(MaterialApp(
        home: BlocProvider<AuthBloc>(
          create: (_) => FakeAuthBloc(),
          child: const DashboardScreen(classLevel: 5),
        ),
      ));
    }, createHttpClient: (_) => _MockHttpClient());

    await tester.pump(const Duration(seconds: 1));
    expect(find.byType(DashboardScreen), findsOneWidget);
  });
}
