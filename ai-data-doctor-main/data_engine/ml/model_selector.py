def select_best_model(
    evaluation_results,
    problem_type
):
    """
    Select the best performing model.
    """

    best_model_name = None

    best_score = None

    for model_name, information in (
        evaluation_results.items()
    ):

        if not information["success"]:

            continue

        metrics = information[
            "metrics"
        ]

        if problem_type == "classification":

            score = metrics["f1_score"]

            higher_is_better = True

        else:

            score = metrics["r2_score"]

            higher_is_better = True

        if best_score is None:

            best_score = score

            best_model_name = model_name

            continue

        if higher_is_better:

            if score > best_score:

                best_score = score

                best_model_name = model_name

    return {

        "best_model":
            best_model_name,

        "best_score":
            best_score
    }