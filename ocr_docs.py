import requests, json
from db import Document, get_session
from config import TS_KEY

parse_url = "https://api.textspark.io/v1/parse?user_key=%s"%TS_KEY

def update(docs):
    for doc in docs:
        pdf = request.get(doc.url).text
        txt = json.loads(requests.put(parse_url, data=pdf).text)['content']
        doc.text = txt

        
if __name__ == "__main__":
    db = get_session()
    docs = db.query(Document).filter(Document.text == None).filter(Document.url != None)
    update(docs)
    db.commit()
