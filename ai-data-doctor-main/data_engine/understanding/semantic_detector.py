import re
import pandas as pd


def get_string_values(series):
    """
    Convert non-null values into strings.
    """

    return series.dropna().astype(str)


def calculate_match_ratio(values, pattern):
    """
    Calculate how many values match a regex pattern.
    """

    if len(values) == 0:
        return 0

    matches = values.str.match(
        pattern,
        na=False
    ).sum()

    return matches / len(values)


def detect_email(series):

    values = get_string_values(series)

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    return calculate_match_ratio(
        values,
        pattern
    ) >= 0.8


def detect_url(series):

    values = get_string_values(series)

    pattern = (
        r"^(http://|https://|www\.)"
    )

    return calculate_match_ratio(
        values,
        pattern
    ) >= 0.8


def detect_phone(series):

    values = get_string_values(series)

    # Remove common formatting.
    cleaned = values.str.replace(
        r"[^\d+]",
        "",
        regex=True
    )

    if len(cleaned) == 0:
        return False

    valid_count = 0

    for value in cleaned:

        digits = re.sub(
            r"\D",
            "",
            value
        )

        if 7 <= len(digits) <= 15:
            valid_count += 1

    return (
        valid_count / len(cleaned)
    ) >= 0.8


def detect_datetime(series):

    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    values = get_string_values(series)

    if len(values) == 0:
        return False

    converted = pd.to_datetime(
        values,
        errors="coerce"
    )

    success_ratio = (
        converted.notna().sum()
        / len(values)
    )

    return success_ratio >= 0.8


def detect_percentage(series):

    column_name = str(series.name).lower()

    percentage_keywords = [
        "percentage",
        "percent",
        "rate",
        "ratio"
    ]

    if "%" in column_name:
        return True

    return any(
        keyword in column_name
        for keyword in percentage_keywords
    )


def detect_currency(series):

    column_name = str(series.name).lower()

    currency_keywords = [
        "salary",
        "income",
        "price",
        "cost",
        "revenue",
        "profit",
        "amount",
        "expense",
        "balance",
        "payment"
    ]

    return any(
        keyword in column_name
        for keyword in currency_keywords
    )


def detect_name(series):

    column_name = str(series.name).lower()

    name_keywords = [
        "name",
        "first_name",
        "last_name",
        "fullname",
        "full_name"
    ]

    return any(
        keyword in column_name
        for keyword in name_keywords
    )


def detect_semantic_type(series):
    """
    Detect the most likely semantic meaning.
    """

    column_name = str(series.name).lower()

    # Strong column-name signals first.
    if detect_email(series):
        return "email"

    if detect_url(series):
        return "url"

    if detect_phone(series):
        return "phone"

    if detect_datetime(series):
        return "datetime"

    if detect_percentage(series):
        return "percentage"

    if detect_currency(series):
        return "currency"

    if detect_name(series):
        return "name"

    if "address" in column_name:
        return "address"

    if "country" in column_name:
        return "country"

    if "city" in column_name:
        return "city"

    return "unknown"


def detect_all_semantic_types(dataframe):
    """
    Detect semantic meaning for every column.
    """

    results = {}

    for column in dataframe.columns:

        results[column] = detect_semantic_type(
            dataframe[column]
        )

    return results