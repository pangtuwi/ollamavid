import ollama

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

print(analyse_race("The 2004 Monaco Grand Prix"));