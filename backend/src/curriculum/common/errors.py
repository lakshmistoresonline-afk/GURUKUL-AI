class CurriculumError(Exception):
    pass

class ChapterNotFoundError(CurriculumError):
    pass

class SchemaValidationError(CurriculumError):
    pass
