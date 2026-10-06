from .extractor import Class6SocialscienceQuizExtractor
from .normalizer import Class6SocialscienceQuizNormalizer
from .validator import Class6SocialscienceQuizValidator
from .mapper import Class6SocialscienceQuizMapper

class Class6SocialscienceQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceQuizExtractor.extract(source_path)
        if not Class6SocialscienceQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class6SocialscienceQuizNormalizer.normalize(raw)
        return Class6SocialscienceQuizMapper.map_to_runtime(normalized)
