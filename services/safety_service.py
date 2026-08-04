from database.db import get_patient_documents

# Sample interaction database
INTERACTIONS = {
    ("Amoxicillin", "Azithromycin"):
        "Both antibiotics should only be used together if prescribed.",

    ("Paracetamol", "Ibuprofen"):
        "Usually safe together, but prolonged combined use should be monitored.",

    ("Metformin", "Prednisone"):
        "Prednisone may increase blood sugar and reduce Metformin effectiveness.",

    ("Warfarin", "Aspirin"):
        "High risk of bleeding when used together."
}


def check_duplicate_medications(patient_id, current_document):

    previous_documents = get_patient_documents(patient_id)

    previous_drugs = set()

    for document in previous_documents:

        for drug in document["drug_name"]:

            previous_drugs.add(drug)

    duplicates = []

    for drug in current_document["drug_name"]:

        if drug in previous_drugs:

            duplicates.append(drug)

    return duplicates


def check_drug_interactions(drug_list):

    warnings = []

    for drug1 in drug_list:

        for drug2 in drug_list:

            if drug1 == drug2:
                continue

            pair = (drug1, drug2)
            reverse_pair = (drug2, drug1)

            if pair in INTERACTIONS:

                warnings.append({
                    "drug1": drug1,
                    "drug2": drug2,
                    "warning": INTERACTIONS[pair]
                })

            elif reverse_pair in INTERACTIONS:

                warnings.append({
                    "drug1": drug1,
                    "drug2": drug2,
                    "warning": INTERACTIONS[reverse_pair]
                })

    return warnings