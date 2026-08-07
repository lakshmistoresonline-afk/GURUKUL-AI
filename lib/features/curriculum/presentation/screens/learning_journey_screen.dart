import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/features/ai/presentation/screens/ai_tutor_chat_screen.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/interactive_activity.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/widgets/interactive/animated_teaching_scene.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/widgets/interactive/matching_activity.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/widgets/interactive/tap_reveal_activity.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/widgets/video_player_widget.dart';
import 'package:project_gurukul_ai/core/telemetry/telemetry_service.dart';
import 'package:project_gurukul_ai/core/telemetry/telemetry_constants.dart';

class LearningJourneyScreen extends StatefulWidget {
  final ConceptNode concept;

  const LearningJourneyScreen({super.key, required this.concept});

  @override
  State<LearningJourneyScreen> createState() => _LearningJourneyScreenState();
}

class _LearningJourneyScreenState extends State<LearningJourneyScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;
  final int _totalPages = 10;
  final DateTime _startTime = DateTime.now();

  @override
  void initState() {
    super.initState();
    sl<TelemetryService>().logStart(type: 'CONTENT', id: widget.concept.id);
  }

  @override
  void dispose() {
    final duration = DateTime.now().difference(_startTime);
    sl<TelemetryService>().logEnd(
      type: 'CONTENT',
      id: widget.concept.id,
      summary: {'duration': duration.inSeconds, 'steps_completed': _currentPage},
    );
    _pageController.dispose();
    super.dispose();
  }

  void _nextPage() {
    if (_currentPage < _totalPages - 1) {
      _pageController.nextPage(duration: const Duration(milliseconds: 400), curve: Curves.easeInOut);
    }
  }

  void _previousPage() {
    if (_currentPage > 0) {
      _pageController.previousPage(duration: const Duration(milliseconds: 400), curve: Curves.easeInOut);
    }
  }

  @override
  Widget build(BuildContext context) {
    final themeService = sl<ThemeService>();
    final subjectColor = themeService.getSubjectColor(widget.concept.subject);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text(widget.concept.topic, style: const TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          Center(
            child: Padding(
              padding: const EdgeInsets.only(right: 16.0),
              child: Text(
                'Step ${_currentPage + 1} of $_totalPages',
                style: TextStyle(color: subjectColor, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(6),
          child: LinearProgressIndicator(
            value: (_currentPage + 1) / _totalPages,
            backgroundColor: Colors.grey.shade100,
            valueColor: AlwaysStoppedAnimation(subjectColor),
            minHeight: 6,
          ),
        ),
      ),
      body: PageView(
        controller: _pageController,
        onPageChanged: (page) {
           setState(() => _currentPage = page);
           sl<TelemetryService>().logImpression(pageId: 'learning_step_$page', type: 'CONTENT_PAGE');
        },
        physics: const NeverScrollableScrollPhysics(),
        children: [
          _buildOverviewStep(subjectColor),
          _buildAnimationStep(subjectColor),
          _buildVideoStep(subjectColor),
          _buildLearnStep(subjectColor),
          _buildActivityStep(subjectColor),
          _buildPracticeStep(subjectColor),
          _buildQuizStep(subjectColor),
          _buildRevisionStep(subjectColor),
          _buildAiTutorStep(subjectColor),
          _buildFinishStep(subjectColor),
        ],
      ),
      bottomNavigationBar: _buildBottomBar(subjectColor),
    );
  }

  Widget _buildBottomBar(Color color) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, -4))],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          if (_currentPage > 0)
            OutlinedButton(
              onPressed: _previousPage,
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                side: BorderSide(color: color),
              ),
              child: Text('Previous', style: TextStyle(color: color)),
            )
          else
            const SizedBox.shrink(),
          FilledButton(
            onPressed: _currentPage == _totalPages - 1 ? () => Navigator.pop(context) : _nextPage,
            style: FilledButton.styleFrom(
              backgroundColor: color,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
            ),
            child: Text(_currentPage == _totalPages - 1 ? 'Go to Dashboard' : 'Next Step'),
          ),
        ],
      ),
    );
  }

  Widget _buildOverviewStep(Color color) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Welcome to ${widget.concept.topic}!', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          _buildInfoCard(
            title: 'Real Life Connection',
            content: widget.concept.realLifeConnection.isNotEmpty
                ? widget.concept.realLifeConnection
                : 'Understanding this helps you in everyday life!',
            icon: Icons.lightbulb,
            color: Colors.amber,
          ),
          const SizedBox(height: 24),
          const Text('Learning Objectives:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          ...widget.concept.learningObjectives.map((o) => ListTile(
                leading: Icon(Icons.check_circle, color: color),
                title: Text(o),
                contentPadding: EdgeInsets.zero,
              )),
          const SizedBox(height: 24),
          _buildInfoCard(
            title: 'Estimated Time',
            content: '${widget.concept.estStudyTime.inMinutes} minutes',
            icon: Icons.timer,
            color: Colors.blue,
          ),
        ],
      ),
    );
  }

  Widget _buildAnimationStep(Color color) {
    return AnimatedTeachingScene(
      assetPath: widget.concept.animatedLessonAsset.isNotEmpty
          ? widget.concept.animatedLessonAsset
          : 'assets/lottie/default_lesson.json',
      caption: 'Watch how ${widget.concept.topic} works in this animation!',
    );
  }

  Widget _buildVideoStep(Color color) {
    final isFallback = widget.concept.videoUrl == 'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4';

    return SingleChildScrollView(
      child: Column(
        children: [
          if (isFallback)
            _buildConceptDiagramFallback(color)
          else
            VideoPlayerWidget(
              videoUrl: widget.concept.videoUrl!,
              title: 'Expert Explanation: ${widget.concept.topic}',
            ),
          Padding(
            padding: const EdgeInsets.all(24.0),
            child: Text(
              isFallback
                ? 'We are preparing a special video for this lesson. In the meantime, let\'s look at this concept diagram!'
                : 'Watch this video to get a clear understanding of the core concepts from a teacher.',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey.shade600),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildConceptDiagramFallback(Color color) {
    return Container(
      height: 250,
      width: double.infinity,
      margin: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.2)),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10)],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.auto_awesome_mosaic, size: 64, color: color),
          const SizedBox(height: 20),
          Text(
            'Interactive Concept Map',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color),
          ),
          const SizedBox(height: 8),
          const Text('Tap nodes to learn more'),
        ],
      ),
    );
  }

  Widget _buildLearnStep(Color color) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Choose Your Learning Style', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.grey)),
          const SizedBox(height: 16),
          _buildLearningTabs(color),
          const SizedBox(height: 24),
          _buildVocabularySection(color),
          const SizedBox(height: 24),
          const Text('Hands-on Task', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          ...widget.concept.handsOnActivities.map((a) => Card(
            color: Colors.green.shade50,
            child: ListTile(
              leading: const Icon(Icons.handyman, color: Colors.green),
              title: Text(a),
            ),
          )),
        ],
      ),
    );
  }

  Widget _buildLearningTabs(Color color) {
    return DefaultTabController(
      length: 3,
      child: Column(
        children: [
          TabBar(
            labelColor: color,
            indicatorColor: color,
            tabs: const [
              Tab(text: 'Simple'),
              Tab(text: 'Story'),
              Tab(text: 'Deep Dive'),
            ],
          ),
          const SizedBox(height: 20),
          SizedBox(
            height: 300,
            child: TabBarView(
              children: [
                _buildTextContent(widget.concept.childFriendlyExplanation.isNotEmpty ? widget.concept.childFriendlyExplanation : widget.concept.revisionNotes),
                _buildTextContent(widget.concept.storyBasedExplanation.isNotEmpty ? widget.concept.storyBasedExplanation : 'Once upon a time, we learned about ${widget.concept.topic}...'),
                _buildTextContent(widget.concept.teacherExplanation.isNotEmpty ? widget.concept.teacherExplanation : widget.concept.revisionNotes),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextContent(String text) {
    return SingleChildScrollView(
      child: Text(
        text,
        style: const TextStyle(fontSize: 16, height: 1.6, color: Colors.black87),
      ),
    );
  }

  Widget _buildActivityStep(Color color) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          const Text('Interactive Challenge', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          Expanded(
            child: widget.concept.activities.isNotEmpty
                ? _renderActivity(widget.concept.activities.first)
                : MatchingActivity(
                    pairs: const {'Sun': 'Star', 'Earth': 'Planet', 'Moon': 'Satellite'},
                    onComplete: (v) {},
                  ),
          ),
        ],
      ),
    );
  }

  Widget _renderActivity(InteractiveActivity activity) {
    switch (activity.type) {
      case ActivityType.matching:
        final pairs = Map<String, String>.from(activity.data['pairs'] ?? {});
        return MatchingActivity(pairs: pairs, onComplete: (_) {});
      case ActivityType.tapReveal:
        final items = List<Map<String, String>>.from(activity.data['items'] ?? []);
        return TapRevealActivity(items: items);
      default:
        return const Center(child: Text('Interactive activity coming soon!'));
    }
  }

  Widget _buildPracticeStep(Color color) {
    return ListView.builder(
      padding: const EdgeInsets.all(24),
      itemCount: widget.concept.practiceExercises.length,
      itemBuilder: (context, index) {
        final e = widget.concept.practiceExercises[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Practice ${index + 1}', style: TextStyle(color: color, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                Text(e.question, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                ...e.options.map((o) => RadioListTile(
                  title: Text(o),
                  value: o,
                  groupValue: null,
                  onChanged: (v) {},
                  activeColor: color,
                )),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildQuizStep(Color color) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.quiz, size: 80, color: Colors.blue),
          const SizedBox(height: 24),
          const Text('Ready for the Chapter Quiz?', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          const Text('10 Questions • 5 Minutes', style: TextStyle(color: Colors.grey)),
          const SizedBox(height: 32),
          FilledButton.icon(
            onPressed: () {
               sl<TelemetryService>().logInteract(id: 'start_quiz', type: 'BUTTON', pageId: 'quiz_intro');
            },
            icon: const Icon(Icons.play_arrow),
            label: const Text('Start Quiz'),
            style: FilledButton.styleFrom(backgroundColor: color, padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16)),
          ),
        ],
      ),
    );
  }

  Widget _buildRevisionStep(Color color) {
    return ListView(
      padding: const EdgeInsets.all(24),
      children: [
        const Text('Quick Revision', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        ...widget.concept.flashcards.map((f) => Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            title: Text(f.front, style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: const Text('Tap to see answer'),
            trailing: const Icon(Icons.style),
          ),
        )),
        const SizedBox(height: 24),
        _buildInfoCard(
          title: 'Memory Trick',
          content: widget.concept.commonMistakes.isNotEmpty ? 'Don\'t forget: ${widget.concept.commonMistakes.first}' : 'Review your notes one last time!',
          icon: Icons.psychology,
          color: Colors.purple,
        ),
      ],
    );
  }

  Widget _buildAiTutorStep(Color color) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.smart_toy, size: 80, color: Colors.indigo),
          const SizedBox(height: 24),
          const Text('Any Doubts?', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 40),
            child: Text(
              'Ask Gurukul AI to explain anything again or give more examples!',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey),
            ),
          ),
          const SizedBox(height: 32),
          FilledButton.icon(
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => AiTutorChatScreen(concept: widget.concept)),
            ),
            icon: const Icon(Icons.chat),
            label: const Text('Talk to AI Tutor'),
            style: FilledButton.styleFrom(backgroundColor: Colors.indigo, padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16)),
          ),
        ],
      ),
    );
  }

  Widget _buildFinishStep(Color color) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.emoji_events, size: 100, color: Colors.amber),
          const SizedBox(height: 24),
          const Text('Excellent Job!', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          const Text('You have completed this lesson.', style: TextStyle(fontSize: 18, color: Colors.grey)),
          const SizedBox(height: 32),
          _buildRewardRow(),
        ],
      ),
    );
  }

  Widget _buildRewardRow() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _rewardChip('+50 XP', Icons.stars, Colors.blue),
        const SizedBox(width: 16),
        _rewardChip('+10 Coins', Icons.monetization_on, Colors.amber),
      ],
    );
  }

  Widget _rewardChip(String text, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(20), border: Border.all(color: color.withOpacity(0.5))),
      child: Row(
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(width: 8),
          Text(text, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildInfoCard({required String title, required String content, required IconData icon, required Color color}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: color.withOpacity(0.05), borderRadius: BorderRadius.circular(20), border: Border.all(color: color.withOpacity(0.2))),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 30),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 14)),
                const SizedBox(height: 4),
                Text(content, style: const TextStyle(fontSize: 15, height: 1.4)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildVocabularySection(Color color) {
    if (widget.concept.vocabulary.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('New Words', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: widget.concept.vocabulary.keys.map((w) => Chip(
            label: Text(w),
            backgroundColor: color.withOpacity(0.1),
            side: BorderSide(color: color.withOpacity(0.2)),
          )).toList(),
        ),
      ],
    );
  }
}
