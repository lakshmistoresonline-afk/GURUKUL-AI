import '../../../../features/curriculum/domain/models/concept_node.dart';

enum ProviderStatus { active, inactive, authenticationRequired, healthCheckFailed }

abstract class ContentProvider {
  String get id;
  String get name;
  String get licenseInfo;
  bool get isOfflineSupported;

  Future<ProviderStatus> checkHealth();
  Future<List<ConceptNode>> searchContent(String query);
  Future<ConceptNode?> getLesson(String lessonId);
}
