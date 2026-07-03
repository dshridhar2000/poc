
#!/usr/bin/env python3
import argparse,csv,html,json
from collections import Counter
from datetime import datetime
p=argparse.ArgumentParser()
p.add_argument("--input",required=True)
p.add_argument("--csv",required=True)
p.add_argument("--html",required=True)
a=p.parse_args()
alerts=json.load(open(a.input,encoding="utf-8"))
rows=[];counts=Counter()
for alert in alerts:
    rule=alert.get("rule",{})
    sev=rule.get("security_severity_level") or rule.get("severity") or "Unknown"
    counts[sev]+=1
    loc=alert.get("most_recent_instance",{}).get("location",{})
    rows.append([sev,rule.get("id",""),rule.get("name",""),rule.get("description",""),alert.get("state",""),alert.get("tool",{}).get("name",""),loc.get("path",""),loc.get("start_line",""),alert.get("html_url","")])
with open(a.csv,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Severity","Rule ID","Rule Name","Description","State","Tool","File","Line","Alert URL"])
    w.writerows(rows)
summary="".join(f"<li>{html.escape(str(k))}: {v}</li>" for k,v in sorted(counts.items()))
trs="".join(f"<tr>{''.join(f'<td>{html.escape(str(c))}</td>' for c in r[:-1])}</tr>" for r in rows)
doc=f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{font-family:Arial}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:4px}}th{{background:#eee}}</style></head><body><h1>CodeQL Report</h1><p>{datetime.utcnow().strftime("%d-%b-%Y %H:%M UTC")}</p><ul><li>Total Alerts: {len(rows)}</li>{summary}</ul><table><tr><th>Severity</th><th>Rule ID</th><th>Rule Name</th><th>Description</th><th>State</th><th>Tool</th><th>File</th><th>Line</th></tr>{trs}</table></body></html>'''
open(a.html,"w",encoding="utf-8").write(doc)
print("done")
