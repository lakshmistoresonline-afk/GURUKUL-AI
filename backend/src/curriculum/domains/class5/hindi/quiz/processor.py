from .extractor import Class5HindiQuizExtractor
from .normalizer import Class5HindiQuizNormalizer
from .validator import Class5HindiQuizValidator
from .mapper import Class5HindiQuizMapper

class Class5HindiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiQuizExtractor.extract(source_path)
        if not Class5HindiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class5HindiQuizNormalizer.normalize(raw)
        return Class5HindiQuizMapper.map_to_runtime(normalized)
