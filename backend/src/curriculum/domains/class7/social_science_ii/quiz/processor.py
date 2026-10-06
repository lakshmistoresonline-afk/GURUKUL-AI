from .extractor import Class7SocialscienceiiQuizExtractor
from .normalizer import Class7SocialscienceiiQuizNormalizer
from .validator import Class7SocialscienceiiQuizValidator
from .mapper import Class7SocialscienceiiQuizMapper

class Class7SocialscienceiiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiQuizExtractor.extract(source_path)
        if not Class7SocialscienceiiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7SocialscienceiiQuizNormalizer.normalize(raw)
        return Class7SocialscienceiiQuizMapper.map_to_runtime(normalized)
