import 'dart:async';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:logger/logger.dart';

class NotificationService {
  final FirebaseMessaging _fcm;
  final Logger _logger;

  final _messageController = StreamController<RemoteMessage>.broadcast();
  Stream<RemoteMessage> get messageStream => _messageController.stream;

  NotificationService(this._fcm, this._logger);

  Future<void> init() async {
    try {
      // Request permissions
      NotificationSettings settings = await _fcm.requestPermission(
        alert: true,
        badge: true,
        sound: true,
      );

      if (settings.authorizationStatus == AuthorizationStatus.authorized) {
        _logger.i('User granted permission');
      } else {
        _logger.w('User declined or has not accepted permission');
      }

      // Get token only if permission is granted
      if (settings.authorizationStatus == AuthorizationStatus.authorized) {
        try {
          String? token = await _fcm.getToken(
            vapidKey: 'BGHQ...', // Add your VAPID key here for Web
          );
          _logger.i('FCM Token: $token');
        } catch (e) {
          _logger.w('Could not retrieve FCM token: $e');
        }
      } else {
        _logger.i('Token retrieval skipped: Notifications not authorized.');
      }

      // Handle background messages
      FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

      // Handle foreground messages
      FirebaseMessaging.onMessage.listen((RemoteMessage message) {
        _logger.i('Got a message whilst in the foreground!');
        _messageController.add(message);
      });
    } catch (e) {
      _logger.e('NotificationService init error: $e');
    }
  }

  static Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
    // If you're going to use other Firebase services in the background, such as Firestore,
    // make sure you call `Firebase.initializeApp()` before using other Firebase services.
    print("Handling a background message: ${message.messageId}");
  }
}
