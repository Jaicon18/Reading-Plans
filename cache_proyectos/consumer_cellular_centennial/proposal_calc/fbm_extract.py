"""FBM (myfbm.com) category extraction over HTTP: the JSON embedded in self.__next_f.push of each category page
(precios-materiales-fbm skill, step 2). Guest branch CO-086 (Englewood / Denver) saved through the site's own API.
Usage: fbm_extract.py <out_dir> <CAT> [<CAT> ...]"""
import json, re, sys, time, http.cookiejar, urllib.request, concurrent.futures as cf
OUT, CATS = sys.argv[1], sys.argv[2:]
cj = http.cookiejar.MozillaCookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", "Mozilla/5.0 (takeoff price check)")]
def get(url, data=None):
    for k in range(4):
        try:
            rq = urllib.request.Request(url, data=data, headers={"content-type": "application/json"} if data else {})
            return op.open(rq, timeout=60).read().decode("utf-8", "replace")
        except Exception as e:
            err = e; time.sleep(2 * (k + 1))
    raise err
get("https://myfbm.com/")
print("branch save:", get("https://myfbm.com/api/commerce/fbm/saveGuestBranch",
      json.dumps([{"branchStore": "FBM", "isCart": True, "isCheckout": False, "posName": "86"}]).encode()))
def page(cat, n):
    t = get(f"https://myfbm.com/all-products/x/c/{cat}?sort=name-asc&page={n}")
    s = "".join(json.loads('"' + p + '"') for p in re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', t))
    i = s.find('"pagination":{'); pg, _ = json.JSONDecoder().raw_decode(s[i + len('"pagination":'):])
    j = s.find('"products":['); pr, _ = json.JSONDecoder().raw_decode(s[j + len('"products":'):])
    return pg, pr
KEEP = ("code", "name", "brandName", "manufactureId", "productCategory", "isBaseProduct", "unitLabel", "stockLevelStatus",
        "specialMessage", "minOrderQuantity", "url")
for cat in CATS:
    pg, pr0 = page(cat, 0)
    with cf.ThreadPoolExecutor(6) as ex:
        rest = list(ex.map(lambda n: page(cat, n)[1], range(1, pg["totalPages"])))
    rows = []
    for pr in [pr0] + rest:
        for p in pr:
            d = {k: p.get(k) for k in KEEP}
            d["price"] = (p.get("price") or {}).get("value")
            d["specialPrice"] = (p.get("specialPrice") or {}).get("value") if isinstance(p.get("specialPrice"), dict) else p.get("specialPrice")
            d["specialPriceUnit"] = p.get("specialPriceUnit")
            rows.append(d)
    codes = [r["code"] for r in rows]
    json.dump({"category": cat, "totalResults": pg["totalResults"], "rows": rows,
               "fecha": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}, open(f"{OUT}/{cat}.json", "w"), indent=0)
    print(cat, "total", pg["totalResults"], "extracted", len(rows), "unique", len(set(codes)), "no price", sum(r["price"] is None for r in rows))
