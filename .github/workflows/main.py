import os
import requests
import json
import time

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SORA_API_KEY = os.getenv("SORA_API_KEY")
SORA_MODEL = os.getenv("SORA_MODEL")

SHORTS_DURATION = int(os.getenv("SHORTS_DURATION", "11"))
VIDEO_RATIO = os.getenv("VIDEO_RATIO", "9:16")
POST_HASHTAGS = os.getenv("POST_HASHTAGS", "#shorts")

def generate_story():
    prompt = """
Write a powerful micro-story for a YouTube Short.

Rules:
- Maximum 35 words
- Must fit within 11 seconds
- Emotional, realistic, human
- No names
- No hashtags
- No emojis
- Simple language
- Strong hook in first sentence
- Twist or realization at the end

Topic: life, regret, success, relationships, time, or ambition

Return ONLY the story text.
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9
        }
    )

    return response.json()["choices"][0]["message"]["content"].strip()


def generate_sora_video(story_text):
    payload = {
        "model": SORA_MODEL,
        "input": story_text,
        "duration": SHORTS_DURATION,
        "aspect_ratio": VIDEO_RATIO
    }

    response = requests.post(
        "https://api.sora.ai/v1/video/generate",
        headers={
            "Authorization": f"Bearer {SORA_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    result = response.json()
    return result["video_url"]


def main():
    print("Generating story...")
    story = generate_story()
    print("Story:", story)

    print("Generating Sora video...")
    video_url = generate_sora_video(story)

    print("Video ready:", video_url)
    print("NEXT STEP: upload phase")


if __name__ == "__main__":
    main()
