import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../domain/models/study_plan.dart';

class StudyPlannerScreen extends StatefulWidget {
  const StudyPlannerScreen({super.key});

  @override
  State<StudyPlannerScreen> createState() => _StudyPlannerScreenState();
}

class _StudyPlannerScreenState extends State<StudyPlannerScreen> {
  final List<StudyTask> _tasks = [
    StudyTask(id: '1', title: 'Math: Fractions Practice', type: TaskType.practice, estimatedTime: const Duration(minutes: 30), scheduledDate: DateTime.now()),
    StudyTask(id: '2', title: 'Science: Water Cycle', type: TaskType.learn, estimatedTime: const Duration(minutes: 45), scheduledDate: DateTime.now()),
    StudyTask(id: '3', title: 'Hindi: Story Reading', type: TaskType.learn, estimatedTime: const Duration(minutes: 20), scheduledDate: DateTime.now()),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Study Planner'),
        actions: [
          IconButton(onPressed: () {}, icon: const Icon(Icons.settings)),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildWeekCalendar(),
            const SizedBox(height: 32),
            const Text('Tasks for Today', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ..._tasks.map((t) => _buildTaskTile(t)),
            const SizedBox(height: 32),
            _buildAiAdjustmentBanner(),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('Add Task'),
        icon: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildWeekCalendar() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: List.generate(7, (index) {
        final day = DateTime.now().add(Duration(days: index - 3));
        final isToday = index == 3;
        return Column(
          children: [
            Text(['M', 'T', 'W', 'T', 'F', 'S', 'S'][day.weekday - 1], style: const TextStyle(fontSize: 12, color: Colors.grey)),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isToday ? Colors.blue : Colors.transparent,
                shape: BoxShape.circle,
              ),
              child: Text('${day.day}', style: TextStyle(color: isToday ? Colors.white : Colors.black, fontWeight: FontWeight.bold)),
            ),
          ],
        );
      }),
    );
  }

  Widget _buildTaskTile(StudyTask task) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: CheckboxListTile(
        value: task.isCompleted,
        onChanged: (v) {},
        title: Text(task.title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text('${task.type.name.toUpperCase()} • ${task.estimatedTime.inMinutes} mins'),
        secondary: CircleAvatar(
          backgroundColor: _getTaskColor(task.type).withOpacity(0.12),
          child: Icon(_getTaskIcon(task.type), color: _getTaskColor(task.type), size: 20),
        ),
      ),
    );
  }

  Widget _buildAiAdjustmentBanner() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.amber.shade50, borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.amber.shade100)),
      child: const Row(
        children: [
          Icon(Icons.auto_awesome, color: Colors.orange),
          SizedBox(width: 12),
          Expanded(child: Text('AI Tip: "You missed 2 tasks yesterday. I have rescheduled them to spread your workload evenly."', style: TextStyle(fontSize: 13, color: Colors.brown))),
        ],
      ),
    );
  }

  Color _getTaskColor(TaskType type) {
    switch (type) {
      case TaskType.learn: return Colors.green;
      case TaskType.practice: return Colors.blue;
      case TaskType.quiz: return Colors.purple;
      default: return Colors.orange;
    }
  }

  IconData _getTaskIcon(TaskType type) {
    switch (type) {
      case TaskType.learn: return Icons.menu_book;
      case TaskType.practice: return Icons.edit;
      case TaskType.quiz: return Icons.quiz;
      default: return Icons.assignment;
    }
  }
}
