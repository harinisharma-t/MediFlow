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

def get_total_patients():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT patient_id)
        FROM documents
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_total_documents():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM documents
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_total_flags():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM flags
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_recent_patients(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT patient_id
        FROM documents
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]


def patient_exists(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM documents
        WHERE patient_id = ?
    """, (patient_id,))

    exists = cursor.fetchone()[0] > 0

    connection.close()

    return exists

def view_documents():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM documents")

    rows = cursor.fetchall()

    connection.close()

    if len(rows) == 0:
        print("No documents found.")
    else:
        for row in rows:
            print(row)


def get_patient_summary(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Summary information
    cursor.execute("""
        SELECT
            COUNT(*) AS total_documents,
            MAX(date),
            diagnosis,
            SUM(json_array_length(drug_name))
        FROM documents
        WHERE patient_id = ?
    """, (patient_id,))

    row = cursor.fetchone()

    # Total safety alerts
    cursor.execute("""
        SELECT COUNT(*)
        FROM flags
        WHERE patient_id = ?
    """, (patient_id,))

    total_flags = cursor.fetchone()[0]

    # Number of hospitals visited
    cursor.execute("""
        SELECT COUNT(DISTINCT hospital)
        FROM documents
        WHERE patient_id = ?
    """, (patient_id,))

    total_hospitals = cursor.fetchone()[0]

    # Number of visits
    cursor.execute("""
        SELECT COUNT(DISTINCT date)
        FROM documents
        WHERE patient_id = ?
    """, (patient_id,))

    total_visits = cursor.fetchone()[0]

    connection.close()

    if row and row[0] > 0:

        return {
            "patient_id": patient_id,
            "total_documents": row[0],
            "latest_visit": row[1],
            "latest_diagnosis": row[2],
            "total_medicines": row[3] or 0,
            "total_flags": total_flags,
            "total_hospitals": total_hospitals,
            "total_visits": total_visits
        }

    return None

def get_patient_documents(
    patient_id,
    diagnosis="",
    document_type="",
    medicine="",
    sort="desc"
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            type,
            diagnosis,
            doctor_name,
            hospital,
            date,
            drug_name
        FROM documents
        WHERE patient_id = ?
    """

    parameters = [patient_id]

    if diagnosis:

        query += " AND diagnosis LIKE ?"
        parameters.append(f"%{diagnosis}%")

    if document_type:

        query += " AND type LIKE ?"
        parameters.append(f"%{document_type}%")

    if medicine:

        query += " AND drug_name LIKE ?"
        parameters.append(f"%{medicine}%")

    if sort == "asc":
        query += " ORDER BY id ASC"
    else:
        query += " ORDER BY id DESC"

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    connection.close()

    documents = []

    for row in rows:

        documents.append({

            "id": row[0],
            "type": row[1],
            "diagnosis": row[2],
            "doctor_name": row[3],
            "hospital": row[4],
            "date": row[5],
            "drug_name": json.loads(row[6])

        })

    return documents

def get_recent_documents(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            diagnosis,
            doctor_name,
            date
        FROM documents
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    documents = []

    for row in rows:

        documents.append({

            "patient_id": row[0],
            "diagnosis": row[1],
            "doctor_name": row[2],
            "date": row[3]

        })

    return documents

def compare_patient_prescriptions(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT diagnosis, drug_name, date
        FROM documents
        WHERE patient_id = ?
        ORDER BY id DESC
        LIMIT 2
    """, (patient_id,))

    rows = cursor.fetchall()

    connection.close()

    if len(rows) < 2:
        return None

    current = {
        "diagnosis": rows[0][0],
        "medicines": json.loads(rows[0][1]),
        "date": rows[0][2]
    }

    previous = {
        "diagnosis": rows[1][0],
        "medicines": json.loads(rows[1][1]),
        "date": rows[1][2]
    }

    current_set = set(current["medicines"])
    previous_set = set(previous["medicines"])

    added = sorted(list(current_set - previous_set))
    removed = sorted(list(previous_set - current_set))

    return {
        "current": current,
        "previous": previous,
        "added": added,
        "removed": removed
    }

def get_top_diagnosis():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT diagnosis, COUNT(*)
        FROM documents
        WHERE diagnosis IS NOT NULL
          AND diagnosis != ''
        GROUP BY diagnosis
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    connection.close()

    if row:
        return row[0]

    return "No Data"


def get_top_medicine():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT drug_name
        FROM documents
    """)

    rows = cursor.fetchall()

    connection.close()

    medicines = {}

    for row in rows:

        try:
            drugs = json.loads(row[0])

            for drug in drugs:

                drug = drug.strip()

                medicines[drug] = medicines.get(drug, 0) + 1

        except:
            pass

    if medicines:

        return max(
            medicines,
            key=medicines.get
        )

    return "No Data"


if __name__ == "__main__":

    create_database()

    print("Database ready.\n")

    view_documents()