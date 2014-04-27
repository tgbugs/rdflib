from rdflib import Graph, URIRef, BNode, RDF, Literal
from rdflib.collection import Collection
from rdflib.py3compat import b


def testTurtleFinalDot(): 
    """
    https://github.com/RDFLib/rdflib/issues/282
    """

    g = Graph()
    u = URIRef("http://ex.org/bob.")
    g.bind("ns", "http://ex.org/")
    g.add( (u, u, u) )
    s=g.serialize(format='turtle')
    assert b("ns:bob.") not in s


def testTurtleBoolList():
    subject = URIRef("http://localhost/user")
    predicate = URIRef("http://localhost/vocab#hasList")
    g1 = Graph()
    list_item1 = BNode()
    list_item2 = BNode()
    list_item3 = BNode()
    g1.add((subject, predicate, list_item1))
    g1.add((list_item1, RDF.first, Literal(True)))
    g1.add((list_item1, RDF.rest, list_item2))
    g1.add((list_item2, RDF.first, Literal(False)))
    g1.add((list_item2, RDF.rest, list_item3))
    g1.add((list_item3, RDF.first, Literal(True)))
    g1.add((list_item3, RDF.rest, RDF.nil))

    ttl_dump = g1.serialize(format="turtle")
    g2 = Graph()
    g2.parse(data=ttl_dump, format="turtle")

    list_id = g2.value(subject, predicate)
    bool_list = [i.toPython() for i in Collection(g2, list_id)]
    assert bool_list == [True, False, True]


if __name__ == "__main__":
    import nose, sys
    nose.main(defaultTest=sys.argv[0])
