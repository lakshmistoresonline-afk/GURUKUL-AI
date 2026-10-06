from .extractor import Class7MathematicsiiQuestionpapersExtractor
from .normalizer import Class7MathematicsiiQuestionpapersNormalizer
from .validator import Class7MathematicsiiQuestionpapersValidator
from .mapper import Class7MathematicsiiQuestionpapersMapper

class Class7MathematicsiiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiQuestionpapersExtractor.extract(source_path)
        if not Class7MathematicsiiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7MathematicsiiQuestionpapersNormalizer.normalize(raw)
        return Class7MathematicsiiQuestionpapersMapper.map_to_runtime(normalized)
