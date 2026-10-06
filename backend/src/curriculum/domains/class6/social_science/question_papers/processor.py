from .extractor import Class6SocialscienceQuestionpapersExtractor
from .normalizer import Class6SocialscienceQuestionpapersNormalizer
from .validator import Class6SocialscienceQuestionpapersValidator
from .mapper import Class6SocialscienceQuestionpapersMapper

class Class6SocialscienceQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceQuestionpapersExtractor.extract(source_path)
        if not Class6SocialscienceQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class6SocialscienceQuestionpapersNormalizer.normalize(raw)
        return Class6SocialscienceQuestionpapersMapper.map_to_runtime(normalized)
