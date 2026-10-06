from .extractor import Class6SocialscienceFoundationalExtractor
from .normalizer import Class6SocialscienceFoundationalNormalizer
from .validator import Class6SocialscienceFoundationalValidator
from .mapper import Class6SocialscienceFoundationalMapper

class Class6SocialscienceFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceFoundationalExtractor.extract(source_path)
        if not Class6SocialscienceFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class6SocialscienceFoundationalNormalizer.normalize(raw)
        return Class6SocialscienceFoundationalMapper.map_to_runtime(normalized)
