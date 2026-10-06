from .extractor import Class7MathematicsiQuizExtractor
from .normalizer import Class7MathematicsiQuizNormalizer
from .validator import Class7MathematicsiQuizValidator
from .mapper import Class7MathematicsiQuizMapper

class Class7MathematicsiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiQuizExtractor.extract(source_path)
        if not Class7MathematicsiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7MathematicsiQuizNormalizer.normalize(raw)
        return Class7MathematicsiQuizMapper.map_to_runtime(normalized)
