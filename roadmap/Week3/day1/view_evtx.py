from evtx import PyEvtxParser
import json

parser = PyEvtxParser("EVTX-ATTACK-SAMPLES/Privilege Escalation/privesc_KrbRelayUp_windows_4624.evtx")

events = []

for record in parser.records_json():
    events.append(json.loads(record["data"]))

with open("events.json", "w") as f:
    json.dump(events, f, indent=2)