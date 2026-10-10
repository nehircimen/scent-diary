import sqlite3
from datetime import datetime
DB_NAME = "Scent_diary.db"
def main():
    initialize_database()
    while True:
        show_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            brand = input("Brand: ")
            name = input("Name: ")
            perfume_id = add_perfume(brand,name)
            if not isinstance(perfume_id, int):
                print(perfume_id)
                continue
            top = input("Top Note: ")
            note_id = add_note(top)
            if not isinstance(note_id,int):
                print(note_id)
                continue
            top_result = add_perfume_note(perfume_id,note_id,"top")
            if top_result is not True:
                print(top_result)
                continue
            middle = input("Middle Note: ")
            note_id = add_note(middle)
            if not isinstance(note_id,int):
                print(note_id)
                continue
            mid_result = add_perfume_note(perfume_id,note_id,"middle")
            if mid_result is not True:
                print(mid_result)
                continue
            base = input("Base Note: ")
            note_id = add_note(base)
            if not isinstance(note_id,int):
                print(note_id)
                continue
            base_result = add_perfume_note(perfume_id,note_id,"base")
            if base_result is not True:
                print(base_result)
                continue
            print("Perfume added succesfully.")

        elif choice == "2":
            date = input("Date: ")
            brand = input("Brand: ")
            name = input("Name: ")
            perfume_id = get_perfume_by_name(brand,name)
            if perfume_id is None:
                print("Diary entry could not be added. Perfume not found.")
                continue
            rating = input("Rating: ")
            occasion = input("Occasion: ")
            result = add_diary_entry(date,perfume_id,rating,occasion)
            if result is not True:
                print(result)
                continue
            print("Diary entry added succesfuly.")

        elif choice == "3":
            term = input("Enter the term you want the search for: ")
            perfumes = search_perfume(term)

            if not perfumes:
                print("No matching perfumes found.")
                continue
            print("\n".join(perfumes))

        elif choice == "4":
            print(f"Most used perfume: {most_used_perfume()}")
            print(f"Average rating: {average_rating()}")
            print(f"Highest rated perfume: {highest_rated_perfume()}")
            print(f"Your favorite brand: {fav_brand()}")
            print(f"Most used note: {most_used_note()}")

        elif choice == "5":
            break
        else:
            print("Invalid choice")

def connect_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    return con,cur

def initialize_database():
    # 1. coonect database
    con,cur = connect_db()

    # 2. read schema.sql file
    with open("schema.sql","r") as file:
        schema = file.read()

    # 3. run SQL script on database
    cur.executescript(schema)

    con.commit()
    con.close()
def show_menu():
    print("\n --- SCENT DIARY --- ")
    print("What would you like to do?")
    print("1. Add a new perfume")
    print("2. Add a diary entry")
    print("3. Search perfumes")
    print("4. View statistics")
    print("5. Exit")

def get_perfume_by_name(brand,name):
    brand = brand.strip().title()
    name = name.strip().title()
    con, cur = connect_db()

    cur.execute(
        "SELECT ID FROM Perfume WHERE Brand = ? AND PerfumeName = ?",
        (brand,name)
    )

    result = cur.fetchone()

    con.close()
    if result is None:
        return None
    return result[0]
def add_perfume(brand, name):
    brand = brand.strip().title()
    name = name.strip().title()

    if not brand or not name:
        return "Brand and perfume name cannot be empty."

    con, cur = connect_db()

    try:
        cur.execute(
            "INSERT INTO Perfume (Brand, PerfumeName) VALUES (?, ?)",
            (brand, name)
        )

        last_id = cur.lastrowid
        con.commit()
        return last_id

    except sqlite3.IntegrityError:
        return "This perfume already exists."

    finally:
        con.close()
def add_perfume_note(perfume_id,note_id,note_type):
    con,cur = connect_db()

    try:
        cur.execute(
            "INSERT INTO PerfumeNotes (PerfumeID,NoteID,NoteType) VALUES (?,?,?)",
            (perfume_id,note_id,note_type)
        )
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return "This perfume-note relationship already exists."
    finally:
        con.close()

def add_note(note_name):
    note_name = note_name.strip().title()

    if not note_name:
        return "Note name cannot be empty."

    con, cur = connect_db()

    cur.execute(
        "SELECT ID FROM Note WHERE LOWER(NoteName) = LOWER(?)",
        (note_name,)
    )

    result = cur.fetchone()

    if result:
        con.close()
        return result[0]

    try:
        cur.execute(
            "INSERT INTO Note (NoteName) VALUES (?)",
            (note_name,)
        )

        last_id = cur.lastrowid
        con.commit()
        con.close()

        return last_id

    except sqlite3.IntegrityError:
        con.close()
        return "Could not add note."
def add_diary_entry(entry_date,perfume_id,rating,occasion):
    occasion = occasion.strip().title()
    try:
        datetime.strptime(entry_date, "%d-%m-%Y")
    except ValueError:
        return "Diary entry could not be added. Date must be in DD-MM-YYYY format."
    try:
        rating = int(rating)
    except ValueError:
        return "Diary entry could not be added. Rating must be a number."
    if rating < 1 or rating > 10:
        return "Diary entry could not be added. Rating must be between 1 and 10."
    if not occasion:
        return "Diary entry could not be added. Occasion cannot be empty."

    con,cur = connect_db()
    cur.execute(
        "INSERT INTO DiaryEntry (EntryDate,PerfumeID,Rating,Occasion) VALUES (?,?,?,?)",
        (entry_date,perfume_id,rating,occasion)
    )
    con.commit()
    con.close()
    return True
def get_perfume(perfume_id):
    con,cur = connect_db()
    cur.execute(
        "SELECT * FROM Perfume WHERE ID = ?",
        (perfume_id,)
    )
    result = cur.fetchone()
    con.close()
    return result
def search_perfume(search_term):
    con,cur = connect_db()
    cur.execute(
        """
        SELECT
            Perfume.ID,
            Perfume.Brand,
            Perfume.PerfumeName
        FROM Perfume
        LEFT JOIN PerfumeNotes
            ON Perfume.ID = PerfumeNotes.PerfumeID
        LEFT JOIN Note
            ON PerfumeNotes.NoteID = Note.ID
        WHERE Perfume.PerfumeName LIKE ?
        OR Perfume.Brand LIKE ?
        OR Note.NoteName LIKE ?
        GROUP BY Perfume.ID, Perfume.Brand, Perfume.PerfumeName
        ORDER BY MIN(
            CASE PerfumeNotes.NoteType
                WHEN 'top' THEN 1
                WHEN 'middle' THEN 2
                WHEN 'base' THEN 3
                ELSE 4
            END
)
        """,
        (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
    )
    result = cur.fetchall()
    con.close()
    formatted_result = [f"{brand} - {name}" for perf_id, brand, name in result]
    return formatted_result
def most_used_perfume():
    con,cur = connect_db()
    cur.execute(
        """
        SELECT Perfume.Brand, Perfume.PerfumeName, COUNT(*) FROM DiaryEntry
        JOIN Perfume
            ON DiaryEntry.PerfumeID = Perfume.ID
        GROUP BY Perfume.ID ORDER BY COUNT(*) DESC LIMIT 1
        """
    )
    result = cur.fetchone()

    con.close()
    if result is None:
        return "No diary entries yet."

    brand,name,count = result
    return f"{brand} - {name} ({count} use{'s' if count != 1 else ''})"

def average_rating():
    con,cur = connect_db()
    cur.execute("SELECT AVG(Rating) FROM DiaryEntry")

    result = cur.fetchone()
    con.close()
    if not result or result[0] is None:
        return "No reviews yet."
    avg_val = result[0]
    return f"{avg_val:.1f}/10"

def highest_rated_perfume():
    con,cur = connect_db()
    cur.execute(
        """
        SELECT Perfume.Brand, Perfume.PerfumeName, AVG(Rating) FROM DiaryEntry
        JOIN Perfume
            ON DiaryEntry.PerfumeID = Perfume.ID
        GROUP BY Perfume.ID ORDER BY AVG(Rating) DESC LIMIT 1
        """
    )

    result = cur.fetchone()
    con.close()
    if result is None:
        return "No ratings yet."
    brand,name,rt = result
    return f"{brand} - {name}: {rt:.1f}/10"
def fav_brand():
    con,cur = connect_db()
    cur.execute(
        """
        SELECT Brand, COUNT(*) FROM Perfume
        GROUP BY Brand ORDER BY COUNT(*) DESC LIMIT 1
        """)
    result = cur.fetchone()
    con.close()
    if result is None:
        return "No perfumes added yet."
    brand,count = result
    return f"{brand} ({count} perfumes)"
def most_used_note():
    con,cur = connect_db()
    cur.execute(
        """
        SELECT Note.NoteName, COUNT(*)
        FROM DiaryEntry
        JOIN Perfume
            ON DiaryEntry.PerfumeID = Perfume.ID
        JOIN PerfumeNotes
            ON Perfume.ID = PerfumeNotes.PerfumeID
        JOIN Note
            ON PerfumeNotes.NoteID = Note.ID
        GROUP BY Note.ID
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """)
    result = cur.fetchone()
    con.close()

    if result is None:
        return "No notes recorded yet."

    note, count = result
    return f"{note} ({count} use{'s' if count != 1 else ''})"
if __name__ == "__main__":
    main()
