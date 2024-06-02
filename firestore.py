import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate(r'skill-trend-firebase-adminsdk-bgeyp-d7e802fc25.json')
firebase_admin.initialize_app(cred)

class FirestoreConfig:
    def __init__(self):
        self.db = firestore.client()
        
    def add_document(self, json_input):
        skill = json_input['skill'].replace(" ", "_")
        start_date = json_input['startDate'].replace(" ", "_")
        end_date = json_input['endDate'].replace(" ", "_")
        doc_ref = self.db.collection('skillReports').document(f"{skill}_{start_date}_{end_date}")
        doc_ref.set(json_input)
        
    def get_document(self, json_input):
        skill = json_input['skill'].replace(" ", "_")
        start_date = json_input['startDate'].replace(" ", "_")
        end_date = json_input['endDate'].replace(" ", "_")
        doc_ref = self.db.collection('skillReports').document(f"{skill}_{start_date}_{end_date}")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return False
