import json
from datetime import datetime as dt
from dateutil.parser import parse

def parse_date(date):
    try:
        return parse(date, dayfirst=True)
    except:
        print(f"ERROR: can't parse date {date}")
        return None

from foi import FOI
with open('json_outputs/moray_foi.json') as f:
    l = json.load(f)

with open("json_outputs/moray_foi_dataclass.json", "w") as f:
    json.dump([FOI(title=x['name'], last_updated_at=parse_date(x['date']),
                   tags=[x['department']], link=x['url'], body_id=x['number']).asdict()
               for x in l], f, indent=2)
