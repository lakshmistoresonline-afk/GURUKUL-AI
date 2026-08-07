import '../../domain/providers/content_provider.dart';
import '../../../../features/curriculum/domain/models/concept_node.dart';

class NcertEpathshalaProvider implements ContentProvider {
  @override
  String get id => 'ncert_epathshala';

  @override
  String get name => 'NCERT ePathshala';

  @override
  String get licenseInfo => 'CC BY-NC-SA (Non-Commercial, ShareAlike)';

  @override
  bool get isOfflineSupported => true;

  @override
  Future<ProviderStatus> checkHealth() async {
    // Mock health check
    return ProviderStatus.active;
  }

  @override
  Future<ConceptNode?> getLesson(String lessonId) async {
    // Logic to fetch from ePathshala API/Scraper
    return null;
  }

  @override
  Future<List<ConceptNode>> searchContent(String query) async {
    return [];
  }
}
