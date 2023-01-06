from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import pandas as pd


def parse_bibtex(cols, file='bibliography.bib'):

    with open(file) as bibtex_file:
        bibtex_str = bibtex_file.read()

    parser = BibTexParser()
    parser.customization = convert_to_unicode
    bib_database = parser.parse(bibtex_str)

    entries = bib_database.entries_dict
    # We want only file name, not local Zotero storage path:
    for key in entries.keys():
        try:
            entries[key]['file'] = entries[key]['file'].split("/")[-1]
        # If no file is stored, skip this:
        except KeyError:
            pass

    bib_df = pd.DataFrame.from_dict(entries).T.set_index("title")
    bib_df = bib_df[[c for c in cols if c in bib_df.columns]]
    
    return bib_df