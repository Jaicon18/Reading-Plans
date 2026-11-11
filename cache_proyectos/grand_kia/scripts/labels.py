"""page labels = número de hoja impreso (sheetmap.json verificado en title blocks; p41 duplica A521 -> 'A521-DUP')."""
import json
m = json.load(open('/root/gk/work/sheetmap.json'))
d = {str(v): k for k, v in m.items()}
d['41'] = 'A521-DUP'
print(json.dumps(d))
