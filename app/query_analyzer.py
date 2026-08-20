import re


# ============================================================
# KNOWN BIKE NAMES
# ============================================================

BIKE_NAMES = [
    "Bullet 650",
    "Hunter 350",
    "Classic 350",
    "Goan Classic 350",
    "Bullet 350",
    "Meteor 350",
    "Scram 440",
    "Himalayan 450",
    "Guerrilla 450",
    "Bear 650",
    "Interceptor 650",
    "Continental GT 650",
    "Super Meteor 650",
    "Shotgun 650",
    "Classic 650",
]


# ============================================================
# ATTRIBUTE PATTERNS
# ============================================================

ATTRIBUTE_PATTERNS = {

    "engine": [
        "engine",
        "engine capacity",
        "engine displacement",
        "displacement",
        "cc",
        "cubic capacity",
    ],

    "power": [
        "power",
        "maximum power",
        "max power",
        "bhp",
        "ps",
    ],

    "torque": [
        "torque",
        "maximum torque",
        "max torque",
    ],

    "mileage": [
        "mileage",
        "fuel consumption",
        "fuel economy",
        "km/l",
        "kmpl",
        "kilometres per litre",
        "kilometers per litre",
        "distance per litre",
    ],

    "top_speed": [
        "top speed",
        "maximum speed",
        "max speed",
        "fastest",
        "speed",
    ],

    "fuel_tank": [
        "fuel tank",
        "tank capacity",
        "fuel capacity",
        "tank size",
        "tank",
        "how much fuel",
        "hold the most fuel",
        "carry the most fuel",
        "carry most fuel",
        "hold most fuel",
        "biggest tank",
        "largest tank",
    ],

    "weight": [
        "weight",
        "kerb weight",
        "kerb",
        "heavy",
        "heaviest",
        "lightest",
    ],

    "seat_height": [
        "seat height",
        "seat",
        "tallest seat",
        "highest seat",
        "lowest seat",
    ],

    "ground_clearance": [
        "ground clearance",
        "clearance",
    ],

    "wheelbase": [
        "wheelbase",
    ],

    "suspension": [
        "suspension",
    ],

    "brakes": [
        "brakes",
        "braking",
        "abs",
        "braking system",
    ],

    "tyres": [
        "tyres",
        "tires",
        "tyre",
        "tire",
    ],

    "wheels": [
        "wheels",
        "wheel",
    ],

    "colours": [
        "colour",
        "colours",
        "color",
        "colors",
    ],

    "gearbox": [
        "gearbox",
        "gears",
        "gear",
    ],

    "clutch": [
        "clutch",
    ],
}


# ============================================================
# CATEGORY / CLASSIFICATION PATTERNS
# ============================================================

CATEGORY_PATTERNS = {

    "adventure_tourer": [
        "adventure tourer",
        "adventure touring",
        "adventure motorcycle",
        "adventure bike",
        "adventure",
    ],

    "cruiser": [
        "cruiser",
        "cruisers",
    ],

    "heritage": [
        "heritage",
        "heritage bikes",
        "heritage motorcycles",
    ],

    "roadster": [
        "roadster",
        "roadsters",
    ],

    "scrambler": [
        "scrambler",
        "scramblers",
    ],

    "adventure_crossover": [
        "adventure crossover",
        "crossover",
    ],

    "supermoto_custom": [
        "supermoto",
        "custom",
    ],

    "pure_sport_cafe_racer": [
        "cafe racer",
        "café racer",
        "pure sport",
    ],

    "heritage_bobber": [
        "bobber",
    ],
}


# ============================================================
# COMPARISON WORDS
# ============================================================

COMPARISON_WORDS = [
    "compare",
    "comparison",
    "difference",
    "differences",
    "versus",
    "vs",
    "better",
    "which is better",
]


# ============================================================
# MAXIMUM / HIGHEST OPERATION
# ============================================================

MAX_WORDS = [
    "largest",
    "biggest",
    "highest",
    "maximum",
    "max",
    "greatest",
    "most",
    "fastest",
    "heaviest",
    "tallest"
]


# ============================================================
# MINIMUM / LOWEST OPERATION
# ============================================================

MIN_WORDS = [
    "smallest",
    "lowest",
    "minimum",
    "min",
    "least",
    "lightest",
    "slowest",
]


# ============================================================
# GLOBAL / AGGREGATE WORDS
# ============================================================

AGGREGATE_WORDS = [
    "average",
    "mean",
    "how many",
    "count",
    "all bikes",
    "every bike",
    "each bike",
    "top",
    "bottom",
]


# ============================================================
# ENTITY DETECTION
# ============================================================

def detect_entities(question: str):
    """
    Detect known Royal Enfield bike names in the question.
    """

    question_lower = question.lower()

    found = []

    for bike in BIKE_NAMES:

        if bike.lower() in question_lower:
            found.append(bike)

    return found


# ============================================================
# ATTRIBUTE DETECTION
# ============================================================

def detect_attribute(question: str):
    """
    Detect the attribute the user is asking about.
    """

    question_lower = question.lower()

    for attribute, patterns in ATTRIBUTE_PATTERNS.items():

        for pattern in patterns:

            if pattern in question_lower:
                return attribute

    return None


# ============================================================
# CATEGORY DETECTION
# ============================================================

def detect_category(question: str):
    """
    Detect motorcycle category/classification.

    Example:

        Which bike is the adventure tourer?

    returns:

        adventure_tourer
    """

    question_lower = question.lower()

    for category, patterns in CATEGORY_PATTERNS.items():

        for pattern in patterns:

            if pattern in question_lower:
                return category

    return None


# ============================================================
# OPERATION DETECTION
# ============================================================

def detect_operation(question: str):
    """
    Detect what operation the question requires.
    """

    question_lower = question.lower()

    # --------------------------------------------------------
    # MAX
    # --------------------------------------------------------

    for word in MAX_WORDS:

        if word in question_lower:
            return "MAX"

    # --------------------------------------------------------
    # MIN
    # --------------------------------------------------------

    for word in MIN_WORDS:

        if word in question_lower:
            return "MIN"

    # --------------------------------------------------------
    # AGGREGATE
    # --------------------------------------------------------

    for word in AGGREGATE_WORDS:

        if word in question_lower:

            if word in ["average", "mean"]:
                return "AVERAGE"

            if word in ["how many", "count"]:
                return "COUNT"

            if word in ["top", "bottom"]:
                return "RANK"

            return "ALL"

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    for word in COMPARISON_WORDS:

        if word in question_lower:
            return "COMPARE"

    # --------------------------------------------------------
    # CATEGORY LOOKUP
    # --------------------------------------------------------

    category = detect_category(question)

    if category:
        return "CATEGORY"

    # --------------------------------------------------------
    # NORMAL GET
    # --------------------------------------------------------

    return "GET"


# ============================================================
# QUERY TYPE DETECTION
# ============================================================

def detect_query_type(
    entities,
    operation,
    category
):
    """
    Determine the overall query type.

    ENTITY
        Specific bike question.

    COMPARISON
        Comparing multiple bikes.

    GLOBAL
        Requires looking across all bikes.

    GENERAL
        Normal semantic retrieval.
    """

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    if operation == "COMPARE":
        return "COMPARISON"

    if len(entities) >= 2:
        return "COMPARISON"

    # --------------------------------------------------------
    # GLOBAL
    # --------------------------------------------------------

    if operation in [
        "MAX",
        "MIN",
        "AVERAGE",
        "COUNT",
        "RANK",
        "ALL",
        "CATEGORY",
    ]:
        return "GLOBAL"

    # --------------------------------------------------------
    # ENTITY
    # --------------------------------------------------------

    if len(entities) == 1:
        return "ENTITY"

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    return "GENERAL"


# ============================================================
# MAIN QUERY ANALYZER
# ============================================================

def analyze_query(question: str):

    entities = detect_entities(question)

    attribute = detect_attribute(question)

    category = detect_category(question)

    operation = detect_operation(question)

    query_type = detect_query_type(
        entities=entities,
        operation=operation,
        category=category
    )

    return {
        "question": question,
        "query_type": query_type,
        "entities": entities,
        "attribute": attribute,
        "category": category,
        "operation": operation,
    }