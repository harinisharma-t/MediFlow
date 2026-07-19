import sqlite3
import json

DATABASE_NAME = "database/mediflow.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id TEXT,

        type TEXT,

        drug_name TEXT,

        dosage TEXT,

        frequency TEXT,

        diagnosis TEXT,

        doctor_name TEXT,

        hospital TEXT,

        date TEXT,

        follow_up_instructions TEXT,

        raw_text TEXT

    )
    """)

    connection.commit()
    connection.close()


def save_document(document):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO documents (

        patient_id,
        type,
        drug_name,
        dosage,
        frequency,
        diagnosis,
        doctor_name,
        hospital,
        date,
        follow_up_instructions,
        raw_text

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        document["patient_id"],
        document["type"],
        json.dumps(document["drug_name"]),
        json.dumps(document["dosage"]),
        json.dumps(document["frequency"]),
        document["diagnosis"],
        document["doctor_name"],
        document["hospital"],
        document["date"],
        document["follow_up_instructions"],
        document["raw_text"]

    ))

    connection.commit()
    connection.close()

    print("Document saved successfully.")


def view_documents():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM documents")

    rows = cursor.fetchall()

    connection.close()

    if len(rows) == 0:
        print("No documents found in the database.")
    else:
        print("Documents in database:\n")
        for row in rows:
            print(row)


if __name__ == "__main__":

    create_database()

    print("Database ready.\n")

    view_documents()