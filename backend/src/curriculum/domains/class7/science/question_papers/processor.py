from .extractor import Class7ScienceQuestionpapersExtractor
from .normalizer import Class7ScienceQuestionpapersNormalizer
from .validator import Class7ScienceQuestionpapersValidator
from .mapper import Class7ScienceQuestionpapersMapper

class Class7ScienceQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceQuestionpapersExtractor.extract(source_path)
        if not Class7ScienceQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7ScienceQuestionpapersNormalizer.normalize(raw)
        return Class7ScienceQuestionpapersMapper.map_to_runtime(normalized)
