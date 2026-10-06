from .extractor import Class6ScienceQuestionpapersExtractor
from .normalizer import Class6ScienceQuestionpapersNormalizer
from .validator import Class6ScienceQuestionpapersValidator
from .mapper import Class6ScienceQuestionpapersMapper

class Class6ScienceQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceQuestionpapersExtractor.extract(source_path)
        if not Class6ScienceQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class6ScienceQuestionpapersNormalizer.normalize(raw)
        return Class6ScienceQuestionpapersMapper.map_to_runtime(normalized)
