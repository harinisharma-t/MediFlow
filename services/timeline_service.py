import sqlite3
import json

DATABASE_NAME = "database/mediflow.db"


def get_patient_timeline(patient_id):

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # Show every patient_id in the database
    cursor.execute("SELECT patient_id FROM documents")
    print("Patient IDs in database:")
    for row in cursor.fetchall():
        print(row["patient_id"])

    # Now run the timeline query
    cursor.execute("""
        SELECT *
        FROM documents
        WHERE patient_id = ?
        ORDER BY date DESC
    """, (patient_id,))

    rows = cursor.fetchall()

    connection.close()

    documents = []

    for row in rows:

        document = dict(row)

        document["drug_name"] = json.loads(document["drug_name"])
        document["dosage"] = json.loads(document["dosage"])
        document["frequency"] = json.loads(document["frequency"])

        documents.append(document)

    return documents


if __name__ == "__main__":

    timeline = get_patient_timeline("patient1")

    print("\nTimeline:\n")
    print(timeline)