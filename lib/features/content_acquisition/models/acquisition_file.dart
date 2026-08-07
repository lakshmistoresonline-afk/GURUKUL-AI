class AcquisitionFile {
  final String path;
  final String name;
  final String extension;
  final int size;
  final int classLevel;
  final String subject;
  final int chapterIndex;
  final String? checksum;

  AcquisitionFile({
    required this.path,
    required this.name,
    required this.extension,
    required this.size,
    required this.classLevel,
    required this.subject,
    required this.chapterIndex,
    this.checksum,
  });

  Map<String, dynamic> toJson() {
    return {
      'path': path,
      'name': name,
      'extension': extension,
      'size': size,
      'classLevel': classLevel,
      'subject': subject,
      'chapterIndex': chapterIndex,
      'checksum': checksum,
    };
  }

  factory AcquisitionFile.fromJson(Map<String, dynamic> json) {
    return AcquisitionFile(
      path: json['path'] as String,
      name: json['name'] as String,
      extension: json['extension'] as String,
      size: json['size'] as int,
      classLevel: json['classLevel'] as int,
      subject: json['subject'] as String,
      chapterIndex: json['chapterIndex'] as int,
      checksum: json['checksum'] as String?,
    );
  }
}
