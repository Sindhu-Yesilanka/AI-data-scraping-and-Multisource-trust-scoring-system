from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import json

from scoring.trust_score import (
    get_domain_score,
    get_citation_score,
    get_disclaimer_score,
    calculate_trust_score
)

# -----------------------------------
# VIDEO IDS
# -----------------------------------

video_ids = [
    "j6EB9HO6acE"
]

all_videos = []

# -----------------------------------
# PROCESS VIDEOS
# -----------------------------------

for video_id in video_ids:

    print("\n==============================")
    print("Processing Video:")
    print(video_id)
    print("==============================")

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        full_text = ""

        for entry in transcript:

            full_text += entry.text + " "

        print("\nTranscript Preview:\n")
        print(full_text[:1000])

        # -----------------------------------
        # LANGUAGE DETECTION
        # -----------------------------------

        language = detect(full_text)

        print("\nDetected Language:")
        print(language)

        # -----------------------------------
        # TOPIC TAGGING
        # -----------------------------------

        topic_keywords = {
            "AI": ["ai", "artificial intelligence"],
            "Healthcare": ["healthcare", "medical", "patient"],
            "Machine Learning": ["machine learning", "deep learning"],
            "Python": ["python"],
            "Neural Networks": ["neural network"]
        }

        detected_tags = []

        lower_text = full_text.lower()

        for topic, keywords in topic_keywords.items():

            for keyword in keywords:

                if keyword in lower_text:
                    detected_tags.append(topic)
                    break

        detected_tags = list(set(detected_tags))

        print("\nDetected Tags:")
        print(detected_tags)

        # -----------------------------------
        # CHUNKING
        # -----------------------------------

        chunk_size = 500

        content_chunks = [
            full_text[i:i + chunk_size]
            for i in range(0, len(full_text), chunk_size)
        ]

        print("\nTotal Chunks:")
        print(len(content_chunks))

        # -----------------------------------
        # TRUST SCORING
        # -----------------------------------

        domain_score = get_domain_score("youtube.com")

        citation_count = (
            full_text.lower().count("research") +
            full_text.lower().count("study")
        )

        citation_score = get_citation_score(citation_count)

        disclaimer_score = get_disclaimer_score(full_text)

        trust_score = calculate_trust_score(
            author_score=0.70,
            citation_score=citation_score,
            domain_score=domain_score,
            recency_score=0.80,
            disclaimer_score=disclaimer_score
        )

        print("\nTrust Score:")
        print(trust_score)

        # -----------------------------------
        # VIDEO TITLE
        # -----------------------------------

        video_title = "Artificial Intelligence In Healthcare"

        # -----------------------------------
        # FINAL STRUCTURED OBJECT
        # -----------------------------------

        video_data = {
            "source_type": "youtube",
            "video_id": video_id,
            "title": video_title,
            "language": language,
            "topic_tags": detected_tags,
            "trust_score": trust_score,
            "transcript_length": len(full_text),
            "content_chunks": content_chunks
        }

        all_videos.append(video_data)

    except Exception as e:

        print("Error:", e)

# -----------------------------------
# SAVE JSON
# -----------------------------------

with open(
    "output/youtube.json",
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        all_videos,
        json_file,
        indent=4,
        ensure_ascii=False
    )

print("\nYouTube JSON saved successfully!")

