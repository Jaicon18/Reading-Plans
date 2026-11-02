# Reader A — extra fields (on top of BRIEF_COMUN.md)

Reader A reads the full canon for its walls (SKILL §2 P3–P6): each wall carries, besides the common fields:

```
"detail": "<type detail N/SHEET, e.g. 'INTERIOR PARTITION TYPE A' A301>", "detail_source": "A301",
"stud_size": "3-5/8\"" | "6\"" | "2\"", "stud_source": "A301 type table", "oc_in": 16, "oc_source": "<N/SHEET or S100/spec>",
"gauge": "<printed gauge or PENDING>", "gauge_source": "<N/SHEET / spec section>",
"height_ft": <stud height>, "height_status": "CONFIRMED|DERIVED|PENDING",
"height_source": "<chain: head detail letter of the tag (A..G) on A301 + B.O. deck / T.O. wall / ceiling from RCP / section>",
"top_track": "<head condition from the tag's head letter, e.g. 'HEAD DETAIL (D)/A301: 2\" slip track to structural deck'>",
"top_track_source": "A301",
"faces": [ {"side": "A"|"B"|"END",            // A = north or west face, B = south or east face
            "room": "<room name + number>", "board": "5/8\" type X | 5/8\" MR | 5/8\" cement backer | DensArmor Plus | none",
            "layers": 1, "height_ft": <board height on this face>, "height_source": "<ceiling height of that room from RCP + type note, or 'full height' per head detail>",
            "board_none_reason": "<only if no board, with N/SHEET>"} ],
"openings": [ {"ref": "<door / window number from A601>", "kind": "door|window|cased|storefront", "ro_w_ft": <>, "head_ft": <>, "source": "A601 / A602 / elevation"} ]
```

Rules for A:
- Head letter = last letter of the tag (A3C → head C, A6D → head D, A2-3D → head D, B2E → head E, X6D → head D …) per
  "WALL TAG KEY" I/A301; the head detail decides whether the stud goes to deck (slip track) or stops above the ceiling.
  Stud size from the middle digit (3 = 3-5/8", 6 = 6", 2 = 2", 8 = 8") per I/A301.
- Face height = the ceiling of the room that face looks at (RCP A121 and the enlarged RCPs A4xx.A) unless the head detail
  says the board goes full height / to deck; B.O. deck / roof structure from S300, sections and elevations. Write the chain.
- Base detail V / W (concrete curb at wet spaces) and X: record it in `notes` of the wall (curb itself is not our scope).
- A2 type note on A301: "MIN. 25 GAUGE 3-5/8\" STEEL STUDS 16\" O.C. WITH LATERAL BRACING IN TWO ROWS 3\" APART" → two rows
  of studs (`rows`: 2) for A2-3D.
- Keynotes on A101 / enlarged plans that change board (A1.11, A1.13, A1.14 FRT plywood to 24" / 8' AFF; A1.15 impact
  gypsum board to 24"; A2.25 existing door opening infilled with metal and drywall) → record per face (zone height and
  source). FRT / oak plywood itself is EXCLUDED (wood).
- Openings: door R.O. from A601 schedule (door size + frame) with source; headers / sills are computed later by the tools.
- Backing / blocking from A103 (WALL BACKING PLAN) for walls of your sheet: `blocking_items[]` {wall, label (literal text),
  material: "metal" | "wood (EXCLUDED)", length_ft or qty, source}. Wood → EXCLUDED note, never a quantity.
- Do not compute studs, track, board SF or accessories — the tools do that from your canon.
