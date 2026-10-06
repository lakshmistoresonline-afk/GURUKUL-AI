from .extractor import Class7MathematicsiOverviewExtractor
from .normalizer import Class7MathematicsiOverviewNormalizer
from .validator import Class7MathematicsiOverviewValidator
from .mapper import Class7MathematicsiOverviewMapper

class Class7MathematicsiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiOverviewExtractor.extract(source_path)
        if not Class7MathematicsiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7MathematicsiOverviewNormalizer.normalize(raw)
        return Class7MathematicsiOverviewMapper.map_to_runtime(normalized)
