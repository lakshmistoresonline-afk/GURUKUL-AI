from .extractor import Class7SocialscienceiMasterExtractor
from .normalizer import Class7SocialscienceiMasterNormalizer
from .validator import Class7SocialscienceiMasterValidator
from .mapper import Class7SocialscienceiMasterMapper

class Class7SocialscienceiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiMasterExtractor.extract(source_path)
        if not Class7SocialscienceiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7SocialscienceiMasterNormalizer.normalize(raw)
        return Class7SocialscienceiMasterMapper.map_to_runtime(normalized)
