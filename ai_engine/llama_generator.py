# llama_generator.py

import requests
import json
import os
from datetime import datetime, timedelta
from domains import DOMAINS

CACHE_FILE = "cache.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def clean_topics(raw_topics, count):
    cleaned = []

    for line in raw_topics.split("\n"):
        line = line.strip()

        if not line:
            continue

        # Remove numbering (1. , 2. etc)
        if ". " in line:
            line = line.split(". ", 1)[1]

        # Remove bullets if any
        line = line.replace("-", "").strip()

        # Keep only short phrases (max 3 words)
        if len(line.split()) <= 3:
            cleaned.append(line)

    return cleaned[:count]


def call_llama(domain: str, count: int):
    prompt = f"""
You are a senior technology trend analyst.

Generate exactly {count} trending technical topics in the domain of {domain}.

IMPORTANT:
- Each topic must be ONE WORD or MAXIMUM THREE WORDS.
- No explanations.
- No sentences.
- No punctuation.
- Return only a numbered list.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "temperature": 0.8,
            "stream": False
        }
    )

    result = response.json()["response"]

    return clean_topics(result, count)


def generate_topics(domain: str, count: int = 10):

    if domain not in DOMAINS:
        return ["Invalid Domain"]

    cache = load_cache()

    if domain in cache:
        last_updated = datetime.strptime(
            cache[domain]["last_updated"], "%Y-%m-%d"
        )

        # If within 6 months return cached
        if datetime.now() - last_updated < timedelta(days=180):
            return cache[domain]["topics"]

    # Regenerate
    topics = call_llama(domain, count)

    cache[domain] = {
        "topics": topics,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    save_cache(cache)

    return topics