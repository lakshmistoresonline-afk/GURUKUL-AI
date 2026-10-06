from .extractor import Class6SocialscienceMasterExtractor
from .normalizer import Class6SocialscienceMasterNormalizer
from .validator import Class6SocialscienceMasterValidator
from .mapper import Class6SocialscienceMasterMapper

class Class6SocialscienceMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceMasterExtractor.extract(source_path)
        if not Class6SocialscienceMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class6SocialscienceMasterNormalizer.normalize(raw)
        return Class6SocialscienceMasterMapper.map_to_runtime(normalized)
