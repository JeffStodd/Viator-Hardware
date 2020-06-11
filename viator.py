import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
	'projectId':'viator-b2e7e',
	})
	
db = firestore.client()

doc_ref = db.collection(u'users').document(
	u'GIyoaICsC8bGQ482qIJrCZPbDA53')
	
try:
	doc = doc_ref.get()
	print(u'Document data: {}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
	print(u'No doc')	
