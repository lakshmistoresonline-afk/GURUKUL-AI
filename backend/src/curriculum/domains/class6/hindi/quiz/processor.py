from .extractor import Class6HindiQuizExtractor
from .normalizer import Class6HindiQuizNormalizer
from .validator import Class6HindiQuizValidator
from .mapper import Class6HindiQuizMapper

class Class6HindiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiQuizExtractor.extract(source_path)
        if not Class6HindiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class6HindiQuizNormalizer.normalize(raw)
        return Class6HindiQuizMapper.map_to_runtime(normalized)
