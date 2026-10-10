CREATE TABLE IF NOT EXISTS Perfume(
    ID INTEGER PRIMARY KEY,
    Brand TEXT NOT NULL,
    PerfumeName TEXT NOT NULL,
    UNIQUE(Brand,PerfumeName)
);
CREATE TABLE IF NOT EXISTS Note(
    ID INTEGER PRIMARY KEY,
    NoteName TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS PerfumeNotes(
    PerfumeID INTEGER NOT NULL,
    NoteID INTEGER NOT NULL,
    NoteType TEXT CHECK(NoteType IN ('top','middle','base')),

    FOREIGN KEY(PerfumeID) REFERENCES Perfume(ID),
    FOREIGN KEY(NoteID) REFERENCES Note(ID),

    UNIQUE(PerfumeID,NoteID,NoteType)
);
CREATE TABLE IF NOT EXISTS DiaryEntry(
    ID INTEGER PRIMARY KEY,
    EntryDate TEXT NOT NULL,
    PerfumeID INTEGER NOT NULL,
    Rating INTEGER CHECK(Rating>=1 AND Rating<=10),
    Occasion TEXT NOT NULL,

    FOREIGN KEY(PerfumeID) REFERENCES Perfume(ID)
);

