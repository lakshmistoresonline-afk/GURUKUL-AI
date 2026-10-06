from .extractor import Class6MathematicsOverviewExtractor
from .normalizer import Class6MathematicsOverviewNormalizer
from .validator import Class6MathematicsOverviewValidator
from .mapper import Class6MathematicsOverviewMapper

class Class6MathematicsOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsOverviewExtractor.extract(source_path)
        if not Class6MathematicsOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class6MathematicsOverviewNormalizer.normalize(raw)
        return Class6MathematicsOverviewMapper.map_to_runtime(normalized)
