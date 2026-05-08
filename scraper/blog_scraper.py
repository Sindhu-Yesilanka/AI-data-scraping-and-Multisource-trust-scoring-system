import requests
from bs4 import BeautifulSoup
from langdetect import detect
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
# BLOG URLS
# -----------------------------------

blog_urls = [
    "https://hai.stanford.edu/news/how-do-we-ensure-healthcare-ai-useful",

    "https://infermedica.com/blog/articles/the-future-of-virtual-triage-and-care-navigation-software-where-ai-meets-the-human-touch",

    "https://medium.com/@noe7486/healthcare-is-driving-u-s-job-growth-ai-is-accelerating-that-shift-fc4c733ba3a0"
]

# -----------------------------------
# STORE ALL BLOG DATA
# -----------------------------------

all_blog_data = []

# -----------------------------------
# LOOP THROUGH URLS
# -----------------------------------

for url in blog_urls:

    print("\n==============================")
    print("Processing URL:")
    print(url)
    print("==============================")

    # -----------------------------------
    # SEND REQUEST
    # -----------------------------------

    response = requests.get(url)

    print("Status Code:", response.status_code)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    # -----------------------------------
    # TITLE EXTRACTION
    # -----------------------------------

    if soup.title:
        title = soup.title.text.strip()
    else:
        title = "No title found"

    print("\nPage Title:")
    print(title)

    # -----------------------------------
    # DESCRIPTION EXTRACTION
    # -----------------------------------

    description_meta = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if description_meta:
        description = description_meta.get("content").strip()
    else:
        description = "No description found"

    print("\nDescription:")
    print(description)

    # -----------------------------------
    # ARTICLE CONTENT EXTRACTION
    # -----------------------------------

    if "infermedica" in url:

        article_section = soup.find("article")

    elif "medium.com" in url:

        article_section = soup.find("article")

    else:

        article_section = soup.find("section")


    if article_section:
        paragraphs = article_section.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    # -----------------------------------
    # CLEAN ARTICLE TEXT
    # -----------------------------------

    article_text = ""

    for p in paragraphs:

        text = p.get_text(strip=True)

        if text:
            article_text += text + "\n\n"

    print("\nCleaned Article Preview:\n")
    print(article_text[:1000])

    # -----------------------------------
    # LANGUAGE DETECTION
    # -----------------------------------

    if article_text.strip():
        language = detect(article_text)
    else:
        language = "unknown"

    print("\nDetected Language:")
    print(language)

    # -----------------------------------
    # CHUNKING
    # -----------------------------------

    content_chunks = []

    for p in paragraphs:

        text = p.get_text(strip=True)

        if text:
            content_chunks.append(text)

    print("\nTotal Chunks:")
    print(len(content_chunks))

    # -----------------------------------
    # TOPIC TAGGING
    # -----------------------------------

    topic_keywords = {
        "AI": ["ai", "artificial intelligence"],
        "Healthcare": ["healthcare", "hospital", "patient"],
        "Machine Learning": ["model", "predictive", "machine learning"],
        "Data Science": ["data", "analytics"],
        "Research": ["research", "study", "paper"]
    }

    detected_tags = []

    lower_text = article_text.lower()

    for topic, keywords in topic_keywords.items():

        for keyword in keywords:

            if keyword in lower_text:
                detected_tags.append(topic)
                break

    detected_tags = list(set(detected_tags))

    print("\nDetected Topic Tags:")
    print(detected_tags)

    # -----------------------------------
    # TRUST SCORE CALCULATION
    # -----------------------------------

    author_name = title

    author_score = get_author_score(author_name)

    domain_score = get_domain_score(url)

    publication_year = 2022

    recency_score = get_recency_score(publication_year)

    citation_count = (
        article_text.lower().count("paper") +
        article_text.lower().count("study") +
        article_text.lower().count("research")
    )

    citation_score = get_citation_score(citation_count)

    disclaimer_score = get_disclaimer_score(article_text)

    trust_score = calculate_trust_score(
        author_score,
        citation_score,
        domain_score,
        recency_score,
        disclaimer_score
    )

    print("\nFinal Trust Score:")
    print(trust_score)

    # -----------------------------------
    # FINAL STRUCTURED OBJECT
    # -----------------------------------

    blog_data = {
        "source_url": url,
        "source_type": "blog",
        "title": title,
        "description": description,
        "language": language,
        "topic_tags": detected_tags,
        "total_paragraphs": len(paragraphs),
        "trust_score": trust_score,
        "content_chunks": content_chunks
    }

    # ADD TO MASTER LIST

    all_blog_data.append(blog_data)

# -----------------------------------
# SAVE JSON FILE
# -----------------------------------

with open(
    "output/blogs.json",
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        all_blog_data,
        json_file,
        indent=4,
        ensure_ascii=False
    )

print("\nJSON file saved successfully!")