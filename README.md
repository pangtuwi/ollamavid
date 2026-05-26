# ollamavid

Analyses iRacing race broadcasts by fetching a YouTube transcript and sending it to an LLM (local Ollama or Claude) for a structured race summary.

## Features

- Fetches YouTube transcripts automatically
- Caches transcripts locally to avoid re-downloading
- Injects the driver roster into the AI prompt so it can correct phonetic transcription errors
- Supports local Ollama or the Claude API as the LLM backend
- Saves the analysis as a markdown file

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally (if using `llm_provider=ollama`)
- An Anthropic API key (if using `llm_provider=claude`)

## Installation

```bash
pip install ollama anthropic youtube-transcript-api requests
```

## Configuration

Edit `config.md`:

```
llm_provider=ollama        # ollama | claude
video_id=<YouTube video ID>
drivers_url=<iRaceResults drivers endpoint>
```

For Claude, set your API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Customising the prompt

Edit `prompt.md` to change the analysis style. Two placeholders are available:

- `{drivers}` — replaced with the driver roster at runtime (use in the `# System` section)
- `{transcript}` — replaced with the race transcript (use in the `# User` section)

## Usage

```bash
python3 poc4.py
```

Outputs:
- `transcript_{video_id}.txt` — the raw YouTube transcript
- `analysis_{video_id}.md` — the AI-generated race summary
