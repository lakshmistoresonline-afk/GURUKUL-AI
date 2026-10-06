from .extractor import Class7ScienceQuizExtractor
from .normalizer import Class7ScienceQuizNormalizer
from .validator import Class7ScienceQuizValidator
from .mapper import Class7ScienceQuizMapper

class Class7ScienceQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceQuizExtractor.extract(source_path)
        if not Class7ScienceQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7ScienceQuizNormalizer.normalize(raw)
        return Class7ScienceQuizMapper.map_to_runtime(normalized)
