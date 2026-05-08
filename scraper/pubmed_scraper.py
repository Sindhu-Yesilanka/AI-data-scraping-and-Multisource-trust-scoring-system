from Bio import Entrez
import json

# -----------------------------------
# EMAIL REQUIRED BY NCBI
# -----------------------------------

Entrez.email = "sindhuyesilanka@gmail.com"

# -----------------------------------
# PUBMED ARTICLE ID
# -----------------------------------

pubmed_id = "38177566"

# -----------------------------------
# FETCH ARTICLE
# -----------------------------------

handle = Entrez.efetch(
    db="pubmed",
    id=pubmed_id,
    rettype="abstract",
    retmode="xml"
)

records = Entrez.read(handle)

article = records["PubmedArticle"][0]

# -----------------------------------
# EXTRACT METADATA
# -----------------------------------

article_data = article["MedlineCitation"]["Article"]

title = article_data["ArticleTitle"]

abstract = ""

if "Abstract" in article_data:

    abstract_sections = article_data["Abstract"]["AbstractText"]

    for section in abstract_sections:

        try:
            abstract += section + " "

        except:
            abstract += str(section) + " "

journal = article_data["Journal"]["Title"]

# -----------------------------------
# AUTHORS
# -----------------------------------

authors = []

if "AuthorList" in article_data:

    for author in article_data["AuthorList"]:

        if "LastName" in author and "ForeName" in author:

            full_name = (
                author["ForeName"] + " " +
                author["LastName"]
            )

            authors.append(full_name)

# -----------------------------------
# PUBLICATION YEAR
# -----------------------------------

publication_year = "Unknown"

try:

    publication_year = (
        article_data["Journal"]
        ["JournalIssue"]
        ["PubDate"]
        ["Year"]
    )

except:
    pass

# -----------------------------------
# PRINT OUTPUT
# -----------------------------------

print("\nTitle:")
print(title)

print("\nJournal:")
print(journal)

print("\nAuthors:")
print(authors)

print("\nPublication Year:")
print(publication_year)

print("\nAbstract Preview:")
print(abstract[:1000])

# -----------------------------------
# FINAL JSON OBJECT
# -----------------------------------

pubmed_json = {
    "source_type": "pubmed",
    "pubmed_id": pubmed_id,
    "title": title,
    "journal": journal,
    "authors": authors,
    "publication_year": publication_year,
    "abstract": abstract
}

# -----------------------------------
# SAVE JSON
# -----------------------------------

with open(
    "output/pubmed.json",
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        pubmed_json,
        json_file,
        indent=4,
        ensure_ascii=False
    )

print("\nPubMed JSON saved successfully!")
