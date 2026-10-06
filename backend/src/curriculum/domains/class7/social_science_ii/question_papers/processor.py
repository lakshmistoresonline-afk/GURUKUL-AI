from .extractor import Class7SocialscienceiiQuestionpapersExtractor
from .normalizer import Class7SocialscienceiiQuestionpapersNormalizer
from .validator import Class7SocialscienceiiQuestionpapersValidator
from .mapper import Class7SocialscienceiiQuestionpapersMapper

class Class7SocialscienceiiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiQuestionpapersExtractor.extract(source_path)
        if not Class7SocialscienceiiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7SocialscienceiiQuestionpapersNormalizer.normalize(raw)
        return Class7SocialscienceiiQuestionpapersMapper.map_to_runtime(normalized)
