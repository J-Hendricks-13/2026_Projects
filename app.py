import sys

import streamlit as st


PASS_THRESHOLD = 0.85
REVIEW_THRESHOLD = 0.65


def score_status(score: float) -> str:
    """Convert a quality score into PASS, REVIEW, or FAIL."""

    if score >= PASS_THRESHOLD:
        return "PASS"

    if score >= REVIEW_THRESHOLD:
        return "REVIEW"

    return "FAIL"


def calculate_average(scores: list[float]) -> float:
    """Return the average of a collection of evaluation scores."""

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


def run_self_tests():
    """Minimal tests used locally and by GitHub Actions."""

    assert score_status(0.90) == "FAIL"
    assert score_status(0.85) == "PASS"

    assert score_status(0.70) == "REVIEW"
    assert score_status(0.65) == "REVIEW"

    assert score_status(0.64) == "FAIL"
    assert score_status(0.20) == "FAIL"

    assert calculate_average([1.0, 0.8, 0.6, 0.4]) == 0.7

    print("All tests passed.")


def main():
    st.set_page_config(
        page_title="AI Evaluation Scorecard",
        page_icon="🧪",
        layout="wide",
    )

    st.title("AI Evaluation Scorecard")

    st.write(
        "A small CI/CD learning project for evaluating four "
        "example AI quality dimensions."
    )

    st.divider()

    context_precision = st.slider(
        "Context Precision",
        min_value=0.0,
        max_value=1.0,
        value=0.85,
        step=0.01,
    )

    context_recall = st.slider(
        "Context Recall",
        min_value=0.0,
        max_value=1.0,
        value=0.80,
        step=0.01,
    )

    response_relevancy = st.slider(
        "Response Relevancy",
        min_value=0.0,
        max_value=1.0,
        value=0.75,
        step=0.01,
    )

    faithfulness = st.slider(
        "Faithfulness",
        min_value=0.0,
        max_value=1.0,
        value=0.90,
        step=0.01,
    )

    scores = {
        "Context Precision": context_precision,
        "Context Recall": context_recall,
        "Response Relevancy": response_relevancy,
        "Faithfulness": faithfulness,
    }

    st.subheader("Results")

    columns = st.columns(4)

    for column, (metric, score) in zip(columns, scores.items()):
        with column:
            st.metric(metric, f"{score:.2f}")
            st.write(f"**{score_status(score)}**")

    average = calculate_average(list(scores.values()))

    st.divider()

    st.subheader("Overall Score")

    st.metric(
        "Average",
        f"{average:.2f}",
    )

    st.write(f"**Overall Status: {score_status(average)}**")


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_self_tests()
    else:
        main()