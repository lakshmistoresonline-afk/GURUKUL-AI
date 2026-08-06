import 'package:get_it/get_it.dart';
import 'package:logger/logger.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import '../config/app_config.dart';
import '../telemetry/telemetry_service.dart';
import '../storage/local_storage_service.dart';
import '../storage/secure_storage_service.dart';
import '../theme/theme_service.dart';
import '../offline/sync_service.dart';
import '../notifications/notification_service.dart';
import '../../features/auth/data/auth_repository.dart';
import '../../features/auth/presentation/bloc/auth_bloc.dart';
import '../../features/curriculum/data/framework_repository.dart';
import '../../features/curriculum/data/mastery_repository.dart';
import '../../features/curriculum/domain/services/recommendation_service.dart';
import '../../features/curriculum/domain/services/mastery_service.dart';
import '../../features/curriculum/domain/services/spaced_repetition_service.dart';
import '../../features/ai/data/ai_tutor_service.dart';
import '../../features/ai/data/ai_insight_service.dart';
import '../../features/ai/data/ocr_service.dart';
import '../../features/ai/domain/services/voice_service.dart';
import '../../features/gamification/data/gamification_repository.dart';
import '../../features/gamification/domain/services/milestone_service.dart';
import '../../features/assessment/domain/assessment_engine.dart';
import '../../features/assessment/data/quml_parser.dart';
import '../../features/student/domain/services/learning_coordinator.dart';
import '../../features/parent/domain/services/report_service.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // Core
  sl.registerLazySingleton(() => Logger());
  sl.registerLazySingleton(() => SecureStorageService());
  sl.registerLazySingleton(() => LocalStorageService());
  sl.registerLazySingleton(() => ThemeService(sl()));

  final secureStorage = sl<SecureStorageService>();
  final encryptionKey = await secureStorage.getOrCreateHiveKey();

  final storageService = sl<LocalStorageService>();
  await storageService.init(encryptionKey);

  sl.registerLazySingleton(() => TelemetryService(sl(), sl()));
  sl.registerLazySingleton(() => SyncService(sl(), sl(), firestore: FirebaseFirestore.instance));
  sl.registerLazySingleton(() => NotificationService(FirebaseMessaging.instance, sl()));

  // Features - Auth
  sl.registerLazySingleton(() => AuthRepository(firebaseAuth: FirebaseAuth.instance));
  sl.registerFactory(() => AuthBloc(sl()));

  // Features - Curriculum
  final frameworkRepo = FrameworkRepository();
  await frameworkRepo.init();
  sl.registerLazySingleton(() => frameworkRepo);
  sl.registerLazySingleton(() => MasteryRepository(firestore: FirebaseFirestore.instance));
  sl.registerLazySingleton(() => RecommendationService());
  sl.registerLazySingleton(() => MasteryService());
  sl.registerLazySingleton(() => SpacedRepetitionService());

  // Features - AI
  sl.registerLazySingleton(() => AiTutorService(AppConfig.geminiApiKey));
  sl.registerLazySingleton(() => AiInsightService(AppConfig.geminiApiKey));
  sl.registerLazySingleton(() => OcrService());
  sl.registerLazySingleton(() => VoiceService());

  // Features - Gamification
  sl.registerLazySingleton(() => GamificationRepository(firestore: FirebaseFirestore.instance));
  sl.registerLazySingleton(() => MilestoneService());

  // Features - Assessment
  sl.registerLazySingleton(() => QuMLParser());
  sl.registerLazySingleton(() => AssessmentEngine(sl(), sl()));

  // Features - Reporting
  sl.registerLazySingleton(() => ReportService(sl()));

  // Coordinator
  sl.registerLazySingleton(() => LearningCoordinator(sl(), sl(), sl(), sl()));
}
