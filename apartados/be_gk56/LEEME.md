# BE-GK56: check and test (to merge into tools/ in the next skill version)

Error (Grand Kia rev3b, measurement by the U-193 independent reviewer, 12-nov):
- In an exclusion, the target of "same wall as <X>" was taken from the first wall id written in the reason.
- Those ids use the READER's numbering. Reader A's A-Z1-06 is not canon A-Z1-06.
- Result: 5 of 10 targets pointed to another canon wall. The worst case was 12.9 ft away.
- One of the 10 pieces, readerA_G-Z2-15, had a measured gap > 0 (6.9"). That gap hid an unloaded furring box: the keynote 6 roof drain in Dealer 140, now RI-18C.

Rule:
- The target of a "same wall" exclusion is the canon wall whose band the piece sits on, MEASURED on the plan by the independent reviewer, with gap_proof = measured gap + N/SHEET.
- The target is never an id parsed from the reader's text.
- A measured gap > 0 is a FALTA. It goes through the chain, and the exclusion says "loaded as <ref>".

Files:
- `be_gk56.py::fallas(canon)`. CLI: `python3 be_gk56.py <canon>`.
- `test_be_gk56.py`: the real cases (target parsed from text = FAIL; measured = PASS; gap > 0 not loaded = FAIL; gap > 0 loaded as RI-18C = PASS; target not in the canon = FAIL).
