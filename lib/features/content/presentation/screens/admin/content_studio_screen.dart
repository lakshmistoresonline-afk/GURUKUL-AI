import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'lesson_editor_screen.dart';
import 'import_wizard_screen.dart';
import 'ai_content_factory_screen.dart';

class ContentStudioScreen extends StatefulWidget {
  const ContentStudioScreen({super.key});

  @override
  State<ContentStudioScreen> createState() => _ContentStudioScreenState();
}

class _ContentStudioScreenState extends State<ContentStudioScreen> {
  String _selectedClass = 'Class 6';
  String _selectedSubject = 'Science';
  Map<String, dynamic>? _healthReport;
  bool _isScanning = false;

  @override
  void initState() {
    super.initState();
    _scanRepository();
  }

  Future<void> _scanRepository() async {
    setState(() => _isScanning = true);
    final report = await sl<FrameworkRepository>().getRepositoryHealth();
    setState(() {
      _healthReport = report;
      _isScanning = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: const Text('Gurukul Content Studio'),
        actions: [
          IconButton(
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AiContentFactoryScreen())),
            icon: const Icon(Icons.factory_outlined),
            tooltip: 'AI Content Factory',
          ),
          IconButton(
            onPressed: _scanRepository,
            icon: Icon(_isScanning ? Icons.sync : Icons.scanner),
            tooltip: 'Scan Repository',
          ),
          IconButton(
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ImportWizardScreen())),
            icon: const Icon(Icons.auto_awesome),
            tooltip: 'Import Wizard',
          ),
        ],
      ),
      body: Column(
        children: [
          if (_healthReport != null) _buildHealthBanner(),
          _buildFilterBar(),
          Expanded(child: _buildLessonGrid()),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('New Manual Lesson'),
        icon: const Icon(Icons.add),
        backgroundColor: DesignSystem.primary,
        foregroundColor: Colors.white,
      ),
    );
  }

  Widget _buildHealthBanner() {
    final score = _healthReport!['healthScore'];
    final color = score > 80 ? Colors.green : (score > 50 ? Colors.orange : Colors.red);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      color: color.withValues(alpha: 0.1),
      child: Row(
        children: [
          Icon(Icons.health_and_safety, color: color, size: 20),
          const SizedBox(width: 8),
          Text(
            'Repository Health: $score%',
            style: TextStyle(color: color, fontWeight: FontWeight.bold),
          ),
          const Spacer(),
          Text(
            '${_healthReport!['totalLessons']} Lessons Scanned',
            style: DesignSystem.bodySmall,
          ),
          if (_healthReport!['missingMedia'] > 0) ...[
            const SizedBox(width: 16),
            Icon(Icons.warning_amber, color: Colors.orange, size: 16),
            Text(
              ' ${_healthReport!['missingMedia']} Missing Media',
              style: const TextStyle(fontSize: 10, color: Colors.orange),
            ),
          ]
        ],
      ),
    );
  }

  Widget _buildFilterBar() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: BoxDecoration(
        color: DesignSystem.surface,
        border: Border(bottom: BorderSide(color: Colors.grey.shade200)),
      ),
      child: Row(
        children: [
          Expanded(
            child: DropdownButtonFormField<String>(
              initialValue: _selectedClass,
              items: ['Class 5', 'Class 6', 'Class 7', 'Class 8'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (v) => setState(() => _selectedClass = v!),
              decoration: const InputDecoration(labelText: 'Grade', border: OutlineInputBorder()),
            ),
          ),
          const SizedBox(width: DesignSystem.spacingMd),
          Expanded(
            child: DropdownButtonFormField<String>(
              initialValue: _selectedSubject,
              items: ['Mathematics', 'Science', 'EVS', 'English', 'Hindi'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (v) => setState(() => _selectedSubject = v!),
              decoration: const InputDecoration(labelText: 'Subject', border: OutlineInputBorder()),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLessonGrid() {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: sl<FrameworkRepository>().getChapters(int.parse(_selectedClass.split(' ')[1]), _selectedSubject),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
        final chapters = snapshot.data ?? [];
        return GridView.builder(
          padding: const EdgeInsets.all(DesignSystem.spacingMd),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: DesignSystem.spacingMd,
            mainAxisSpacing: DesignSystem.spacingMd,
            childAspectRatio: 0.75,
          ),
          itemCount: chapters.length,
          itemBuilder: (context, index) {
            final c = chapters[index];
            return _buildLessonCard(c);
          },
        );
      },
    );
  }

  Widget _buildLessonCard(Map<String, dynamic> chapter) {
    return Card(
      child: InkWell(
        onTap: () {
          Navigator.push(context, MaterialPageRoute(builder: (_) => LessonEditorScreen(chapterId: chapter['id'])));
        },
        child: Padding(
          padding: const EdgeInsets.all(DesignSystem.spacingMd),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Icon(Icons.article_outlined, color: DesignSystem.primary),
              const SizedBox(height: DesignSystem.spacingMd),
              Text(
                chapter['title'],
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const Spacer(),
              _statusChip('Structure', true),
              _statusChip('Multimedia', false),
              _statusChip('Assessment', true),
              const SizedBox(height: DesignSystem.spacingMd),
              const Text('Overall Readiness', style: TextStyle(fontSize: 10, color: Colors.grey)),
              const SizedBox(height: 4),
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: const LinearProgressIndicator(value: 0.6, minHeight: 6),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _statusChip(String label, bool complete) {
    return Padding(
      padding: const EdgeInsets.only(top: 4.0),
      child: Row(
        children: [
          Icon(complete ? Icons.check_circle : Icons.circle_outlined, size: 10, color: complete ? Colors.green : Colors.grey),
          const SizedBox(width: 4),
          Text(label, style: const TextStyle(fontSize: 10, color: DesignSystem.textSecondary)),
        ],
      ),
    );
  }
}
