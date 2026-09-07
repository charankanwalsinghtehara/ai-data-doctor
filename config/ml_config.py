RANDOM_STATE = 42


# =========================
# TRAIN / TEST SPLIT
# =========================

TEST_SIZE = 0.2


# =========================
# CLASSIFICATION
# =========================

CLASSIFICATION_MODELS = [

    "logistic_regression",

    "random_forest",

    "decision_tree"
]


# =========================
# REGRESSION
# =========================

REGRESSION_MODELS = [

    "linear_regression",

    "random_forest_regressor",

    "decision_tree_regressor"
]


# =========================
# ANOMALY DETECTION
# =========================

DEFAULT_CONTAMINATION = 0.05


# =========================
# MODEL SELECTION
# =========================

ENABLE_AUTO_MODEL_SELECTION = True