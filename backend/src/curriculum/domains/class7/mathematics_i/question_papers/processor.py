from .extractor import Class7MathematicsiQuestionpapersExtractor
from .normalizer import Class7MathematicsiQuestionpapersNormalizer
from .validator import Class7MathematicsiQuestionpapersValidator
from .mapper import Class7MathematicsiQuestionpapersMapper

class Class7MathematicsiQuestionpapersProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiQuestionpapersExtractor.extract(source_path)
        if not Class7MathematicsiQuestionpapersValidator.validate(raw):
            raise ValueError("Validation failed for Questionpapers")
        normalized = Class7MathematicsiQuestionpapersNormalizer.normalize(raw)
        return Class7MathematicsiQuestionpapersMapper.map_to_runtime(normalized)
