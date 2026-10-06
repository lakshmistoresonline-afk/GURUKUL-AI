from .extractor import Class7EnglishQuestionpapersExtractor
from .normalizer import Class7EnglishQuestionpapersNormalizer
from .validator import Class7EnglishQuestionpapersValidator
from .mapper import Class7EnglishQuestionpapersMapper

class Class7EnglishQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishQuestionpapersExtractor.extract(source_path)
        if not Class7EnglishQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7EnglishQuestionpapersNormalizer.normalize(raw)
        return Class7EnglishQuestionpapersMapper.map_to_runtime(normalized)
