import '../../domain/models/media/lesson_media.dart';

class LessonMediaRepository {
  // Hardcoded mapping for demonstration. In production, this would load from a JSON file or API.
  final Map<String, LessonMedia> _mediaMapping = {
    // Mathematics
    'm5_c1': const LessonMedia(
      lessonId: 'm5_c1_media',
      chapterId: 'm5_c1',
      subject: 'Mathematics',
      title: 'The Fish Tale - Large Numbers',
      animationAsset: 'assets/lottie/math_numbers_m5_c1.json',
      videoAsset: 'assets/videos/math_m5_c1.mp4',
      thumbnail: 'assets/images/thumbs/math_m5_c1.png',
      audioNarration: 'assets/audio/math_m5_c1_intro.mp3',
      duration: Duration(minutes: 5),
      license: 'CC BY-NC 4.0',
      source: 'Gurukul AI Original',
    ),
    'm5_c2': const LessonMedia(
      lessonId: 'm5_c2_media',
      chapterId: 'm5_c2',
      subject: 'Mathematics',
      title: 'Shapes and Angles',
      animationAsset: 'assets/lottie/geometry_angles_m5_c2.json',
      videoAsset: 'assets/videos/math_m5_c2.mp4',
    ),
    'm6_c7': const LessonMedia(
      lessonId: 'm6_c7_media',
      chapterId: 'm6_c7',
      subject: 'Mathematics',
      title: 'Fractions',
      animationAsset: 'assets/lottie/math_fractions_m6_c7.json',
      videoAsset: 'assets/videos/math_m6_c7.mp4',
    ),
    'm6_c7_topic1': const LessonMedia(
      lessonId: 'm6_c7_t1_media',
      chapterId: 'm6_c7',
      subject: 'Mathematics',
      title: 'Equivalent Fractions',
      animationAsset: 'assets/lottie/fractions_equivalent.json',
      videoAsset: 'assets/videos/fractions_pizzas.mp4',
    ),

    // Science - Electricity
    's6_c9': const LessonMedia(
      lessonId: 's6_c9_media',
      chapterId: 's6_c9',
      subject: 'Science',
      title: 'Electricity and Circuits',
      animationAsset: 'assets/lottie/science_circuit.json',
      videoAsset: 'assets/videos/science_battery_bulb.mp4',
    ),

    // Science
    's6_c1': const LessonMedia(
      lessonId: 's6_c1_media',
      chapterId: 's6_c1',
      subject: 'Science',
      title: 'Components of Food',
      animationAsset: 'assets/lottie/science_food_s6_c1.json',
      videoAsset: 'assets/videos/science_s6_c1.mp4',
    ),

    // History
    'ss6_h1': const LessonMedia(
      lessonId: 'ss6_h1_media',
      chapterId: 'ss6_h1',
      subject: 'Social Science',
      title: 'What, Where, How and When?',
      animationAsset: 'assets/lottie/history_intro_ss6_h1.json',
      videoAsset: 'assets/videos/history_ss6_h1.mp4',
    ),
  };

  LessonMedia? getMediaForChapter(String chapterId) {
    return _mediaMapping[chapterId];
  }

  /// Generates a fallback lesson media if specific assets are missing.
  LessonMedia generateFallbackMedia(String chapterId, String subject, String title) {
    return LessonMedia(
      lessonId: '${chapterId}_fallback',
      chapterId: chapterId,
      subject: subject,
      title: title,
      // We do NOT use generic assets here.
      // Instead, the UI will handle null assets by showing illustrated walkthroughs.
    );
  }
}
