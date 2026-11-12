"""BE-GK56 (Grand Kia rev3b, U-193 / BE-GK54 measurement by the independent reviewer, 12-nov): the target of an exclusion "same wall as <X>"
was taken from the first wall id written in the reason, but those ids are the READER's numbering (reader A's A-Z1-06 is not canon
A-Z1-06): 5 of 10 targets pointed to another canon wall (A-Z1-05 -> A-Z1-06 was 12.9 ft away; the real one, A-Z1-08, shares the band).
Rule: the target of a 'same wall' exclusion is the canon wall whose band the piece lies on, MEASURED on the plan (gap_proof with the
measured gap + N/SHEET, from the independent reviewer), never an id parsed from the reader's text; a piece with a measured gap > 0 is a
FALTA and goes through the chain (the exclusion then says 'loaded as <ref>' and the ref exists in the canon). Usage: python3 be_gk56.py <canon.json>  -> exit 1 on FAIL."""
import json, re, sys

RX_NH = re.compile(r"\b\d{1,2}[A-Z]?/[A-Z]{1,2}-?\d{1,3}(?:\.\d{1,2})?\b")
RX_GAP = re.compile(r"(?i)\bgap\s*(\d+(?:\.\d+)?)\s*(?:\"|in\b)")


def fallas(canon):
    ids = {w['id'] for w in canon.get('walls') or []}
    ev = []
    for e in canon.get('excluded_walls') or []:
        r = str(e.get('reason') or '')
        m = re.match(r"(?i)same wall as ([A-Z][A-Z0-9]*-Z\d-\d{2})\s*:", r)
        if not m:
            continue
        x, gp = m.group(1), str(e.get('gap_proof') or '')
        g = RX_GAP.search(gp)
        if x not in ids:
            ev.append(f"{e.get('id')}: 'same wall as {x}' but {x} is not a canon wall (BE-GK56)")
        elif not (g and RX_NH.search(gp)):
            ev.append(f"{e.get('id')}: 'same wall as {x}' without a measured gap_proof (gap + N/SHEET): the target may be a reader id read as "
                      f"a canon id; measure on the plan which canon band the piece lies on (BE-GK56)")
        elif float(g.group(1)) > 0 and not any(re.search(r"(?i)loaded as " + re.escape(str(m.get('ref', '')).split()[0]) + r"\b", r + ' ' + gp)
                                                for m in canon.get('misc_items') or [] if m.get('ref')):
            ev.append(f"{e.get('id')}: measured gap {g.group(1)}\" > 0 to {x}: not the same wall - it is a FALTA and goes through the chain (BE-GK56)")
    return ev


if __name__ == '__main__':
    ev = fallas(json.load(open(sys.argv[1])))
    print('\n'.join(ev) if ev else 'BE-GK56 PASS: every same-wall exclusion has its measured canon target')
    sys.exit(1 if ev else 0)
