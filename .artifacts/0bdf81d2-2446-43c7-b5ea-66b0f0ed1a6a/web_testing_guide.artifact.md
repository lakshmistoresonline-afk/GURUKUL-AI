# Steps to Test Project Gurukul AI in Browser

Follow these steps to run and test the application in your web browser.

## 1. Prerequisites
- **Flutter SDK**: Ensure you have Flutter installed and configured in your system PATH.
- **Google Chrome**: Recommended browser for testing.
- **Firebase Web Config**: You will need your Firebase project's web configuration (API Key, Auth Domain, etc.).

## 2. Command Sequence
Run the following commands in your terminal at the project root:

```bash
# 1. Fetch dependencies
flutter pub get

# 2. Run the application in Chrome
flutter run -d chrome --dart-define=GEMINI_API_KEY=your_actual_key_here
```

## 3. Web Configuration (Important)
Since Firebase Web requires explicit options, you may need to update `lib/main.dart` with your project's `DefaultFirebaseOptions`.

### Adding Firebase Web Options
If you encounter a "Firebase initialization error" on web, run:
```bash
flutterfire configure
```
This will generate `lib/firebase_options.dart`. Then, update `lib/main.dart`:

```dart
// lib/main.dart snippet
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  // ... rest of the code
}
```

## 4. Testing Features in Browser
Once the app is running in Chrome, you can verify:
- [x] **Dashboard Navigation**: Subject selection and chapter lists.
- [x] **Pedagogical Hub**: The new `TopicDetailScreen` (Learn/Practice/Review tabs).
- [x] **AI Tutor**: Socratic chat sessions (requires valid Gemini API key).
- [x] **Responsive Layout**: Resize the browser to test the Material 3 adaptive UI.

> [!NOTE]
> Some mobile-specific features like **OCR (Textbook Scanning)** and **Hardware-specific Voice STT** may behave differently in a browser environment compared to a physical Android device.
