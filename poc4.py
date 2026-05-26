import os
import json
import ollama
import anthropic
import requests
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_driver_names(url: str) -> str:
    response = requests.get(url)
    drivers = json.loads(response.text)
    names = [driver.get("custom_display_name", driver.get("display_name", "")) for driver in drivers]
    return "\n".join(f"- {name}" for name in names if name)


def load_prompt(path="prompt.md") -> tuple[str, str]:
    system, user = "", ""
    current = None
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if stripped == "# System":
                current = "system"
            elif stripped == "# User":
                current = "user"
            elif current == "system":
                system += line
            elif current == "user":
                user += line
    return system.strip(), user.strip()


def load_config(path="config.md"):
    config = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()
    return config


def analyse_race_ollama(transcript: str, system: str, user: str) -> str:
    client = ollama.Client()
    response = client.chat(
        model="qwen3:14b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user.replace("{transcript}", transcript)}
        ]
    )
    return response.message.content


def analyse_race_claude(transcript: str, system: str, user: str) -> str:
    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=system,
        messages=[
            {"role": "user", "content": user.replace("{transcript}", transcript)}
        ]
    ) as stream:
        message = stream.get_final_message()
    return next(block.text for block in message.content if block.type == "text")


def analyse_race(transcript: str, provider: str, system: str, user: str) -> str:
    if provider == "claude":
        return analyse_race_claude(transcript, system, user)
    elif provider == "ollama":
        return analyse_race_ollama(transcript, system, user)
    else:
        raise ValueError(f"Unknown llm_provider '{provider}'. Valid options: ollama, claude")


config = load_config()
video_id = config["video_id"]
provider = config["llm_provider"]
system_prompt, user_prompt = load_prompt()

drivers = fetch_driver_names(config["drivers_url"])
system_prompt = system_prompt.replace("{drivers}", drivers)

transcript_filename = f"transcript_{video_id}.txt"

if os.path.exists(transcript_filename):
    with open(transcript_filename) as f:
        transcript_text = f.read()
    print(f"Transcript loaded from {transcript_filename}")
else:
    transcript_data = YouTubeTranscriptApi().fetch(video_id)
    transcript_text = " ".join([item.text for item in transcript_data])
    with open(transcript_filename, "w") as f:
        f.write(transcript_text)
    print(f"Transcript saved to {transcript_filename}")

analysis = analyse_race(transcript_text, provider, system_prompt, user_prompt)

analysis_filename = f"analysis_{video_id}.md"
with open(analysis_filename, "w") as f:
    f.write(analysis)
print(f"Analysis saved to {analysis_filename}")

print(analysis)
