from .extractor import Class7HindiQuizExtractor
from .normalizer import Class7HindiQuizNormalizer
from .validator import Class7HindiQuizValidator
from .mapper import Class7HindiQuizMapper

class Class7HindiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiQuizExtractor.extract(source_path)
        if not Class7HindiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7HindiQuizNormalizer.normalize(raw)
        return Class7HindiQuizMapper.map_to_runtime(normalized)
