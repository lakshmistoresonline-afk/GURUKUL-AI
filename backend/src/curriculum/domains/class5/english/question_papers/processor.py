from .extractor import Class5EnglishQuestionpapersExtractor
from .normalizer import Class5EnglishQuestionpapersNormalizer
from .validator import Class5EnglishQuestionpapersValidator
from .mapper import Class5EnglishQuestionpapersMapper

class Class5EnglishQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishQuestionpapersExtractor.extract(source_path)
        if not Class5EnglishQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class5EnglishQuestionpapersNormalizer.normalize(raw)
        return Class5EnglishQuestionpapersMapper.map_to_runtime(normalized)
