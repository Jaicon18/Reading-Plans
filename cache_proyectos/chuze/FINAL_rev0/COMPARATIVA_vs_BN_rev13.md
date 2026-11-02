# Comparison vs best reference take-off (Barnes & Noble Colorado Springs, rev13, skill v80s)

Purpose: same procedure and format on every project; proportions within range of the verified reference.

## 1. Format (Excel)
| Check | Result |
|---|---|
| Sheets | Identical: Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist (+ hidden _reglas seal) |
| Column headers of every sheet | Identical |
| Partitions in schedule order, subtotal per type, grand total | Yes (A301 order A2-3D … X6D, then OTHER FRAMING) |

## 2. Proportions (from each Excel Material Summary NET and Partition Takeoff)
| Ratio | Chuze rev0 | B&N rev13 | Explanation |
|---|---|---|---|
| Partition LF | 1,006.72 | 569.82 | Chuze is ~1.8x larger |
| Stud LF / partition LF | 22.90 | 26.06 | B&N walls 25'-0" to deck; Chuze 22'-10" (PENDING, RFI-01) plus 5'-0" / 12'-0" partial-height walls |
| Track LF / partition LF | 2.63 | 3.48 | Chuze: bottom + top per wall (+ double row A2-3D) + ceiling / soffit track; B&N had double deflection track and exterior / parapet framing |
| Board SF / partition LF | 37.15 | 27.81 | Chuze boards both faces to deck on most walls (theoretical max 2 x 22.83 = 45.7); B&N exterior walls had no board (by future tenant) |
| Bracing LF / partition LF | 6.30 | 5.86 | Similar wall heights → similar rows of bracing |
| Drywall screws / board SF | 1.20 | 1.16 | Same yield criterion (Inputs) |

No proportion is out of range without explanation.

## 3. Biggest sensitivities of Chuze (open RFIs)
- RFI-01 B.O. deck not printed (22'-10" loaded, only hidden text): drives stud LF, board SF and bracing on ~80 walls.
- RFI-04 / RFI-18 gauge and O.C. not printed (S501 / S001 not in the set).
- AD101 note 5 furring removed at existing exterior walls: only B2E where tagged is loaded; re-furring of untagged existing walls is an RFI.
