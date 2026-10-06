from .extractor import Class5HindiQuestionpapersExtractor
from .normalizer import Class5HindiQuestionpapersNormalizer
from .validator import Class5HindiQuestionpapersValidator
from .mapper import Class5HindiQuestionpapersMapper

class Class5HindiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiQuestionpapersExtractor.extract(source_path)
        if not Class5HindiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class5HindiQuestionpapersNormalizer.normalize(raw)
        return Class5HindiQuestionpapersMapper.map_to_runtime(normalized)
