import project
import os
def setup_db():
    if os.path.exists("test.db"):
        os.remove("test.db")
    project.DB_NAME = "test.db"
    project.initialize_database()

def test_get_perfume_by_name():
    setup_db()

    project.add_perfume("Givenchy", "Linterdit")

    result = project.get_perfume_by_name("Givenchy","Linterdit")
    assert result == 1
def test_search_perfume():
    project.add_perfume("Yves Saint Laurent","Libre")
    project.add_perfume("Gucci", "Guilty")
    result = project.search_perfume("Yves")
    assert result[0] == "Yves Saint Laurent - Libre"

def test_average_rating():
    setup_db()

    project.add_perfume("Guess", "Bella Vita")
    perfume_id = project.get_perfume_by_name("Guess", "Bella Vita")
    project.add_diary_entry("25-09-2026", perfume_id, 8, "Dinner")

    project.add_perfume("Lancome", "Idole")
    perfume_id = project.get_perfume_by_name("Lancome", "Idole")
    project.add_diary_entry("15-11-2026", perfume_id, 6, "School")

    result = project.average_rating()
    assert result == "7.0/10"
def test_most_used_note():
    setup_db()
    p_id = project.add_perfume("Guess","Bella Vita")

    n_id = project.add_note("Misk")
    project.add_perfume_note(p_id,n_id,"top")
    n_id = project.add_note("Pepper")
    project.add_perfume_note(p_id,n_id,"middle")
    n_id = project.add_note("Vanilla")
    project.add_perfume_note(p_id,n_id,"base")

    project.add_diary_entry(
        "05-10-2026",
        p_id,
        8,
        "Dinner"
    )

    result = project.most_used_note()

    assert result == "Misk (1 use)"

def test_search_by_note():
    setup_db()

    perfume_id = project.add_perfume("Gucci", "Guilty")
    note_id = project.add_note("Vanilla")
    project.add_perfume_note(perfume_id, note_id, "base")

    result = project.search_perfume("Vanilla")

    assert "Gucci - Guilty" in result


def test_search_no_results():
    setup_db()

    project.add_perfume("Gucci", "Guilty")

    result = project.search_perfume("Nehir")

    assert result == []

def test_search_by_note():
    setup_db()

    perfume_id = project.add_perfume("Gucci", "Guilty")
    note_id = project.add_note("Vanilla")
    project.add_perfume_note(perfume_id, note_id, "base")

    result = project.search_perfume("Vanilla")

    assert "Gucci - Guilty" in result


def test_search_no_results():
    setup_db()

    project.add_perfume("Gucci", "Guilty")

    result = project.search_perfume("Nehir")

    assert result == []

def test_empty_database_statistics():
    setup_db()

    assert project.most_used_perfume() == "No diary entries yet."
    assert project.average_rating() == "No reviews yet."
    assert project.highest_rated_perfume() == "No ratings yet."
    assert project.fav_brand() == "No perfumes added yet."
    assert project.most_used_note() == "No notes recorded yet."

def test_invalid_date():
    setup_db()

    perfume_id = project.add_perfume("Gucci", "Guilty")

    result = project.add_diary_entry(
        "05/10/2026",
        perfume_id,
        8,
        "Dinner"
    )

    assert "Date must be in DD-MM-YYYY format." in result


def test_invalid_rating():
    setup_db()

    perfume_id = project.add_perfume("Gucci", "Guilty")

    result = project.add_diary_entry(
        "05-10-2026",
        perfume_id,
        11,
        "Dinner"
    )

    assert "Rating must be between 1 and 10." in result
