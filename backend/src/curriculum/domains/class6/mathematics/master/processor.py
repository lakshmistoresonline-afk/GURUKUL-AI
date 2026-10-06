from .extractor import Class6MathematicsMasterExtractor
from .normalizer import Class6MathematicsMasterNormalizer
from .validator import Class6MathematicsMasterValidator
from .mapper import Class6MathematicsMasterMapper

class Class6MathematicsMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsMasterExtractor.extract(source_path)
        if not Class6MathematicsMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class6MathematicsMasterNormalizer.normalize(raw)
        return Class6MathematicsMasterMapper.map_to_runtime(normalized)
