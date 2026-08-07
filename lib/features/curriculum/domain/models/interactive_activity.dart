enum ActivityType { dragDrop, matching, sorting, tapReveal, fillBlanks, diagramLabeling }

class InteractiveActivity {
  final String id;
  final String title;
  final String instruction;
  final ActivityType type;
  final Map<String, dynamic> data; // Schema depends on type
  final String? feedbackCorrect;
  final String? feedbackIncorrect;

  const InteractiveActivity({
    required this.id,
    required this.title,
    required this.instruction,
    required this.type,
    required this.data,
    this.feedbackCorrect,
    this.feedbackIncorrect,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'instruction': instruction,
      'type': type.name,
      'data': data,
      'feedbackCorrect': feedbackCorrect,
      'feedbackIncorrect': feedbackIncorrect,
    };
  }

  factory InteractiveActivity.fromMap(Map<String, dynamic> map) {
    return InteractiveActivity(
      id: map['id'] ?? '',
      title: map['title'] ?? '',
      instruction: map['instruction'] ?? '',
      type: ActivityType.values.firstWhere((e) => e.name == map['type'], orElse: () => ActivityType.tapReveal),
      data: Map<String, dynamic>.from(map['data'] ?? {}),
      feedbackCorrect: map['feedbackCorrect'],
      feedbackIncorrect: map['feedbackIncorrect'],
    );
  }
}
