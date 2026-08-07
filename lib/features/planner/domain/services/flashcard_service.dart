import '../../../curriculum/domain/models/concept_node.dart';
import '../../../curriculum/domain/models/mastery.dart';

class FlashcardService {
  final Map<String, int> _spacedRepetitionData = {}; // CardId -> Interval

  void processReview(String cardId, int quality) {
    // Basic SM-2 quality: 0-5
    if (quality < 3) {
      _spacedRepetitionData[cardId] = 1;
    } else {
      final current = _spacedRepetitionData[cardId] ?? 1;
      _spacedRepetitionData[cardId] = (current * 2).clamp(1, 365);
    }
  }

  List<Flashcard> getCardsForToday(List<Flashcard> allCards) {
    // For MVP, return all. In production, filter based on next review date.
    return allCards;
  }
}
