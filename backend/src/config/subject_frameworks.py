"""
Subject-Aware Complete Content Framework for Gurukul AI.
Defines subject-specific generation instructions and content types.
"""

SUBJECT_FRAMEWORKS = {
    "english": {
        "description": "Language and Literature focused on vocabulary, grammar, and literary analysis.",
        "content_types": ["VOCABULARY", "GRAMMAR", "IDIOMS", "PHRASES", "COMPREHENSION", "LITERATURE", "POETRY", "WRITING"],
        "prompt_instructions": (
            "For English/Languages, generate:\n"
            "- VOCABULARY: new words, meanings, synonyms, antonyms, usage, word families, prefixes/suffixes.\n"
            "- GRAMMAR: concepts, rules, examples, exceptions, common mistakes, exercises.\n"
            "- IDIOMS & PHRASES: meanings and contextual usage with examples.\n"
            "- COMPREHENSION: main ideas, supporting details, inference, and vocabulary in context.\n"
            "- LITERATURE/POETRY: characters, setting, plot, themes, literary devices, stanza meanings, imagery, and tone."
        )
    },
    "mathematics": {
        "description": "Logic and calculation focused on concepts, formulas, and worked examples.",
        "content_types": ["CONCEPTS", "DEFINITIONS", "FORMULAS", "THEOREMS", "PROPERTIES", "METHODS", "WORKED_EXAMPLES", "PROBLEM_TYPES", "NUMERICAL_PRACTICE", "GRAPHS", "UNITS"],
        "prompt_instructions": (
            "For Mathematics, do NOT use 'vocabulary' as the primary category. Generate:\n"
            "- CONCEPTS & DEFINITIONS: intuitive and formal explanations, exact terminology.\n"
            "- FORMULAS & THEOREMS: variable meanings, units, conditions, statement, and proof/applications.\n"
            "- PROPERTIES & RULES: mathematical properties, rules, and relationships.\n"
            "- METHODS: procedures, algorithms, and step-by-step 'how to solve'.\n"
            "- WORKED EXAMPLES: problem, given info, required result, method, step-by-step solution, verification, and common mistakes.\n"
            "- NUMERICAL PRACTICE: Categorized by difficulty: Easy, Medium, Hard, Application, HOTS.\n"
            "- GRAPHS & UNITS: interpretation, trends, conversions, and dimensional understanding."
        )
    },
    "science": {
        "description": "Inquiry-based learning focused on processes, laws, and experiments.",
        "content_types": ["CONCEPTS", "DEFINITIONS", "PROCESSES", "LAWS", "PRINCIPLES", "EXPERIMENTS", "DIAGRAMS", "APPLICATIONS", "TERMINOLOGY", "CAUSE_AND_EFFECT", "COMPARISONS"],
        "prompt_instructions": (
            "For Science, generate:\n"
            "- CONCEPTS & DEFINITIONS: simple and detailed explanations of terms and relationships.\n"
            "- PROCESSES: step-by-step sequences, conditions, and outcomes.\n"
            "- LAWS & PRINCIPLES: statements, meanings, conditions, and practical applications.\n"
            "- EXPERIMENTS: objective, materials, procedure, observations, result, conclusion, precautions, and explanation.\n"
            "- DIAGRAMS: identify parts, labels, functions, and interpretation.\n"
            "- APPLICATIONS: real-world and practical examples.\n"
            "- CAUSE & EFFECT / COMPARISONS: mechanism, similarities, and differences."
        )
    },
    "social_science": {
        "description": "Contextual learning focused on facts, events, and spatial relationships.",
        "content_types": ["FACTS", "CONCEPTS", "EVENTS", "DATES", "PEOPLE", "PLACES", "CAUSES", "EFFECTS", "COMPARISONS", "MAPS", "TIMELINES"],
        "prompt_instructions": (
            "For Social Science, generate:\n"
            "- FACTS & CONCEPTS: important factual information and explanations.\n"
            "- EVENTS & DATES: event description, significance, and associated dates.\n"
            "- PEOPLE & PLACES: important individuals (roles/contributions) and places (significance).\n"
            "- CAUSES & EFFECTS: contributing factors, immediate/long-term consequences.\n"
            "- MAPS & TIMELINES: spatial relationships, map interpretation, and chronological sequence."
        )
    },
    "history": {
        "parent": "social_science",
        "content_types": ["EVENTS", "TIMELINE", "PEOPLE", "PLACES", "CAUSES", "CONSEQUENCES", "IMPORTANT_TERMS", "COMPARISONS", "SOURCE_ANALYSIS", "CHRONOLOGY"],
        "prompt_instructions": (
            "For History, prioritize:\n"
            "- EVENTS & TIMELINE: chronological order, context, and significance.\n"
            "- PEOPLE & PLACES: individual roles and location significance.\n"
            "- CAUSES & CONSEQUENCES: immediate and underlying causes, long-term consequences.\n"
            "- SOURCE ANALYSIS: evidence, perspective, and historical significance."
        )
    },
    "geography": {
        "parent": "social_science",
        "content_types": ["CONCEPTS", "DEFINITIONS", "PROCESSES", "PLACES", "MAPS", "DATA", "CASE_STUDIES", "CAUSE_EFFECT", "COMPARISONS", "DIAGRAMS"],
        "prompt_instructions": (
            "For Geography, generate:\n"
            "- CONCEPTS & PROCESSES: natural and human processes, step-by-step explanations.\n"
            "- PLACES & MAPS: locations, geographical significance, and map interpretation.\n"
            "- DATA: interpretation of tables, statistics, and graphs.\n"
            "- CASE STUDIES: background, issue, process, outcome, and significance.\n"
            "- DIAGRAMS: cross-sections, cycles (e.g. water cycle), and geographic models."
        )
    },
    "civics": {
        "parent": "social_science",
        "content_types": ["INSTITUTIONS", "CONCEPTS", "DEFINITIONS", "RIGHTS", "DUTIES", "PROCESSES", "EXAMPLES", "COMPARISONS", "CASE_BASED_LEARNING"],
        "prompt_instructions": (
            "For Civics/Political Science, generate:\n"
            "- INSTITUTIONS: roles, structure, and relationships.\n"
            "- CONCEPTS & DEFINITIONS: political/civic concepts and precise meanings.\n"
            "- RIGHTS & DUTIES: meaning, examples, and protections.\n"
            "- PROCESSES: elections, decision-making, and governance procedures."
        )
    },
    "economics": {
        "parent": "social_science",
        "content_types": ["CONCEPTS", "DEFINITIONS", "PRINCIPLES", "INDICATORS", "CAUSES", "EFFECTS", "EXAMPLES", "APPLICATIONS", "COMPARISONS", "DATA_INTERPRETATION"],
        "prompt_instructions": (
            "For Economics, generate:\n"
            "- CONCEPTS & DEFINITIONS: economic concepts, intuitive and formal explanations.\n"
            "- PRINCIPLES & INDICATORS: explanation, application, and interpretation.\n"
            "- DATA INTERPRETATION: analysis of tables, graphs, and trends."
        )
    },
    "computer_science": {
        "description": "Technical and algorithmic focused on syntax and logic.",
        "content_types": ["TERMINOLOGY", "CONCEPTS", "COMMANDS", "SYNTAX", "ALGORITHMS", "PROCESSES", "EXAMPLES", "APPLICATIONS", "DEBUGGING", "PROBLEM_SOLVING"],
        "prompt_instructions": (
            "For Computer Science, generate:\n"
            "- TERMINOLOGY & CONCEPTS: technical terms and conceptual explanations.\n"
            "- COMMANDS & SYNTAX: syntax rules, parameters, examples, and common errors.\n"
            "- ALGORITHMS: inputs, outputs, steps, and pseudocode.\n"
            "- DEBUGGING: identify error, explain it, and provide corrected version.\n"
            "- PROBLEM SOLVING: approach, algorithm, and implementation results."
        )
    },
    "biology": {
        "parent": "science",
        "content_types": ["TERMINOLOGY", "CONCEPTS", "STRUCTURES", "FUNCTIONS", "PROCESSES", "CLASSIFICATIONS", "DIAGRAMS", "COMPARISONS", "EXPERIMENTS", "APPLICATIONS", "CAUSE_EFFECT"],
        "prompt_instructions": (
            "For Biology, generate:\n"
            "- TERMINOLOGY & CONCEPTS: biological terms and detailed explanations.\n"
            "- STRUCTURES & FUNCTIONS: parts, organization, mechanism, and relationships.\n"
            "- PROCESSES & CLASSIFICATIONS: step-by-step biological processes, characteristics, and distinguishing features.\n"
            "- DIAGRAMS: parts, labels, functions, and interpretation."
        )
    },
    "physics": {
        "parent": "science",
        "content_types": ["CONCEPTS", "LAWS", "FORMULAS", "PRINCIPLES", "DERIVATIONS", "UNITS", "GRAPHS", "APPLICATIONS", "NUMERICALS"],
        "prompt_instructions": (
            "For Physics, generate:\n"
            "- LAWS & PRINCIPLES: meanings, conditions, and applications.\n"
            "- FORMULAS: variables, units, conditions, when to use, and examples.\n"
            "- DERIVATIONS: assumptions, intermediate steps, and final result.\n"
            "- NUMERICALS: Given, Required, Formula, Substitution, Calculation, Answer, Unit, Verification, and Common Mistake.\n"
            "- GRAPHS: interpretation, slope, trends, and relationships."
        )
    },
    "chemistry": {
        "parent": "science",
        "content_types": ["TERMINOLOGY", "CONCEPTS", "REACTIONS", "EQUATIONS", "PROPERTIES", "LAWS", "PROCESSES", "APPLICATIONS", "EXPERIMENTS", "COMPARISONS", "NUMERICALS"],
        "prompt_instructions": (
            "For Chemistry, generate:\n"
            "- REACTIONS & EQUATIONS: reactants, products, conditions, observations, and balanced equations.\n"
            "- PROPERTIES & LAWS: physical and chemical properties and their explanations.\n"
            "- EXPERIMENTS: objective, materials, procedure, observation, result, and precautions."
        )
    }
}

def get_framework_for_subject(subject_name: str) -> dict:
    """Returns the framework for a subject, falling back to a generic one if not found."""
    if not subject_name:
        return {}

    s_lower = subject_name.lower().strip()

    # Direct match
    if s_lower in SUBJECT_FRAMEWORKS:
        return SUBJECT_FRAMEWORKS[s_lower]

    # Heuristic matches
    if "comp" in s_lower or "it" == s_lower or "ict" in s_lower:
        return SUBJECT_FRAMEWORKS["computer_science"]
    if "math" in s_lower:
        return SUBJECT_FRAMEWORKS["mathematics"]
    if "science" in s_lower:
        if "biology" in s_lower: return SUBJECT_FRAMEWORKS["biology"]
        if "physics" in s_lower: return SUBJECT_FRAMEWORKS["physics"]
        if "chemistry" in s_lower: return SUBJECT_FRAMEWORKS["chemistry"]
        return SUBJECT_FRAMEWORKS["science"]
    if "social" in s_lower or "history" in s_lower or "geography" in s_lower or "civics" in s_lower or "politic" in s_lower or "econom" in s_lower:
        if "history" in s_lower: return SUBJECT_FRAMEWORKS["history"]
        if "geography" in s_lower: return SUBJECT_FRAMEWORKS["geography"]
        if "civics" in s_lower or "politic" in s_lower: return SUBJECT_FRAMEWORKS["civics"]
        if "econom" in s_lower: return SUBJECT_FRAMEWORKS["economics"]
        return SUBJECT_FRAMEWORKS["social_science"]
    if "english" in s_lower or "hindi" in s_lower or "lang" in s_lower or "sanskrit" in s_lower:
        return SUBJECT_FRAMEWORKS["english"]
    if "comp" in s_lower or "it" == s_lower or "ict" in s_lower:
        return SUBJECT_FRAMEWORKS["computer_science"]

    return {}
