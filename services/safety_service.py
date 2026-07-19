import sqlite3
import json

DATABASE_NAME = "database/mediflow.db"


def get_existing_documents(patient_id):

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM documents
        WHERE patient_id = ?
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


def check_duplicate_medications(patient_id, new_document):

    existing_documents = get_existing_documents(patient_id)

    existing_drugs = set()

    for document in existing_documents:

        for drug in document["drug_name"]:
            existing_drugs.add(drug.lower().strip())

    duplicate_drugs = []

    for drug in new_document["drug_name"]:

        if drug.lower().strip() in existing_drugs:
            duplicate_drugs.append(drug)

    return duplicate_drugs


if __name__ == "__main__":

    sample_document = {
        "drug_name": [
            "Paracetamol",
            "Vitamin C",
            "Cetirizine"
        ]
    }

    duplicates = check_duplicate_medications(
        "patient1",
        sample_document
    )

    print("Duplicate Medicines Found:")
    print(duplicates)