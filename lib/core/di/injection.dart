import 'package:flutter/foundation.dart';
import 'package:get_it/get_it.dart';
import 'package:logger/logger.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import '../config/app_config.dart';
import '../telemetry/telemetry_service.dart';
import '../telemetry/telemetry_sync_worker.dart';
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

import '../../features/curriculum/data/media/lesson_media_repository.dart';
import '../../features/gamification/domain/services/certificate_service.dart';
import '../../features/questions/data/question_repository.dart';
import '../utils/qr_scanner_service.dart';
import '../../features/content/data/ai_content_factory.dart';
import '../../features/content/domain/services/content_download_service.dart';

final sl = GetIt.instance;

Future<void> init() async {
  debugPrint('DI: Registering Core...');
  // Core
  sl.registerLazySingleton(() => Logger());
  sl.registerLazySingleton(() => SecureStorageService());
  sl.registerLazySingleton(() => LocalStorageService());
  sl.registerLazySingleton(() => ThemeService(sl()));
  sl.registerLazySingleton(() => QrScannerService());

  debugPrint('DI: Getting encryption key...');
  final secureStorage = sl<SecureStorageService>();
  final encryptionKey = await secureStorage.getOrCreateHiveKey();

  debugPrint('DI: Initializing LocalStorage...');
  final storageService = sl<LocalStorageService>();
  await storageService.init(encryptionKey);

  sl.registerLazySingleton(() => TelemetryService(sl(), sl()));
  sl.registerLazySingleton(() => TelemetrySyncWorker(sl(), FirebaseFirestore.instance));
  sl.registerLazySingleton(() => SyncService(sl(), sl(), firestore: FirebaseFirestore.instance));
  sl.registerLazySingleton(() => NotificationService(FirebaseMessaging.instance, sl()));

  debugPrint('DI: Registering Auth...');
  // Features - Auth
  sl.registerLazySingleton(() => AuthRepository(firebaseAuth: FirebaseAuth.instance));
  sl.registerFactory(() => AuthBloc(sl()));

  debugPrint('DI: Initializing Framework...');
  // Features - Curriculum
  sl.registerLazySingleton(() => LessonMediaRepository());
  final frameworkRepo = FrameworkRepository();
  await frameworkRepo.init();
  sl.registerLazySingleton(() => frameworkRepo);
  sl.registerLazySingleton(() => MasteryRepository(firestore: FirebaseFirestore.instance));
  sl.registerLazySingleton(() => RecommendationService());
  sl.registerLazySingleton(() => MasteryService());
  sl.registerLazySingleton(() => SpacedRepetitionService());

  debugPrint('DI: Registering AI...');
  // Features - AI
  sl.registerLazySingleton(() => AiTutorService(AppConfig.geminiApiKey));
  sl.registerLazySingleton(() => AiInsightService(AppConfig.geminiApiKey));
  sl.registerLazySingleton(() => OcrService());
  sl.registerLazySingleton(() => VoiceService());
  sl.registerLazySingleton(() => AiContentFactory(AppConfig.geminiApiKey));

  debugPrint('DI: Registering Gamification...');
  // Features - Gamification
  sl.registerLazySingleton(() => GamificationRepository(firestore: FirebaseFirestore.instance));
  sl.registerLazySingleton(() => MilestoneService());
  sl.registerLazySingleton(() => CertificateService());

  debugPrint('DI: Registering Assessment...');
  // Features - Assessment
  sl.registerLazySingleton(() => QuMLParser());
  sl.registerLazySingleton(() => AssessmentEngine(sl(), sl()));
  sl.registerLazySingleton(() => QuestionRepository());

  debugPrint('DI: Registering Content...');
  sl.registerLazySingleton(() => ContentDownloadService(sl()));

  debugPrint('DI: Registering Reporting...');
  // Features - Reporting
  sl.registerLazySingleton(() => ReportService(sl()));

  debugPrint('DI: Registering Coordinator...');
  // Coordinator
  sl.registerLazySingleton(() => LearningCoordinator(sl(), sl(), sl(), sl()));

  debugPrint('DI: Initialization Complete.');
}
