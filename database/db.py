import sqlite3
import json

DATABASE_NAME = "database/mediflow.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Documents table
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

    # Flags table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flags (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id TEXT,

        document_id INTEGER,

        flag_type TEXT,

        message TEXT

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

    document_id = cursor.lastrowid

    connection.close()

    print("Document saved successfully.")

    return document_id


def save_flag(patient_id, document_id, flag_type, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO flags (

        patient_id,
        document_id,
        flag_type,
        message

    )

    VALUES (?, ?, ?, ?)
    """, (

        patient_id,
        document_id,
        flag_type,
        message

    ))

    connection.commit()
    connection.close()

    print("Flag saved successfully.")
def get_flags(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT flag_type, message
    FROM flags
    WHERE patient_id = ?
    ORDER BY id DESC
    """, (patient_id,))

    rows = cursor.fetchall()

    connection.close()

    flags = []

    for row in rows:

        flags.append({
            "flag_type": row[0],
            "message": row[1]
        })

    return flags


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