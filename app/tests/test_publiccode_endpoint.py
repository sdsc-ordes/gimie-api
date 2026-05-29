from fastapi.testclient import TestClient
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

import app.main as main
from gimie.graph.namespaces import SDO


def _fake_graph() -> Graph:
    g = Graph()
    s = URIRef("https://github.com/org/repo")
    g.add((s, RDF.type, SDO.SoftwareSourceCode))
    g.add((s, SDO.name, Literal("org/repo")))
    g.add((s, SDO.description, Literal("A test repository")))
    g.add((s, SDO.license, URIRef("https://spdx.org/licenses/MIT.html")))
    return g


def test_publiccode_endpoint_returns_mapped_object(monkeypatch):
    class FakeProject:
        def __init__(self, url):
            self.url = url

        def extract(self):
            return _fake_graph()

    monkeypatch.setattr(main, "Project", FakeProject)

    client = TestClient(main.app)
    res = client.get("/publiccode/https://github.com/org/repo")

    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "repo"
    assert data["url"] == "https://github.com/org/repo"
    assert data["legal"]["license"] == "MIT"
    assert data["description"]["en"]["shortDescription"] == "A test repository"


def test_publiccode_endpoint_returns_502_on_failure(monkeypatch):
    class BoomProject:
        def __init__(self, url):
            pass

        def extract(self):
            raise RuntimeError("extraction failed")

    monkeypatch.setattr(main, "Project", BoomProject)

    client = TestClient(main.app)
    res = client.get("/publiccode/https://github.com/org/repo")

    assert res.status_code == 502
    assert "error" in res.json()
