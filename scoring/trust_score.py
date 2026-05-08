from datetime import datetime


# -----------------------------------
# AUTHOR SCORE
# -----------------------------------

def get_author_score(author_name):

    trusted_authors = [
        "Stanford",
        "NIH",
        "WHO",
        "OpenAI",
        "Google",
        "Microsoft",
        "PubMed"
    ]

    if not author_name:
        return 0.30

    for trusted in trusted_authors:

        if trusted.lower() in author_name.lower():
            return 0.95

    return 0.60


# -----------------------------------
# DOMAIN SCORE
# -----------------------------------

def get_domain_score(url):

    trusted_domains = [
        ".gov",
        ".edu",
        "stanford",
        "nih",
        "who.int",
        "pubmed"
    ]

    medium_trust_domains = [
        "medium",
        "towardsdatascience",
        "infermedica"
    ]

    lower_url = url.lower()

    for domain in trusted_domains:

        if domain in lower_url:
            return 0.95

    for domain in medium_trust_domains:

        if domain in lower_url:
            return 0.75

    return 0.50


# -----------------------------------
# RECENCY SCORE
# -----------------------------------

def get_recency_score(publication_year):

    current_year = datetime.now().year

    age = current_year - publication_year

    if age <= 1:
        return 0.95

    elif age <= 3:
        return 0.80

    elif age <= 5:
        return 0.60

    else:
        return 0.40


# -----------------------------------
# CITATION SCORE
# -----------------------------------

def get_citation_score(citation_count):

    if citation_count >= 10:
        return 0.95

    elif citation_count >= 5:
        return 0.80

    elif citation_count >= 1:
        return 0.60

    else:
        return 0.30


# -----------------------------------
# DISCLAIMER SCORE
# -----------------------------------

def get_disclaimer_score(article_text):

    disclaimer_keywords = [
        "consult your doctor",
        "medical advice",
        "not a substitute",
        "healthcare professional",
        "for informational purposes"
    ]

    lower_text = article_text.lower()

    for keyword in disclaimer_keywords:

        if keyword in lower_text:
            return 0.90

    return 0.50


# -----------------------------------
# FINAL TRUST SCORE
# -----------------------------------

def calculate_trust_score(
    author_score,
    citation_score,
    domain_score,
    recency_score,
    disclaimer_score
):

    final_score = (
        0.30 * author_score +
        0.25 * citation_score +
        0.20 * domain_score +
        0.15 * recency_score +
        0.10 * disclaimer_score
    )

    return round(final_score, 2)