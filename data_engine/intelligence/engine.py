from .dataset_classifier import (
    classify_dataset
)

from .target_detector import (
    detect_target_candidates
)

from .ml_recommender import (
    recommend_ml_task
)

from .analysis_recommender import (
    recommend_analysis
)


def run_intelligence_engine(
    dataframe,
    previous_results=None
):
    """
    Run the complete
    intelligence engine.
    """


    # =========================
    # CLASSIFY DATASET
    # =========================

    dataset_classification = (

        classify_dataset(
            dataframe
        )
    )


    # =========================
    # DETECT TARGETS
    # =========================

    target_candidates = (

        detect_target_candidates(
            dataframe
        )
    )


    # =========================
    # ML RECOMMENDATION
    # =========================

    ml_recommendation = (

        recommend_ml_task(

            dataframe,

            target_candidates
        )
    )


    # =========================
    # ANALYSIS RECOMMENDATION
    # =========================

    analysis_recommendations = (

        recommend_analysis(
            dataframe
        )
    )


    # =========================
    # FINAL RESULT
    # =========================

    return {

        "dataset_classification":

            dataset_classification,


        "target_candidates":

            target_candidates,


        "ml_recommendation":

            ml_recommendation,


        "analysis_recommendations":

            analysis_recommendations
    }