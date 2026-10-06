from .extractor import Class6ScienceFoundationalExtractor
from .normalizer import Class6ScienceFoundationalNormalizer
from .validator import Class6ScienceFoundationalValidator
from .mapper import Class6ScienceFoundationalMapper

class Class6ScienceFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceFoundationalExtractor.extract(source_path)
        if not Class6ScienceFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class6ScienceFoundationalNormalizer.normalize(raw)
        return Class6ScienceFoundationalMapper.map_to_runtime(normalized)
