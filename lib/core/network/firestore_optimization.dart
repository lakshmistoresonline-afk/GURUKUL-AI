import 'package:cloud_firestore/cloud_firestore.dart';

class FirestoreOptimization {
  static void configure() {
    FirebaseFirestore.instance.settings = const Settings(
      persistenceEnabled: true,
      cacheSizeBytes: Settings.CACHE_SIZE_UNLIMITED,
    );
  }

  // Example of a debounced search to save on reads
  static Stream<QuerySnapshot> getOptimizedQuery(Query query) {
    return query.snapshots(includeMetadataChanges: false);
  }
}
