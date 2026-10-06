from .extractor import Class7MathematicsiMasterExtractor
from .normalizer import Class7MathematicsiMasterNormalizer
from .validator import Class7MathematicsiMasterValidator
from .mapper import Class7MathematicsiMasterMapper

class Class7MathematicsiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiMasterExtractor.extract(source_path)
        if not Class7MathematicsiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7MathematicsiMasterNormalizer.normalize(raw)
        return Class7MathematicsiMasterMapper.map_to_runtime(normalized)
