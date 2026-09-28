import csv
from pathlib import Path


# ---------------------------------------------------------
# Find the Nanami customer feedback CSV
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "data" / "nanami_50_Customer_Feedback.csv"


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def find_column(fieldnames, possible_names):
    """
    Find a CSV column using several possible column names.
    """
    if not fieldnames:
        return None

    normalized_fields = {
        normalize(field): field
        for field in fieldnames
    }

    for name in possible_names:
        key = normalize(name)

        if key in normalized_fields:
            return normalized_fields[key]

    # Partial match
    for field in fieldnames:
        field_normalized = normalize(field)

        for name in possible_names:
            name_normalized = normalize(name)

            if name_normalized in field_normalized:
                return field

    return None


def classify_sentiment(text):
    """
    Simple fallback sentiment detection if the CSV does not
    contain a sentiment column.
    """

    text = normalize(text)

    positive_words = [
        "good",
        "great",
        "excellent",
        "happy",
        "satisfied",
        "love",
        "amazing",
        "helpful",
        "fast",
        "perfect",
        "easy",
        "nice",
        "working well",
        "works well"
    ]

    negative_words = [
        "bad",
        "poor",
        "problem",
        "issue",
        "slow",
        "terrible",
        "worst",
        "drain",
        "draining",
        "blurry",
        "disconnect",
        "disconnecting",
        "overheat",
        "heating",
        "broken",
        "error",
        "fail",
        "failed",
        "failure",
        "not working"
    ]

    positive_score = 0
    negative_score = 0

    for word in positive_words:
        if word in text:
            positive_score += 1

    for word in negative_words:
        if word in text:
            negative_score += 1

    if positive_score > negative_score:
        return "positive"

    if negative_score > positive_score:
        return "negative"

    return "neutral"


def detect_category(text):
    """
    Detect the main customer complaint category.
    """

    text = normalize(text)

    if "battery" in text:
        return "battery"

    if "camera" in text:
        return "camera"

    if "wifi" in text or "wi-fi" in text:
        return "wifi"

    if (
        "heating" in text
        or "overheat" in text
        or "overheating" in text
        or "hot" in text
        or "temperature" in text
    ):
        return "heating"

    return "other"


def get_numeric_rating(value):
    """
    Safely convert a rating value to a number.
    """

    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    try:
        return float(text)
    except ValueError:
        return None


# ---------------------------------------------------------
# Main dashboard function
# ---------------------------------------------------------

def get_dashboard_data():

    # Check that the CSV exists
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Customer feedback CSV not found at: {CSV_PATH}"
        )

    # Read CSV
    with open(
        CSV_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)
        fieldnames = reader.fieldnames or []

    # -----------------------------------------------------
    # Detect important columns
    # -----------------------------------------------------

    sentiment_column = find_column(
        fieldnames,
        [
            "sentiment",
            "Sentiment",
            "customer sentiment"
        ]
    )

    rating_column = find_column(
        fieldnames,
        [
            "rating",
            "Rating",
            "customer rating",
            "score",
            "stars"
        ]
    )

    category_column = find_column(
        fieldnames,
        [
            "category",
            "Category",
            "issue category",
            "complaint category",
            "issue type",
            "type"
        ]
    )

    feedback_column = find_column(
        fieldnames,
        [
            "feedback",
            "Feedback",
            "customer feedback",
            "comment",
            "comments",
            "review",
            "text",
            "message",
            "description"
        ]
    )

    # -----------------------------------------------------
    # Counters
    # -----------------------------------------------------

    total_feedback = len(rows)

    positive = 0
    negative = 0
    neutral = 0

    battery = 0
    camera = 0
    heating = 0
    wifi = 0

    ratings = []

    # -----------------------------------------------------
    # Process every customer record
    # -----------------------------------------------------

    for row in rows:

        # Combine all row values for fallback analysis
        all_text = " ".join(
            str(value)
            for value in row.values()
            if value is not None
        )

        # ---------------------------------------------
        # Sentiment
        # ---------------------------------------------

        if sentiment_column:
            sentiment = normalize(
                row.get(sentiment_column, "")
            )

            if "positive" in sentiment:
                positive += 1

            elif "negative" in sentiment:
                negative += 1

            else:
                neutral += 1

        else:
            sentiment = classify_sentiment(all_text)

            if sentiment == "positive":
                positive += 1

            elif sentiment == "negative":
                negative += 1

            else:
                neutral += 1

        # ---------------------------------------------
        # Rating
        # ---------------------------------------------

        if rating_column:

            rating = get_numeric_rating(
                row.get(rating_column)
            )

            if rating is not None:
                ratings.append(rating)

        # ---------------------------------------------
        # Category
        # ---------------------------------------------

        if category_column:

            category = normalize(
                row.get(category_column, "")
            )

            # Battery
            if "battery" in category:
                battery += 1

            # Camera
            elif "camera" in category:
                camera += 1

            # WiFi
            elif "wifi" in category or "wi-fi" in category:
                wifi += 1

            # Heating
            elif (
                "heat" in category
                or "overheat" in category
                or "temperature" in category
            ):
                heating += 1

        else:

            category = detect_category(all_text)

            if category == "battery":
                battery += 1

            elif category == "camera":
                camera += 1

            elif category == "wifi":
                wifi += 1

            elif category == "heating":
                heating += 1

    # -----------------------------------------------------
    # Average rating
    # -----------------------------------------------------

    if ratings:
        average_rating = round(
            sum(ratings) / len(ratings),
            2
        )
    else:
        average_rating = 0

    # -----------------------------------------------------
    # Return dashboard data
    # -----------------------------------------------------

    return {
        "total_feedback": total_feedback,

        "positive": positive,

        "negative": negative,

        "neutral": neutral,

        "average_rating": average_rating,

        "battery": battery,

        "camera": camera,

        "heating": heating,

        "wifi": wifi
    }


# ---------------------------------------------------------
# Local test
# ---------------------------------------------------------

if __name__ == "__main__":

    print("--------------------------------")
    print("Nanami AI Dashboard Test")
    print("--------------------------------")

    print(f"CSV path:")
    print(CSV_PATH)

    print()

    data = get_dashboard_data()

    print("Dashboard data:")
    print(data)

    print()
    print("Dashboard test completed.")