DATASET_KEYWORDS = {

    "sales": [
        "sales",
        "revenue",
        "product",
        "quantity",
        "order",
        "customer"
    ],

    "financial": [
        "income",
        "expense",
        "profit",
        "balance",
        "payment",
        "transaction",
        "amount"
    ],

    "customer": [
        "customer",
        "client",
        "email",
        "gender",
        "age",
        "customer_id"
    ],

    "employee": [
        "employee",
        "salary",
        "department",
        "designation",
        "job",
        "manager"
    ],

    "healthcare": [
        "patient",
        "hospital",
        "disease",
        "diagnosis",
        "doctor",
        "medical"
    ],

    "education": [
        "student",
        "course",
        "marks",
        "grade",
        "school",
        "university"
    ]
}


def classify_dataset(dataframe):
    """
    Classify the overall dataset domain.
    """

    column_names = [
        str(column).lower()
        for column in dataframe.columns
    ]

    scores = {}

    for dataset_type, keywords in (
        DATASET_KEYWORDS.items()
    ):

        score = 0

        for column in column_names:

            for keyword in keywords:

                if keyword in column:
                    score += 1

        scores[dataset_type] = score

    best_type = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_type]

    if best_score == 0:

        return {
            "dataset_type": "general",
            "confidence": 0
        }

    total_keywords = len(
        DATASET_KEYWORDS[best_type]
    )

    confidence = round(
        min(
            (best_score / total_keywords) * 100,
            100
        ),
        2
    )

    return {
        "dataset_type": best_type,
        "confidence": confidence
    }