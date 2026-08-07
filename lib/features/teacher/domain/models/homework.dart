enum HomeworkStatus { assigned, submitted, reviewed }

class Homework {
  final String id;
  final String title;
  final String description;
  final String subject;
  final DateTime dueDate;
  final HomeworkStatus status;
  final String? studentSubmission; // URL or text
  final String? aiFeedback;

  Homework({
    required this.id,
    required this.title,
    required this.description,
    required this.subject,
    required this.dueDate,
    this.status = HomeworkStatus.assigned,
    this.studentSubmission,
    this.aiFeedback,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'subject': subject,
      'dueDate': dueDate.toIso8601String(),
      'status': status.name,
      'studentSubmission': studentSubmission,
      'aiFeedback': aiFeedback,
    };
  }
}
