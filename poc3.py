import ollama
from youtube_transcript_api import YouTubeTranscriptApi

client = ollama.Client()

def analyse_race(transcript: str) -> str:
    response = client.chat(
        model="qwen3:14b",
        messages=[
            {"role": "system", "content": "You are a motorsport analyst."},
            {"role": "user", "content": f"Summarise this race: {transcript}"}
        ]
    )
    return response.message.content

# Extract video ID from URL
video_id = "N6xQWEwmzHk"
transcript_data = YouTubeTranscriptApi().fetch(video_id)
transcript_text = " ".join([item.text for item in transcript_data])

print(analyse_race(transcript_text))