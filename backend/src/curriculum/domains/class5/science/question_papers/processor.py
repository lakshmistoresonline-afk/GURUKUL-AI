from .extractor import Class5ScienceQuestionpapersExtractor
from .normalizer import Class5ScienceQuestionpapersNormalizer
from .validator import Class5ScienceQuestionpapersValidator
from .mapper import Class5ScienceQuestionpapersMapper

class Class5ScienceQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceQuestionpapersExtractor.extract(source_path)
        if not Class5ScienceQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class5ScienceQuestionpapersNormalizer.normalize(raw)
        return Class5ScienceQuestionpapersMapper.map_to_runtime(normalized)
