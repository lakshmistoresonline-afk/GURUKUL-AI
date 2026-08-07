enum TaskType { learn, practice, quiz, revision, homework }

class StudyTask {
  final String id;
  final String title;
  final String? chapterId;
  final String? conceptId;
  final TaskType type;
  final Duration estimatedTime;
  final bool isCompleted;
  final DateTime scheduledDate;

  StudyTask({
    required this.id,
    required this.title,
    this.chapterId,
    this.conceptId,
    required this.type,
    required this.estimatedTime,
    this.isCompleted = false,
    required this.scheduledDate,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'chapterId': chapterId,
      'conceptId': conceptId,
      'type': type.name,
      'estimatedTime': estimatedTime.inMinutes,
      'isCompleted': isCompleted,
      'scheduledDate': scheduledDate.toIso8601String(),
    };
  }
}

class StudyPlan {
  final String id;
  final String studentId;
  final List<StudyTask> tasks;
  final DateTime startDate;
  final DateTime endDate;

  StudyPlan({
    required this.id,
    required this.studentId,
    required this.tasks,
    required this.startDate,
    required this.endDate,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'studentId': studentId,
      'tasks': tasks.map((t) => t.toMap()).toList(),
      'startDate': startDate.toIso8601String(),
      'endDate': endDate.toIso8601String(),
    };
  }
}
