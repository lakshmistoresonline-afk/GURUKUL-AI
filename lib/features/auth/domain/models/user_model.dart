enum UserRole { student, parent, teacher, admin }

class UserModel {
  final String uid;
  final String email;
  final String name;
  final UserRole role;
  final String? classId; // Relevant for students
  final List<String>? childrenIds; // Relevant for parents
  final int xp;
  final List<String> badges;

  UserModel({
    required this.uid,
    required this.email,
    required this.name,
    required this.role,
    this.classId,
    this.childrenIds,
    this.xp = 0,
    this.badges = const [],
  });

  Map<String, dynamic> toMap() {
    return {
      'uid': uid,
      'email': email,
      'name': name,
      'role': role.name,
      'classId': classId,
      'childrenIds': childrenIds,
      'xp': xp,
      'badges': badges,
    };
  }

  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      uid: map['uid'] ?? '',
      email: map['email'] ?? '',
      name: map['name'] ?? '',
      role: UserRole.values.firstWhere((e) => e.name == map['role'], orElse: () => UserRole.student),
      classId: map['classId'],
      childrenIds: map['childrenIds'] != null ? List<String>.from(map['childrenIds']) : null,
      xp: map['xp'] ?? 0,
      badges: List<String>.from(map['badges'] ?? []),
    );
  }
}
