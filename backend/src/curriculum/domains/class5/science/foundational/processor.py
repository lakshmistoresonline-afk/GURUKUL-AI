from .extractor import Class5ScienceFoundationalExtractor
from .normalizer import Class5ScienceFoundationalNormalizer
from .validator import Class5ScienceFoundationalValidator
from .mapper import Class5ScienceFoundationalMapper

class Class5ScienceFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceFoundationalExtractor.extract(source_path)
        if not Class5ScienceFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class5ScienceFoundationalNormalizer.normalize(raw)
        return Class5ScienceFoundationalMapper.map_to_runtime(normalized)
