import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'app.dart';
import 'firebase_options.dart';
import 'core/di/injection.dart' as di;
import 'core/notifications/notification_service.dart';

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

    // Initialize Notifications
    try {
      debugPrint('Initializing Notifications...');
      await di.sl<NotificationService>().init();
      debugPrint('Notifications initialized.');
    } catch (e) {
      debugPrint('Notification initialization failed: $e');
    }
  } catch (e, stack) {
    debugPrint('CRITICAL Initialization error: $e');
    debugPrint('Stack trace: $stack');
  }

  debugPrint('Running App...');
  runApp(const GurukulApp());
}
