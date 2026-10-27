"""Read-only Qloo probes. Secrets come only from QLOO_API_KEY; no raw payloads saved."""
import argparse
import collections
import concurrent.futures
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://hackathon.api.qloo.com"


def query(path, params):
    started = time.monotonic()
    req = urllib.request.Request(
        BASE + path + "?" + urllib.parse.urlencode(params),
        headers={"X-Api-Key": os.environ["QLOO_API_KEY"], "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            data = json.load(response)
            return {"http": response.status, "seconds": round(time.monotonic()-started, 2)}, data
    except urllib.error.HTTPError as exc:
        return {"http": exc.code, "error": "HTTP failure; no response or credentials logged"}, {}
    except Exception as exc:
        return {"http": None, "error": type(exc).__name__}, {}


def entities(data):
    results = data.get("results", {})
    return results.get("entities", []) if isinstance(results, dict) else []


def tag_id(tag):
    return tag.get("id") or tag.get("tag_id") or tag.get("value")


def is_restaurant(row):
    primary = (row.get("properties") or {}).get("primary_genre") or {}
    primary_id = primary.get("id", "") if isinstance(primary, dict) else ""
    return primary_id == "urn:tag:genre:place:restaurant" or primary_id.startswith("urn:tag:genre:place:restaurant:")


def summarize(rows):
    metadata = {k: 0 for k in ["phone", "address", "website", "image", "hours", "price_level", "menu_url", "google_place_id"]}
    genres = collections.Counter()
    restaurant = hotel = 0
    for row in rows:
        props = row.get("properties") or {}
        for k in metadata:
            if k != "google_place_id" and props.get(k):
                metadata[k] += 1
        external = row.get("external") or {}
        gp = external.get("google_place") or []
        if isinstance(gp, dict):
            gp = [gp]
        if any(isinstance(item, dict) and item.get("place_id") for item in gp):
            metadata["google_place_id"] += 1
        primary = props.get("primary_genre")
        primary_label = (primary.get("name") or primary.get("id")) if isinstance(primary, dict) else primary
        genres[str(primary_label)] += 1
        ids = [str(tag_id(t) or "") for t in row.get("tags", [])]
        restaurant += any(":restaurant" in t or t.endswith(":restaurants") for t in ids)
        hotel += any(t.endswith(":hotel") or ":hotel:" in t for t in ids)
    return {"count": len(rows), "metadata_nonempty": metadata, "primary_genres": dict(genres), "with_restaurant_tag": restaurant, "with_hotel_tag": hotel}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["discovery", "matrix", "followup", "final", "repeatability"])
    parser.add_argument("--restaurant-tag")
    parser.add_argument("--output")
    args = parser.parse_args()
    if not os.environ.get("QLOO_API_KEY"):
        raise SystemExit("Set QLOO_API_KEY in the process environment.")
    if args.phase == "discovery":
        terms = ["restaurant", "quiet", "romantic", "vegan", "Italian", "Japanese", "Turkish", "halal", "outdoor"]
        def find(term):
            meta, data = query("/v2/tags", {"filter.query": term, "take": 25})
            tags = data.get("results", {}).get("tags", [])
            tags = [{"name": t.get("name"), "id": tag_id(t)} for t in tags if any(p.get("type") == "urn:entity:place" for p in t.get("parents", []))]
            return {"term": term, **meta, "place_tags": tags}
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(find, terms))
        output = {"phase": "discovery", "calls": len(terms), "results": results}
    elif args.phase == "matrix":
        rt = args.restaurant_tag
        if not rt:
            raise SystemExit("Supply a restaurant tag observed in discovery.")
        tags = {
            "quiet": "urn:tag:ambience:qloo:quiet",
            "romantic": "urn:tag:ambience:qloo:romantic",
            "vegan_option": "urn:tag:dietary_option:qloo:vegan",
            "vegan_restaurant": "urn:tag:category:place:vegan_restaurant",
            "italian": "urn:tag:genre:place:restaurant:italian",
        }
        cases = []
        def add(label, city, extra=None):
            params = {"filter.type": "urn:entity:place", "filter.location.query": city, "filter.tags": rt, "take": 10}
            params.update(extra or {})
            cases.append((label, params))
        for city in ["Istanbul", "Rome", "Mumbai"]:
            add(city + "/baseline", city)
        for city in ["Istanbul", "Rome", "Mumbai"]:
            for label in ["quiet", "romantic", "vegan_option", "italian"]:
                add(city+"/"+label, city, {"filter.tags": rt+","+tags[label], "operator.filter.tags": "intersection"})
        add("Rome/soft_quiet", "Rome", {"signal.interests.tags": tags["quiet"]})
        add("Mumbai/vegan_restaurant", "Mumbai", {"filter.tags": rt+","+tags["vegan_restaurant"], "operator.filter.tags": "intersection"})
        add("Rome/budget_max2", "Rome", {"filter.price_level.max": 2})
        add("Rome/contradictory_tags", "Rome", {"filter.exclude.tags": rt})
        row_cache = {}
        def probe(case):
            label, params = case
            meta, data = query("/v2/insights", params)
            rows = entities(data)
            row_cache[label] = rows
            warnings = data.get("warnings") or data.get("query", {}).get("warnings")
            result = {"case": label, "params": params, **meta, "success": data.get("success"), **summarize(rows)}
            requested = params.get("filter.tags", "").split(",")
            result["requested_tag_membership"] = {tag: sum(tag in {tag_id(t) for t in r.get("tags", [])} for r in rows) for tag in requested}
            if warnings:
                result["warning_present"] = True
            return result
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(probe, cases))
        comparisons = []
        for label, _ in cases:
            city = label.split("/")[0]
            base = row_cache.get(city+"/baseline", [])
            current = row_cache[label]
            ids = lambda rows: [r.get("entity_id") or r.get("id") for r in rows]
            if label.endswith("/baseline"):
                continue
            a, b = ids(base), ids(current)
            comparisons.append({"case": label, "baseline": city+"/baseline", "shared_ids": len(set(a)&set(b)), "same_order": a == b})
        output = {"phase": "matrix", "calls": len(cases), "sample_limit": 10, "results": results, "comparisons": comparisons}
    elif args.phase == "followup":
        restaurant = "urn:tag:genre:place:restaurant"
        tag_meta, hotel_data = query("/v2/tags", {"filter.query": "hotel", "take": 10})
        hotel_tags = [{"name": t.get("name"), "id": tag_id(t)} for t in hotel_data.get("results", {}).get("tags", []) if t.get("name", "").lower() == "hotel"]
        expected = "urn:tag:genre:place:hotel"
        if expected not in {t["id"] for t in hotel_tags}:
            raise SystemExit("Hotel exclusion tag not discovered; inspect tag semantics first.")
        results = []
        baseline_cache = {}
        for city in ["Istanbul", "Rome", "Mumbai"]:
            params = {"filter.type": "urn:entity:place", "filter.location.query": city, "filter.tags": restaurant, "filter.exclude.tags": expected, "take": 10}
            meta, data = query("/v2/insights", params)
            rows = entities(data)
            baseline_cache[city] = rows
            results.append({"case": city+"/exclude_hotel", "params": params, **meta, **summarize(rows), "exact_excluded_tag_present": sum(expected in {tag_id(t) for t in r.get("tags", [])} for r in rows)})
        params = {"filter.type": "urn:entity:place", "filter.location.query": "Mumbai", "filter.tags": restaurant+",urn:tag:category:place:vegan_restaurant", "operator.filter.tags": "intersection", "take": 1}
        meta, data = query("/v2/insights", params)
        vegan_seed = entities(data)
        results.append({"case": "seed_lookup_vegan", **meta, "count": len(vegan_seed)})
        source_rows = [baseline_cache["Mumbai"][0:1], vegan_seed]
        ids = lambda rows: [r.get("entity_id") or r.get("id") for r in rows]
        base_ids = ids(baseline_cache["Rome"])
        seed_id_values = []
        for index, rows in enumerate(source_rows):
            if not rows:
                results.append({"case": "Rome/entity_signal_"+str(index+1), "blocked": "No seed entity"})
                continue
            seed = ids(rows)[0]
            seed_id_values.append(seed)
            params = {"filter.type": "urn:entity:place", "filter.location.query": "Rome", "filter.tags": restaurant, "filter.exclude.tags": expected, "signal.interests.entities": seed, "take": 10}
            meta, data = query("/v2/insights", params)
            target = entities(data)
            results.append({"case": "Rome/entity_signal_"+str(index+1), "seed_source": "Mumbai restaurant sample "+str(index+1), **meta, **summarize(target), "overlap_with_same_filter_baseline": len(set(base_ids)&set(ids(target))), "same_order_as_baseline": base_ids == ids(target)})
        results.append({"case": "seed_distinctness", "distinct": len(set(seed_id_values)) == 2})
        output = {"phase": "followup", "calls": 7, "hotel_tag_lookup": {**tag_meta, "matching_tags": hotel_tags}, "results": results}
    elif args.phase == "final":
        category = "urn:tag:category:place:restaurant"
        cases = [(city+"/category", {"filter.type":"urn:entity:place", "filter.location.query":city, "filter.tags":category,"take":10}) for city in ["Istanbul","Rome","Mumbai"]]
        extra = {"outdoor":"urn:tag:service_options:place:outdoor_seating", "halal":"urn:tag:dietary_option:qloo:halal", "japanese":"urn:tag:genre:place:restaurant:japanese"}
        for name, tag in extra.items():
            cases.append(("Rome/"+name, {"filter.type":"urn:entity:place", "filter.location.query":"Rome", "filter.tags":category+","+tag,"operator.filter.tags":"intersection","take":10}))
        cache = {}
        results=[]
        for label, params in cases:
            meta,data=query("/v2/insights",params)
            rows=entities(data); cache[label]=rows
            clean=[r for r in rows if is_restaurant(r)]
            results.append({"case":label,"params":params,**meta,**summarize(rows),"primary_restaurant_count":len(clean),"primary_restaurant_metadata":summarize(clean)["metadata_nonempty"],"requested_tag_membership":{tag:sum(tag in {tag_id(t) for t in row.get("tags",[])} for row in rows) for tag in params['filter.tags'].split(',')}})
        _,data=query("/v2/insights",{"filter.type":"urn:entity:place","filter.location.query":"Mumbai","filter.tags":"urn:tag:genre:place:restaurant,urn:tag:category:place:vegan_restaurant","operator.filter.tags":"intersection","take":5})
        seeds = [next((r for r in cache['Mumbai/category'] if is_restaurant(r)),None),next((r for r in entities(data) if is_restaurant(r)),None)]
        target_ids=[]
        for i,seed in enumerate(seeds):
            if seed is None:
                results.append({"case":"Rome/clean_entity_"+str(i+1),"blocked":"No primary restaurant seed"});continue
            seed_id=seed.get('entity_id') or seed.get('id')
            params={"filter.type":"urn:entity:place","filter.location.query":"Rome","filter.tags":category,"signal.interests.entities":seed_id,"take":10}
            meta,data=query('/v2/insights',params); rows=entities(data)
            ids=[r.get('entity_id') or r.get('id') for r in rows];target_ids.append(ids)
            results.append({"case":"Rome/clean_entity_"+str(i+1),"seed_primary_category":(seed.get('properties') or {}).get('primary_genre',{}).get('name'),**meta,**summarize(rows),"primary_restaurant_count":sum(is_restaurant(r) for r in rows)})
        if len(target_ids)==2:
            results.append({"case":"clean_entity_comparison","same_order":target_ids[0]==target_ids[1],"shared_ids":len(set(target_ids[0])&set(target_ids[1]))})
        output={"phase":"final","calls":9,"results":results}
    else:
        import hashlib
        category = "urn:tag:category:place:restaurant"
        base = {"filter.type":"urn:entity:place","filter.location.query":"Mumbai","filter.tags":category,"take":10}
        m1,d1=query('/v2/insights',base)
        m2,d2=query('/v2/insights',{**base,"filter.tags":category+",urn:tag:category:place:vegan_restaurant","operator.filter.tags":"intersection"})
        sources1=[r for r in entities(d1) if is_restaurant(r)]
        sources2=[r for r in entities(d2) if is_restaurant(r)]
        rid=lambda r:r.get('entity_id') or r.get('id')
        if not sources1:
            raise SystemExit('No suitable first seed')
        seed1=rid(sources1[0]); seed2=next((rid(r) for r in sources2 if rid(r)!=seed1),None)
        if not seed2:
            raise SystemExit('No distinct suitable second seed')
        ids=[];results=[]
        for label,seed in [('seed1_first',seed1),('seed1_repeat',seed1),('seed2',seed2)]:
            params={"filter.type":"urn:entity:place","filter.location.query":"Rome","filter.tags":category,"signal.interests.entities":seed,"take":10}
            meta,data=query('/v2/insights',params);rows=entities(data); current=[rid(r) for r in rows];ids.append(current)
            results.append({"case":label,"seed_fingerprint":hashlib.sha256(seed.encode()).hexdigest()[:12],**meta,"count":len(rows),"primary_restaurant_count":sum(is_restaurant(r) for r in rows)})
        output={"phase":"repeatability","calls":5,"seed_lookup_http":[m1.get('http'),m2.get('http')],"distinct_seeds":seed1!=seed2,"same_seed_identical_order":ids[0]==ids[1],"different_seed_identical_order":ids[0]==ids[2],"different_seed_shared_ids":len(set(ids[0])&set(ids[2])),"results":results}
    if args.output:
        from pathlib import Path
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    # Windows console encodings must not turn a completed probe into a print failure.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
