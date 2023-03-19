import json

full = []

for fname in ["aberdeen.json", "eastlothian.json", "moray_foi.json"]:
    with open(f"json_outputs/{fname}") as f:
        full += json.load(f)

full.sort(key=lambda x: x['last_updated_at'], reverse=True)

with open("json_outputs/full.json", "w") as f:
    json.dump(full, f, indent=2)

with open("json_outputs/first_1000.json", "w") as f:
    json.dump(full[:1000], f, indent=2)

print(f"Have {len(full)} requests")

