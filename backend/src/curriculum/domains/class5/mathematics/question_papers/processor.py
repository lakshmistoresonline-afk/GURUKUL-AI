from .extractor import Class5MathematicsQuestionpapersExtractor
from .normalizer import Class5MathematicsQuestionpapersNormalizer
from .validator import Class5MathematicsQuestionpapersValidator
from .mapper import Class5MathematicsQuestionpapersMapper

class Class5MathematicsQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsQuestionpapersExtractor.extract(source_path)
        if not Class5MathematicsQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class5MathematicsQuestionpapersNormalizer.normalize(raw)
        return Class5MathematicsQuestionpapersMapper.map_to_runtime(normalized)
