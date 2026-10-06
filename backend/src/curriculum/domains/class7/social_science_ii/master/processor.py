from .extractor import Class7SocialscienceiiMasterExtractor
from .normalizer import Class7SocialscienceiiMasterNormalizer
from .validator import Class7SocialscienceiiMasterValidator
from .mapper import Class7SocialscienceiiMasterMapper

class Class7SocialscienceiiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiMasterExtractor.extract(source_path)
        if not Class7SocialscienceiiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7SocialscienceiiMasterNormalizer.normalize(raw)
        return Class7SocialscienceiiMasterMapper.map_to_runtime(normalized)
