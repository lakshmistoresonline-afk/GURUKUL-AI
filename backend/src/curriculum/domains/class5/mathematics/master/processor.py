from .extractor import Class5MathematicsMasterExtractor
from .normalizer import Class5MathematicsMasterNormalizer
from .validator import Class5MathematicsMasterValidator
from .mapper import Class5MathematicsMasterMapper

class Class5MathematicsMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsMasterExtractor.extract(source_path)
        if not Class5MathematicsMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class5MathematicsMasterNormalizer.normalize(raw)
        return Class5MathematicsMasterMapper.map_to_runtime(normalized)
