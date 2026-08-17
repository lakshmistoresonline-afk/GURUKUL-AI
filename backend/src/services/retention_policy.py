from datetime import datetime, timedelta
from typing import Dict, Any, List

class RetentionPolicy:
    DEFAULT_INTERVALS = [1, 3, 7, 14, 30, 90] # Days

    @staticmethod
    def calculate_next_review(
        rating: int,
        current_repetitions: int,
        current_easiness: float,
        current_interval: int
    ) -> Dict[str, Any]:
        """
        Calculates new SRS parameters based on the SM-2 algorithm.
        Ratings: 1 (Again/Fail), 2 (Hard), 3 (Good), 4 (Easy)
        """
        new_interval = 0
        new_repetitions = current_repetitions
        new_easiness = current_easiness

        if rating >= 2: # Success
            if current_repetitions == 0:
                new_interval = 1
            elif current_repetitions == 1:
                new_interval = 3 # Slightly more aggressive than standard SM-2 for school curriculum
            else:
                new_interval = round(current_interval * current_easiness)

            new_repetitions += 1
            # Adjust EF: q is quality from 0-5. Map 1-4 to 2-5
            q = rating + 1
            new_easiness = max(1.3, current_easiness + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        else: # Failure
            new_repetitions = 0
            new_interval = 1
            new_easiness = max(1.3, current_easiness - 0.2)

        return {
            "interval": new_interval,
            "repetitions": new_repetitions,
            "easiness_factor": new_easiness,
            "next_review_delta": timedelta(days=new_interval)
        }

    @staticmethod
    def get_retention_stability(repetitions: int, easiness: float) -> str:
        """Categorizes the stability of the memory."""
        if repetitions == 0: return "NEW"
        if repetitions < 3: return "FRAGILE"
        if repetitions < 6: return "STABILIZING"
        return "STABLE"
