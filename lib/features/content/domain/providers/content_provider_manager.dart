import 'package:flutter/foundation.dart';
import 'content_provider.dart';
import '../../../../features/curriculum/domain/models/concept_node.dart';
import '../../../../features/curriculum/data/framework_repository.dart';
import '../../../../core/di/injection.dart';

class ContentProviderManager {
  final List<ContentProvider> _providers = [];
  final Map<String, bool> _enabledProviders = {};

  void registerProvider(ContentProvider provider) {
    if (!_providers.any((p) => p.id == provider.id)) {
      _providers.add(provider);
      _enabledProviders[provider.id] = true;
      debugPrint('ContentProvider Registered: ${provider.name}');
    }
  }

  void setProviderEnabled(String providerId, bool enabled) {
    if (_enabledProviders.containsKey(providerId)) {
      _enabledProviders[providerId] = enabled;
    }
  }

  bool isProviderEnabled(String providerId) => _enabledProviders[providerId] ?? false;

  Future<List<ContentProvider>> getActiveProviders() async {
    List<ContentProvider> active = [];
    for (var provider in _providers) {
      if (_enabledProviders[provider.id] == true) {
        final status = await provider.checkHealth();
        if (status == ProviderStatus.active) {
          active.add(provider);
        }
      }
    }
    return active;
  }

  Future<ConceptNode?> getLessonEnriched(String lessonId) async {
    // 1. Try Local Lesson Repository (Primary)
    final localRepo = sl<FrameworkRepository>();
    ConceptNode? node = await localRepo.getConceptNode(lessonId);

    if (node != null) {
      // Logic to enrich from external providers if available
      return node;
    }

    // 2. Search in registered providers
    for (var provider in _providers) {
      if (isProviderEnabled(provider.id)) {
        try {
          final externalNode = await provider.getLesson(lessonId);
          if (externalNode != null) return externalNode;
        } catch (e) {
          debugPrint('Provider ${provider.name} error: $e');
        }
      }
    }

    return null;
  }

  List<ContentProvider> get allProviders => List.unmodifiable(_providers);
}
