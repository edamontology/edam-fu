"""
cli.py
Authors: Alban Gaignard, Hervé Ménager 
Email: alban.gaignard@univ-nantes.fr
Date: 2023-05-31
Description: This script compares two RDF files and outputs the differences.

The MIT License (MIT)
"""

from rdflib import ConjunctiveGraph, Namespace
from rdflib.compare import to_isomorphic, graph_diff, to_canonical_graph
from rdflib.util import guess_format
import difflib
import sys

from rich.progress import Progress
from rich.console import Console

import click

_UNSTABLE_EDAM = "https://edamontology.org/EDAM_unstable.owl"
_STABLE_EDAM = "https://edamontology.org/EDAM.owl"

# kg_ref = ConjunctiveGraph().parse(_STABLE_EDAM)
# to_canonical_graph(kg_ref).serialize("edam_ref.ttl", format="turtle")
# to_canonical_graph(kg_ref).serialize("edam_ref.owl", format="xml")
# sys.exit(0)

console = Console()


def reformat_edam_txt(input_file, output_file):
    console.print(f"Reformatting {input_file}")
    kg = ConjunctiveGraph().parse(input_file)
    kg.serialize(format="turtle")


def diff_edam_txt(rdf_1, rdf_2):
    console.print(f"Diffing {rdf_1} with {rdf_2}")
    with Progress() as progress:
        task1 = progress.add_task("[red]Computing diff ...", total=5)
        while not progress.finished:
            kg_1 = ConjunctiveGraph().parse(rdf_1)
            progress.update(task1, advance=1)
            progress.refresh()

            kg_2 = ConjunctiveGraph().parse(rdf_2)
            progress.update(task1, advance=2)
            progress.refresh()

            kg_1_ttl = to_canonical_graph(kg_1).serialize(format="turtle")
            progress.update(task1, advance=3)
            progress.refresh()

            kg_2_ttl = to_canonical_graph(kg_2).serialize(format="turtle")
            progress.update(task1, advance=4)
            progress.refresh()

            diff_output = difflib.unified_diff(
                kg_1_ttl.splitlines(keepends=True),
                kg_2_ttl.splitlines(keepends=True),
                n=3,
            )
            progress.update(task1, advance=5)
            progress.refresh()

        for line in diff_output:
            if line.startswith("+"):
                console.print("[green]" + line.strip())
            elif line.startswith("-"):
                console.print("[red]" + line.strip())
            else:
                console.print("[white]" + line.strip())

    # _ , in_first, in_second = graph_diff(kg_1, kg_2)
    # console.print("[bold]In first version:")
    # console.print(in_first.serialize(format="turtle"))
    # console.print("[bold]In second version:")
    # console.print(in_second.serialize(format="turtle"))


# @click.command()
# @click.option("--src", required=True, help="your input EDAM ontology.")
# @click.option("--ref", required=True, help="the reference EDAM ontology.")
# def diff_command(src, ref):
#     """Simple program that prints a diff between two EDAM ontologies."""
#     console.print("[bold]EDAM Diff Tool")
#     console.print("[bold]-----------------")

#     guess_format("src")
#     diff_edam_txt(src, ref)


# @click.command("black")
@click.command()
@click.option(
    "--check", is_flag=True, help="Verify if the input file is correctly formatted."
)
@click.option("--diff", is_flag=True, help="Display the differences.")
@click.option("--reformat", is_flag=True, help="Reformat the input file.")
@click.argument("input_filename", type=click.Path(exists=True))
@click.argument("output_filename", type=click.Path(exists=False), required=False)
def fu_command(check, diff, reformat, input_filename, output_filename):
    """EDAM ontology reformatting tool.

    Example:\n
        python edamfu/cli.py --check tests/EDAM_min.ttl\n
        python edamfu/cli.py --check tests/EDAM_min_mod.ttl\n
        python edamfu/cli.py --check --diff tests/EDAM_min_mod.ttl\n
        python edamfu/cli.py --reformat tests/EDAM_min_mod.ttl\n
    """
    # console.print("[bold]EDAM Formatting Utility")
    # console.print("[bold]-----------------------")

    rdf_format = guess_format(input_filename)
    # console.print(f"{input_filename} format: {rdf_format}")
    if not rdf_format in ["xml", "turtle"]:
        sys.exit(2)
    else:
        # console.print(f"Checking {input_filename}")
        with open(input_filename, "r") as f:
            content = f.readlines()
            kg = ConjunctiveGraph().parse(input_filename)

            edam_ns = Namespace("http://edamontology.org/")
            obo_ns = Namespace("http://www.geneontology.org/formats/oboInOwl#")
            dc_ns = Namespace("http://purl.org/dc/elements/1.1/")
            dcterms_ns = Namespace("http://purl.org/dc/terms/")
            owl_ns = Namespace("http://www.w3.org/2002/07/owl#")
            rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
            skos_ns = Namespace("http://www.w3.org/2004/02/skos/core#")
            xml_ns = Namespace("http://www.w3.org/XML/1998/namespace")
            xsd_ns = Namespace("http://www.w3.org/2001/XMLSchema#")
            doap_ns = Namespace("http://usefulinc.com/ns/doap#")
            foaf_ns = Namespace("http://xmlns.com/foaf/0.1/")
            rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")
            oboInOwl_ns = Namespace("http://www.geneontology.org/formats/oboInOwl#")
            oboLegacy_ns = Namespace("http://purl.obolibrary.org/obo/")

            kg.bind("", edam_ns, override=True, replace=True)
            kg.bind("obo", obo_ns, override=True, replace=True)
            kg.bind("dc", dc_ns, override=True, replace=True)
            kg.bind("dcterms", dcterms_ns, override=True, replace=True)
            kg.bind("owl", owl_ns, override=True, replace=True)
            kg.bind("rdf", rdf_ns, override=True, replace=True)
            kg.bind("skos", skos_ns, override=True, replace=True)
            kg.bind("xml", xml_ns, override=True, replace=True)
            kg.bind("xsd", xsd_ns, override=True, replace=True)
            kg.bind("doap", doap_ns, override=True, replace=True)
            kg.bind("foaf", foaf_ns, override=True, replace=True)
            kg.bind("rdfs", rdfs_ns, override=True, replace=True)
            kg.bind("oboInOwl", oboInOwl_ns, override=True, replace=True)
            kg.bind("oboLegacy", oboLegacy_ns, override=True, replace=True)

            kg_normalized_txt = kg.serialize(format=rdf_format)
            diff_output = difflib.unified_diff(
                content, kg_normalized_txt.splitlines(keepends=True), n=3
            )

            if check:
                nb_diff = 0
                # console.print("[bold]Diff " + filename)
                for line in diff_output:
                    if line.startswith("+"):
                        if diff:
                            console.print("[green]" + line.strip())
                        nb_diff += 1
                    elif line.startswith("-"):
                        if diff:
                            console.print("[red]" + line.strip())
                        nb_diff += 1
                    else:
                        if diff:
                            console.print("[white]" + line.strip())
                if nb_diff == 0:
                    console.print(
                        ":smiley:", "[bold]No reformatting needed for " + input_filename
                    )
                    sys.exit(0)
                else:
                    console.print(
                        "[bold]Found "
                        + str(nb_diff)
                        + " differences in "
                        + input_filename,
                    )
                    sys.exit(1)

            if reformat:
                if output_filename:
                    out_format = rdf_format
                    if rdf_format == "xml":
                        out_format = "pretty-xml"
                    console.print("[bold]Reformated EDAM to " + output_filename)
                    kg.serialize(destination=output_filename, format=out_format)
                    sys.exit(0)
                else:
                    console.print("[bold red]Please specify an output file.")
                    sys.exit(2)


# @click.group()
# def entry_point():
#    pass


# entry_point.add_command(fu_command)
# entry_point.add_command(diff_command)

if __name__ == "__main__":
    # entry_point()
    fu_command()
