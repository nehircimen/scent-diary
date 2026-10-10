# Scent Diary

#### Video Demo: https://youtu.be/JqSXL3cl25k

#### Description:

Scent Diary is a command-line perfume diary application written in Python. It allows users to store perfumes and their fragrance notes, record perfume usage in a personal diary, search for perfumes, and view statistics based on their collection and diary entries.

The project uses SQLite as its database. The database is divided into related tables for perfumes, notes, perfume-note relationships, and diary entries.

## Features

* Add a perfume with its brand and name.
* Add top, middle, and base notes to a perfume.
* Record perfume usage with:

  * Date
  * Perfume
  * Rating from 1 to 10
  * Occasion
* Search perfumes by:

  * Perfume name
  * Brand
  * Note
* Display statistics including:

  * Most used perfume
  * Average rating
  * Highest-rated perfume
  * Favorite brand
  * Most used note

## Files

### `project.py`

The main Python program. It contains the database connection, database initialization, perfume and note functions, search functionality, statistics, and the command-line menu.

### `schema.sql`

Contains the SQLite database schema. It creates the following tables:

* `Perfume`
* `Note`
* `PerfumeNotes`
* `DiaryEntry`

The `PerfumeNotes` table connects perfumes and notes and stores whether a note is a top, middle, or base note.

### `test_project.py`

Contains tests for the main project functions using a separate test database.

### `.gitignore`

Prevents generated database files and Python cache files from being included in the repository.

### `Dockerfile`

Contains the instructions for building a Docker image for Scent Diary. It uses a lightweight Python image, copies the application and database schema into the container, and runs the command-line application.

## Database Design

The project uses a relational database to avoid storing repeated information unnecessarily.

A perfume is stored in the `Perfume` table. Notes are stored separately in the `Note` table. Since one perfume can have multiple notes and a note can belong to multiple perfumes, the `PerfumeNotes` junction table establishes the relationship between them.

`DiaryEntry` stores each individual perfume usage and connects it to the corresponding perfume using a foreign key.

The database also uses constraints such as `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, and `CHECK` to maintain data integrity.

## Running the Program

Run the program with:

```bash
python project.py
```

The program will initialize the SQLite database automatically if it does not already exist.

## Running the Tests

The tests can be run with:

```bash
pytest
```

The tests use a separate `test.db` database so that testing does not modify the main project database.

## Requirements

The project uses Python's standard library and SQLite, so no additional packages are required to run the application.

