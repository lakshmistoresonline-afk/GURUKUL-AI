import '../../domain/providers/content_provider.dart';
import '../../../../features/curriculum/domain/models/concept_node.dart';

class DikshaProvider implements ContentProvider {
  @override
  String get id => 'diksha';

  @override
  String get name => 'DIKSHA Platform';

  @override
  String get licenseInfo => 'Subject to DIKSHA platform terms';

  @override
  bool get isOfflineSupported => true;

  @override
  Future<ProviderStatus> checkHealth() async {
    return ProviderStatus.active;
  }

  @override
  Future<ConceptNode?> getLesson(String lessonId) async {
    // Search DIKSHA for related content
    return null;
  }

  @override
  Future<List<ConceptNode>> searchContent(String query) async {
    return [];
  }
}
