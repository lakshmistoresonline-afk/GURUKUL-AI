from .extractor import Class6HindiFoundationalExtractor
from .normalizer import Class6HindiFoundationalNormalizer
from .validator import Class6HindiFoundationalValidator
from .mapper import Class6HindiFoundationalMapper

class Class6HindiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiFoundationalExtractor.extract(source_path)
        if not Class6HindiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class6HindiFoundationalNormalizer.normalize(raw)
        return Class6HindiFoundationalMapper.map_to_runtime(normalized)
