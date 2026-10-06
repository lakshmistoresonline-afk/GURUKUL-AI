from .extractor import Class6EnglishQuestionpapersExtractor
from .normalizer import Class6EnglishQuestionpapersNormalizer
from .validator import Class6EnglishQuestionpapersValidator
from .mapper import Class6EnglishQuestionpapersMapper

class Class6EnglishQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishQuestionpapersExtractor.extract(source_path)
        if not Class6EnglishQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class6EnglishQuestionpapersNormalizer.normalize(raw)
        return Class6EnglishQuestionpapersMapper.map_to_runtime(normalized)
