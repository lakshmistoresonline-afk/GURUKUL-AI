from .extractor import Class6MathematicsQuestionpapersExtractor
from .normalizer import Class6MathematicsQuestionpapersNormalizer
from .validator import Class6MathematicsQuestionpapersValidator
from .mapper import Class6MathematicsQuestionpapersMapper

class Class6MathematicsQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsQuestionpapersExtractor.extract(source_path)
        if not Class6MathematicsQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class6MathematicsQuestionpapersNormalizer.normalize(raw)
        return Class6MathematicsQuestionpapersMapper.map_to_runtime(normalized)
