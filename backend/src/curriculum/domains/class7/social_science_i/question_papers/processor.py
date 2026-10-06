from .extractor import Class7SocialscienceiQuestionpapersExtractor
from .normalizer import Class7SocialscienceiQuestionpapersNormalizer
from .validator import Class7SocialscienceiQuestionpapersValidator
from .mapper import Class7SocialscienceiQuestionpapersMapper

class Class7SocialscienceiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiQuestionpapersExtractor.extract(source_path)
        if not Class7SocialscienceiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7SocialscienceiQuestionpapersNormalizer.normalize(raw)
        return Class7SocialscienceiQuestionpapersMapper.map_to_runtime(normalized)
