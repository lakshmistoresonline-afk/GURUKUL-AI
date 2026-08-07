import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'app.dart';
import 'firebase_options.dart';
import 'core/di/injection.dart' as di;
import 'core/notifications/notification_service.dart';
import 'core/telemetry/telemetry_sync_worker.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  debugPrint('--- App Starting ---');

  try {
    // Initialize Firebase
    debugPrint('Initializing Firebase...');
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
    debugPrint('Firebase initialized.');

    // Initialize Hive
    debugPrint('Initializing Hive...');
    await Hive.initFlutter();
    debugPrint('Hive initialized.');

    // Initialize Dependency Injection
    debugPrint('Initializing DI...');
    await di.init();
    debugPrint('DI initialized.');

    // Initialize Notifications (Non-blocking)
    debugPrint('Starting Notification initialization (Async)...');
    di.sl<NotificationService>().init().then((_) {
      debugPrint('Notifications initialized successfully.');
    }).catchError((e) {
      debugPrint('Notification initialization failed: $e');
    });

    // Initialize Background Sync
    debugPrint('Starting Telemetry Sync Worker...');
    di.sl<TelemetrySyncWorker>().start();

  } catch (e, stack) {
    debugPrint('CRITICAL Initialization error: $e');
    debugPrint('Stack trace: $stack');
  }

  debugPrint('Running App...');
  runApp(const GurukulApp());
}
