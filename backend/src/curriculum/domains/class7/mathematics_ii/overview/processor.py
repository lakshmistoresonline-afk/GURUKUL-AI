from .extractor import Class7MathematicsiiOverviewExtractor
from .normalizer import Class7MathematicsiiOverviewNormalizer
from .validator import Class7MathematicsiiOverviewValidator
from .mapper import Class7MathematicsiiOverviewMapper

class Class7MathematicsiiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiOverviewExtractor.extract(source_path)
        if not Class7MathematicsiiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7MathematicsiiOverviewNormalizer.normalize(raw)
        return Class7MathematicsiiOverviewMapper.map_to_runtime(normalized)
