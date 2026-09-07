import os
import sys
import json
import traceback
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


if str(BASE_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(BASE_DIR)
    )


# =========================================================
# IMPORT MAIN PIPELINE
# =========================================================

try:

    from data_engine.orchestrator.engine import (
        run_ai_data_doctor
    )

except ImportError as error:

    print("\n" + "=" * 60)

    print(
        "IMPORT ERROR"
    )

    print("=" * 60)

    print(
        f"\n{error}\n"
    )

    print(
        "Check your data_engine imports "
        "and __init__.py files."
    )

    sys.exit(1)


# =========================================================
# DISPLAY TITLE
# =========================================================

def print_banner():

    print("\n")

    print("=" * 70)

    print(
        "              AI DATA DOCTOR"
    )

    print(
        "       Intelligent Data Analysis System"
    )

    print("=" * 70)

    print()

    print(
        "Features:"
    )

    print(
        "  ✓ File Validation"
    )

    print(
        "  ✓ Data Extraction"
    )

    print(
        "  ✓ Dataset Understanding"
    )

    print(
        "  ✓ Data Profiling"
    )

    print(
        "  ✓ Data Quality Analysis"
    )

    print(
        "  ✓ Data Cleaning"
    )

    print(
        "  ✓ Statistical Analysis"
    )

    print(
        "  ✓ Anomaly Detection"
    )

    print(
        "  ✓ Dataset Intelligence"
    )

    print(
        "  ✓ ML Recommendations"
    )

    print(
        "  ✓ Reporting"
    )

    print("=" * 70)

    print()


# =========================================================
# DISPLAY FILE INFORMATION
# =========================================================

def display_file_info(
    file_path
):

    path = Path(
        file_path
    )


    print("\n")

    print("-" * 60)

    print(
        "FILE INFORMATION"
    )

    print("-" * 60)


    print(
        f"File Name: {path.name}"
    )


    print(
        f"Extension: {path.suffix}"
    )


    if path.exists():

        file_size = (
            path.stat().st_size
            / (1024 * 1024)
        )


        print(
            f"Size: {file_size:.2f} MB"
        )


    print("-" * 60)


# =========================================================
# DISPLAY PIPELINE SUMMARY
# =========================================================

def display_summary(
    results
):

    print("\n")

    print("=" * 70)

    print(
        "PIPELINE SUMMARY"
    )

    print("=" * 70)


    if results.get(
        "from_cache"
    ):

        print(
            "\n⚡ Result loaded from cache."
        )


    # =====================================================
    # PROJECT
    # =====================================================

    project = results.get(
        "project"
    )


    if project:

        print(
            "\nPROJECT"
        )

        print(
            f"Project ID: "
            f"{project.get('project_id')}"
        )


        print(
            f"Project Name: "
            f"{project.get('project_name')}"
        )


    # =====================================================
    # METADATA
    # =====================================================

    metadata = results.get(
        "metadata"
    )


    if metadata:

        print(
            "\nDATASET METADATA"
        )


        dataset = metadata.get(
            "dataset",
            {}
        )


        print(
            f"Rows: "
            f"{dataset.get('rows')}"
        )


        print(
            f"Columns: "
            f"{dataset.get('columns')}"
        )


    # =====================================================
    # INTELLIGENCE
    # =====================================================

    intelligence = results.get(
        "intelligence"
    )


    if intelligence:

        print(
            "\nDATASET INTELLIGENCE"
        )


        classification = (
            intelligence.get(
                "dataset_classification",
                {}
            )
        )


        print(
            "Dataset Type: "
            f"{classification.get('dataset_type')}"
        )


        ml_recommendation = (
            intelligence.get(
                "ml_recommendation",
                {}
            )
        )


        if ml_recommendation:

            print(
                "ML Recommended: "
                f"{ml_recommendation.get('ml_recommended')}"
            )


            if ml_recommendation.get(
                "target_column"
            ):

                print(
                    "Suggested Target: "
                    f"{ml_recommendation.get('target_column')}"
                )


            if ml_recommendation.get(
                "task_type"
            ):

                print(
                    "Suggested Task: "
                    f"{ml_recommendation.get('task_type')}"
                )


    # =====================================================
    # ML RECOMMENDATIONS
    # =====================================================

    ml_recommendations = results.get(
        "ml_recommendations"
    )


    if ml_recommendations:

        print(
            "\nML RECOMMENDATIONS"
        )

        print(
            json.dumps(
                ml_recommendations,
                indent=4,
                default=str
            )
        )


    # =====================================================
    # MONITORING
    # =====================================================

    monitoring = results.get(
        "monitoring"
    )


    if monitoring:

        print(
            "\nPERFORMANCE"
        )


        pipeline_monitoring = (
            monitoring.get(
                "pipeline_monitoring",
                {}
            )
        )


        total_time = (
            pipeline_monitoring.get(
                "total_execution_time_seconds"
            )
        )


        if total_time is not None:

            print(
                f"Total Execution Time: "
                f"{total_time} seconds"
            )


    # =====================================================
    # ERROR
    # =====================================================

    if results.get(
        "error"
    ):

        print(
            "\n❌ PIPELINE ERROR"
        )

        print(
            results["error"]
        )


    else:

        print(
            "\n✅ PIPELINE COMPLETED"
        )


    print("\n")

    print("=" * 70)


# =========================================================
# SAVE RESULTS
# =========================================================

def save_results_to_json(
    results
):

    output_directory = (
        BASE_DIR / "output"
    )


    output_directory.mkdir(
        exist_ok=True
    )


    output_file = (
        output_directory
        / "latest_results.json"
    )


    try:

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                results,

                file,

                indent=4,

                default=str
            )


        print(
            f"\nResults saved to:\n"
            f"{output_file}"
        )


    except Exception as error:

        print(
            "\nCould not save JSON results."
        )

        print(
            error
        )


# =========================================================
# GET FILE FROM USER
# =========================================================

def get_file_path():

    print(
        "\nEnter the complete path "
        "of your dataset."
    )


    print(
        "\nExample:"
    )


    print(
        r"D:\ai_data_doctor\data\customers.csv"
    )


    file_path = input(
        "\nFile Path: "
    ).strip()


    # Remove quotation marks

    file_path = file_path.strip(
        '"'
    )


    return file_path


# =========================================================
# RUN APPLICATION
# =========================================================

def main():

    print_banner()


    # =====================================================
    # GET FILE PATH
    # =====================================================

    file_path = get_file_path()


    # =====================================================
    # CHECK FILE
    # =====================================================

    if not file_path:

        print(
            "\n❌ No file path entered."
        )

        return


    path = Path(
        file_path
    )


    if not path.exists():

        print(
            "\n❌ File not found."
        )


        print(
            f"\nPath received:\n{file_path}"
        )


        return


    # =====================================================
    # DISPLAY FILE
    # =====================================================

    display_file_info(
        file_path
    )


    # =====================================================
    # PROJECT NAME
    # =====================================================

    project_name = input(

        "\nEnter Project Name "
        "(Press Enter for default): "

    ).strip()


    if not project_name:

        project_name = (

            path.stem
            + "_analysis"
        )


    # =====================================================
    # START PIPELINE
    # =====================================================

    print("\n")

    print("=" * 70)

    print(
        "STARTING AI DATA DOCTOR..."
    )

    print("=" * 70)


    try:

        results = run_ai_data_doctor(

            file_path=file_path,

            project_name=project_name
        )


        # =================================================
        # DISPLAY RESULTS
        # =================================================

        display_summary(
            results
        )


        # =================================================
        # SAVE RESULTS
        # =================================================

        save_results_to_json(
            results
        )


    except KeyboardInterrupt:

        print(
            "\n\nPipeline stopped by user."
        )


    except Exception:

        print(
            "\n❌ UNEXPECTED ERROR\n"
        )


        traceback.print_exc()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()