from .extractor import Class7MathematicsiiMasterExtractor
from .normalizer import Class7MathematicsiiMasterNormalizer
from .validator import Class7MathematicsiiMasterValidator
from .mapper import Class7MathematicsiiMasterMapper

class Class7MathematicsiiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiMasterExtractor.extract(source_path)
        if not Class7MathematicsiiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7MathematicsiiMasterNormalizer.normalize(raw)
        return Class7MathematicsiiMasterMapper.map_to_runtime(normalized)
