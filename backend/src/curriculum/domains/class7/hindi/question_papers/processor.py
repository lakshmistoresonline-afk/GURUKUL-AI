from .extractor import Class7HindiQuestionpapersExtractor
from .normalizer import Class7HindiQuestionpapersNormalizer
from .validator import Class7HindiQuestionpapersValidator
from .mapper import Class7HindiQuestionpapersMapper

class Class7HindiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiQuestionpapersExtractor.extract(source_path)
        if not Class7HindiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7HindiQuestionpapersNormalizer.normalize(raw)
        return Class7HindiQuestionpapersMapper.map_to_runtime(normalized)
