from argparse import ArgumentParser, ArgumentTypeError
from lxml import etree
from pathlib import Path
from rdflib import BNode, Graph, Literal, Namespace
from rdflib.namespace import RDF
from typing import Union


global_cfg = None


def is_valid_file(path: str) -> Path:
    """Checks if given path is a file or not.
    Returns pathlib.Path object or raises ArgumentTypeError
    if not a valid path to a file.
    """
    pathObj = Path(path)
    if pathObj.is_file():
        return pathObj
    else:
        raise ArgumentTypeError(f"{path} is not a file")


def init_argparse() -> ArgumentParser:
    """Initializes ArgumentParser object."""
    ps = ArgumentParser(
        description="""
Converts striped XML to Turtle format.
""")
    ps.add_argument(
        "xmlFile",
        help="Path to XML file to be converted",
        type=is_valid_file
    )
    ps.add_argument(
        "--serializePath",
        help="""
Path to where the serialized graph should be saved.
Graph is printed if not provided.
        """
    )
    ps.add_argument(
        "--outputFormat",
        default="turtle",
        const="turtle",
        nargs="?",
        choices=(
            "xml", "n3", "turtle",
            "nt", "pretty-xml", "trig",
            "json-ld", "hext"
        ),
        help="""
The format that the graph should be output as.
rdflib built-in choices include "xml", "n3", "turtle" (default),
 "nt", "pretty-xml", "trig", "json-ld", and "hext".
        """
    )
    ps.add_argument(
        "--collectAttributes",
        action="store_true",
        help="""
Collect attributes from the XML document if set.
Attributes take on the namespace of the tag they were found in.
"""
    )
    ps.add_argument(
        "--noIgnoreWhitespace",
        action="store_false",
        help="""
Do not ignore whitespace. Prettified XML documents have
whitespace in them and will be converted if not ignored.
"""
    )
    ps.add_argument(
        "--defaultNamespace",
        nargs=2,
        default=("ex", "http://example.org/#"),
        help="""
Set a default prefix and namespace to be used if namespaces
are not found in the XML document.
Default prefix and URI are 'ex' and 'http://example.org/#'.
        """
    )
    return ps


def populate_namespaces(nsMap: dict, namespaces: dict, graph: Graph) -> None:
    """
    Populate the namespaces dictionary with a
    namespace URI to rdflib.Namespace mapping
    and binds the created rdflib.Namespace to the graph.
    """
    for prefix, uri in nsMap.items():
        correctURI = uri
        if uri[-1] != "#":
            correctURI = uri + "#"
        namespaces[uri] = Namespace(correctURI)
        graph.bind(prefix, namespaces[uri], override=False)


def parse_qname(element) -> Union[str, str]:
    """Parse QName string from lxml element.
    Returns a tuple of strings, the namespace URI and element name.
    """
    elQName = etree.QName(element)
    return (elQName.namespace, elQName.localname)


def generate_triple(
    currentElement,
    parentElement,
    parentNode: BNode,
    isNode: bool,
    namespaces: dict,
    graph: Graph) -> \
        None:
    """Generate triple from current element."""
    namespaceURI, elName = parse_qname(currentElement)
    if namespaceURI not in namespaces:
        populate_namespaces(currentElement.nsmap, namespaces, graph)
    namespace = namespaces.get(namespaceURI)
    if namespace is None:
        namespace = namespaces.get(global_cfg.defaultNamespace[1])
    if global_cfg.collectAttributes:
        for attribute, value in currentElement.attrib.items():
            if not attribute.isalnum():
                continue
            graph.add((
                parentNode,
                namespace[attribute],
                Literal(value)
            ))
    if isNode:
        currentNode = BNode()
        if parentNode and parentElement is not None:
            parentNSURI, parentElName = parse_qname(parentElement)
            if parentNSURI not in namespaces:
                populate_namespaces(parentElement.nsmap, namespaces, graph)
            parentNamespace = namespaces.get(parentNSURI)
            if parentNamespace is None:
                defaulNamespaceURI = global_cfg.defaultNamespace[1]
                parentNamespace = namespaces.get(defaulNamespaceURI)
            if len(currentElement) == 0:
                graph.add((
                    parentNode,
                    parentNamespace[parentElName],
                    Literal(currentElement.text)
                ))
                return
            graph.add((
                parentNode,
                parentNamespace[parentElName],
                currentNode
            ))
        graph.add((
            currentNode,
            RDF.type,
            namespace[elName]
        ))
        for childElement in currentElement:
            generate_triple(
                childElement,
                currentElement,
                currentNode,
                not isNode,
                namespaces,
                graph
            )
    if not isNode:
        if currentElement.text:
            graph.add((
                parentNode,
                namespace[elName],
                Literal(currentElement.text)
            ))
        for childElement in currentElement:
            generate_triple(
                childElement,
                currentElement,
                parentNode,
                not isNode,
                namespaces,
                graph
            )


def convert_xml_and_serialize(filePath: str) -> None:
    """Read XML, create triples, and serialize."""
    xmlParser = etree.XMLParser(
        remove_comments=True,
        no_network=True,
        remove_blank_text=global_cfg.noIgnoreWhitespace
    )
    tree = etree.parse(filePath, xmlParser)
    graph = Graph()
    namespaces = {}
    defaultPrefix = global_cfg.defaultNamespace[0]
    defaltNamespaceURI = global_cfg.defaultNamespace[1]
    populate_namespaces(
        {defaultPrefix: defaltNamespaceURI},
        namespaces,
        graph
    )
    generate_triple(
        tree.getroot(),
        None,
        None,
        True,
        namespaces,
        graph
    )
    print(graph.serialize(
        destination=global_cfg.serializePath,
        format=global_cfg.outputFormat
    ))


if __name__ == "__main__":
    parser = init_argparse()
    global_cfg = parser.parse_args()
    convert_xml_and_serialize(global_cfg.xmlFile)
