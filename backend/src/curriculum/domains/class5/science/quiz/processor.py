from .extractor import Class5ScienceQuizExtractor
from .normalizer import Class5ScienceQuizNormalizer
from .validator import Class5ScienceQuizValidator
from .mapper import Class5ScienceQuizMapper

class Class5ScienceQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceQuizExtractor.extract(source_path)
        if not Class5ScienceQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class5ScienceQuizNormalizer.normalize(raw)
        return Class5ScienceQuizMapper.map_to_runtime(normalized)
