"""Route-level tests for surface revisions: snapshot-on-edit, undo, restore, prune."""


def _home_blocks(client, auth):
    r = client.get("/api/admin/compose/home/blocks", headers=auth)
    assert r.status_code == 200
    return r.get_json()["item"]["blocks"]


def _types(blocks):
    return [b["type"] for b in blocks]


def test_compose_add_records_revision_and_undo_reverts(client, auth):
    start = _types(_home_blocks(client, auth))

    r = client.post("/api/admin/compose/home/blocks", json={"type": "faq"}, headers=auth)
    assert r.status_code == 201
    assert _types(_home_blocks(client, auth)).count("faq") == start.count("faq") + 1

    revs = client.get("/api/admin/revisions?target=home", headers=auth).get_json()["items"]
    assert len(revs) == 1
    assert revs[0]["surface"] == "home" and revs[0]["label"] == "add faq"

    u = client.post("/api/admin/undo", json={"target": "home"}, headers=auth)
    assert u.status_code == 200
    assert _types(_home_blocks(client, auth)) == start
    assert client.get("/api/admin/revisions?target=home", headers=auth).get_json()["items"] == []


def test_undo_with_no_history_is_404(client, auth):
    _home_blocks(client, auth)  # seed home but make no edits
    assert client.post("/api/admin/undo", json={"target": "home"}, headers=auth).status_code == 404


def test_design_theme_switch_undo(client, auth):
    a = client.post("/api/admin/design/generate", json={"preset": "minimal"}, headers=auth)
    assert a.status_code == 200
    name_a = a.get_json()["item"]["name"]
    # First generate creates the profile, so there is nothing prior to snapshot.
    assert client.get("/api/admin/revisions?target=design", headers=auth).get_json()["items"] == []

    b = client.post("/api/admin/design/generate", json={"preset": "restaurant"}, headers=auth)
    assert b.get_json()["item"]["name"] != name_a
    revs = client.get("/api/admin/revisions?target=design", headers=auth).get_json()["items"]
    assert len(revs) == 1 and revs[0]["kind"] == "design"

    client.post("/api/admin/undo", json={"target": "design"}, headers=auth)
    assert client.get("/api/admin/design", headers=auth).get_json()["item"]["name"] == name_a


def test_restore_specific_revision_by_id(client, auth):
    _home_blocks(client, auth)
    client.post("/api/admin/compose/home/blocks", json={"type": "faq"}, headers=auth)
    snap_after_faq = _types(_home_blocks(client, auth))
    client.post("/api/admin/compose/home/blocks", json={"type": "pricing"}, headers=auth)

    revs = client.get("/api/admin/revisions?target=home", headers=auth).get_json()["items"]
    assert len(revs) == 2  # newest first: [before pricing, before faq]
    rr = client.post(f"/api/admin/revisions/{revs[0]['id']}/restore", headers=auth)
    assert rr.status_code == 200
    assert _types(_home_blocks(client, auth)) == snap_after_faq  # pricing reverted, faq kept
    after = client.get("/api/admin/revisions?target=home", headers=auth).get_json()["items"]
    assert any(r["label"] == "before restore" for r in after)  # restore is itself undoable


def test_history_is_capped(client, auth):
    _home_blocks(client, auth)
    for _ in range(7):  # REVISION_HISTORY = 5 in TestConfig
        client.post("/api/admin/compose/home/blocks", json={"type": "cta"}, headers=auth)
    revs = client.get("/api/admin/revisions?target=home&limit=100", headers=auth).get_json()["items"]
    assert len(revs) == 5
