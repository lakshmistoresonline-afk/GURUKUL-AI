from .extractor import Class5MathematicsOverviewExtractor
from .normalizer import Class5MathematicsOverviewNormalizer
from .validator import Class5MathematicsOverviewValidator
from .mapper import Class5MathematicsOverviewMapper

class Class5MathematicsOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsOverviewExtractor.extract(source_path)
        if not Class5MathematicsOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class5MathematicsOverviewNormalizer.normalize(raw)
        return Class5MathematicsOverviewMapper.map_to_runtime(normalized)
