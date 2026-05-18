import ollama
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi

client = ollama.Client()

def fetch_driver_names():
    url = "http://iraceresults.co.uk/NXTGT3S9/drivers"
    response = requests.get(url)
    drivers = json.loads(response.text)

    name_map = {}
    driver_list = []
    for driver in drivers:
        # Use custom_display_name if available, otherwise use display_name
        correct_name = driver.get('custom_display_name', driver.get('display_name', ''))
        display_name = driver.get('display_name', '')
        driver_list.append(correct_name)

        # Map common variations to correct name
        if display_name != correct_name:
            name_map[display_name.lower()] = correct_name
            name_map[display_name.split()[0].lower()] = correct_name.split()[0]

    return name_map, driver_list

def normalize_names(transcript: str, name_map: dict) -> str:
    result = transcript
    for misspelling, correct in name_map.items():
        # Case-insensitive replacement
        import re
        result = re.sub(r'\b' + re.escape(misspelling) + r'\b', correct, result, flags=re.IGNORECASE)
    return result

def analyse_race(transcript: str) -> str:
    response = client.chat(
        model="qwen3:14b",
        messages=[
            {"role": "system", "content": "You are a motorsport analyst."},
            {"role": "user", "content": f"Summarise this race: {transcript}.  Include a short description of notable events such as battles between drivers, full course yellows etc."}
        ]
    )
    return response.message.content

# Fetch driver names and create mapping
name_map, drivers = fetch_driver_names()

# Extract video ID from URL
video_id = "N6xQWEwmzHk"
transcript_data = YouTubeTranscriptApi().fetch(video_id)
transcript_text = " ".join([item.text for item in transcript_data])

# Normalize driver names in transcript
normalized_transcript = normalize_names(transcript_text, name_map)

print(analyse_race(normalized_transcript))