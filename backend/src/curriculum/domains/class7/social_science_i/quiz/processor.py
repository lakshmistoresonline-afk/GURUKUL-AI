from .extractor import Class7SocialscienceiQuizExtractor
from .normalizer import Class7SocialscienceiQuizNormalizer
from .validator import Class7SocialscienceiQuizValidator
from .mapper import Class7SocialscienceiQuizMapper

class Class7SocialscienceiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiQuizExtractor.extract(source_path)
        if not Class7SocialscienceiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7SocialscienceiQuizNormalizer.normalize(raw)
        return Class7SocialscienceiQuizMapper.map_to_runtime(normalized)
