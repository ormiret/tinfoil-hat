import requests, json
from db import Document, get_session
from config import TS_KEY

parse_url = "https://api.textspark.io/v1/parse?user_key=%s"%TS_KEY

def update(docs):
    for doc in docs:
        print "Processing document %d"%doc.id
        pdf_resp = requests.get(doc.url)
        resp = requests.put(parse_url, data=pdf_resp.content)
        if resp.ok:
            txt = json.loads(resp.text)['content']
            doc.text = txt[:64000]
        else:
            print "Got %d from textspark."%resp.status_code
            
            doc.text = "borked"

        
if __name__ == "__main__":
    db = get_session()
    while True:
        docs = db.query(Document).filter(Document.text == None).filter(Document.url != None).all()
        update(docs)
        db.commit()
