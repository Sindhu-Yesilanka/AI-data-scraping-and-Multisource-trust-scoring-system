from Bio import Entrez
import json

from scoring.trust_score import (
    get_author_score,
    get_domain_score,
    get_recency_score,
    get_citation_score,
    get_disclaimer_score,
    calculate_trust_score
)

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
# EXTRACT ARTICLE DATA
# -----------------------------------

article_data = article["MedlineCitation"]["Article"]

# -----------------------------------
# TITLE
# -----------------------------------

title = str(article_data["ArticleTitle"])

# -----------------------------------
# ABSTRACT
# -----------------------------------

abstract = ""

if "Abstract" in article_data:

    abstract_sections = (
        article_data["Abstract"]["AbstractText"]
    )

    for section in abstract_sections:

        abstract += str(section) + " "

# -----------------------------------
# JOURNAL
# -----------------------------------

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
# TRUST SCORE CALCULATION
# -----------------------------------

author_name = "PubMed Research"

author_score = get_author_score(author_name)

domain_score = get_domain_score(
    "https://pubmed.ncbi.nlm.nih.gov"
)

try:
    recency_score = get_recency_score(
        int(publication_year)
    )

except:
    recency_score = 0.50

citation_count = abstract.lower().count("study")

citation_score = get_citation_score(
    citation_count
)

disclaimer_score = get_disclaimer_score(
    abstract
)

trust_score = calculate_trust_score(
    author_score,
    citation_score,
    domain_score,
    recency_score,
    disclaimer_score
)

print("\nTrust Score:")
print(trust_score)

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
    "abstract": abstract,
    "trust_score": trust_score
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