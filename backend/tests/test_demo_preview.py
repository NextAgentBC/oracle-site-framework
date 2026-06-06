"""Whole-site industry preview from bundled demo packs: localized home (keeps the
bundled photo) + nav pages + page bodies + a site identity override — all
non-destructive (no DB writes)."""


def test_preview_zh_is_whole_site_and_localized(client):
    r = client.get("/api/design/preview?industry=education&locale=zh").get_json()
    assert r["site"]["industry"] == "education"
    assert r["site"]["name"]                 # zh brand present
    hero = r["item"]["sections"][0]["content"]
    assert (hero.get("image") or "").startswith("/demo/")   # zh home keeps the bundled photo
    pages = client.get("/api/pages/preview?industry=education&locale=zh").get_json()["items"]
    assert {"about", "services"} <= {p["slug"] for p in pages}
    pg = client.get("/api/pages/preview/about?industry=education&locale=zh").get_json()["item"]
    assert pg["bodyMarkdown"].strip()        # localized page body, non-empty


def test_preview_en_uses_template(client):
    r = client.get("/api/design/preview?industry=restaurant").get_json()
    assert r["site"]["industry"] == "restaurant"
    assert r["item"]["sections"]             # full template home


def test_preview_unknown_industry_is_safe(client):
    res = client.get("/api/design/preview?industry=does-not-exist&locale=zh")
    assert res.status_code == 200            # graceful, no crash
    assert client.get("/api/pages/preview/about?industry=does-not-exist").status_code == 404
