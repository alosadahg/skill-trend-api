import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate(r'skill-trend-firebase-adminsdk-bgeyp-d7e802fc25.json')
firebase_admin.initialize_app(cred)

class FirestoreConfig:
    def __init__(self):
        self.db = firestore.client()
        
    def add_document(self, json_input):
        doc_ref = self.db.collection('skillReports').document(f"{json_input['skill']}_{json_input['startDate']}_{json_input['endDate']}")
        doc_ref.set(json_input)
        
    def get_document(self, json_input):
        doc_ref = self.db.collection('skillReports').document(f"{json_input['skill']}_{json_input['startDate']}_{json_input['endDate']}")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return False