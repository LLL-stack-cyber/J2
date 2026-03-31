from backend.services.paper_parser import PaperParser


parser = PaperParser()


def test_parse_questions_extracts_numbered_items():
    paper_text = """
    1. Define polymorphism in OOP.
    2) Explain inheritance with one example.
    3: What is encapsulation?
    """

    questions = parser.parse_questions(paper_text)

    assert questions == [
        {"number": 1, "question": "Define polymorphism in OOP."},
        {"number": 2, "question": "Explain inheritance with one example."},
        {"number": 3, "question": "What is encapsulation?"},
    ]


def test_parse_questions_supports_multiline_questions():
    paper_text = """
    Q1. Explain the CAP theorem
    with at least one distributed systems example.

    Question 2) Describe ACID properties.
    """

    questions = parser.parse_questions(paper_text)

    assert questions == [
        {
            "number": 1,
            "question": "Explain the CAP theorem with at least one distributed systems example.",
        },
        {"number": 2, "question": "Describe ACID properties."},
    ]


def test_parse_questions_returns_empty_for_non_numbered_content():
    paper_text = "Instructions: Answer all questions in 2 hours."

    assert parser.parse_questions(paper_text) == []
