enum ActivityType { matching, tapReveal, sorting, sequence, fillBlanks }

class InteractiveActivity {
  final String id;
  final ActivityType type;
  final Map<String, dynamic> data;
  final String instruction;
  final String title;

  const InteractiveActivity({
    required this.id,
    required this.type,
    required this.data,
    this.instruction = '',
    this.title = '',
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'type': type.name,
      'data': data,
      'instruction': instruction,
      'title': title,
    };
  }

  factory InteractiveActivity.fromMap(Map<String, dynamic> map) {
    return InteractiveActivity(
      id: map['id'] ?? '',
      type: ActivityType.values.firstWhere((e) => e.name == map['type'], orElse: () => ActivityType.matching),
      data: Map<String, dynamic>.from(map['data'] ?? {}),
      instruction: map['instruction'] ?? '',
      title: map['title'] ?? '',
    );
  }
}
