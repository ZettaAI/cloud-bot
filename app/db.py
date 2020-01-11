from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
# db = firestore.Client()

# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})


# doc_ref = db.collection(u"users").document(u"aturing") URPPK415M
# doc_ref.set(
#     {u"first": u"Alan", u"middle": u"Mathison", u"last": u"Turing", u"born": 1912}
# )


# users_ref = db.collection(u"users")
# docs = users_ref.stream()

# for doc in docs:
#     print(u"{} => {}".format(doc.id, doc.to_dict()))


# TODO
# admins collection
#   can run priviledged commands like generating new service account keys
# events collection
#   store each event received from slack with ID and timestamp, as JSON string
# maybe look into helm and tiller
