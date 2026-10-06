from .extractor import Class6HindiQuestionpapersExtractor
from .normalizer import Class6HindiQuestionpapersNormalizer
from .validator import Class6HindiQuestionpapersValidator
from .mapper import Class6HindiQuestionpapersMapper

class Class6HindiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiQuestionpapersExtractor.extract(source_path)
        if not Class6HindiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class6HindiQuestionpapersNormalizer.normalize(raw)
        return Class6HindiQuestionpapersMapper.map_to_runtime(normalized)
