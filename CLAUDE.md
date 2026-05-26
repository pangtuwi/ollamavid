# ollamavid

A motorsport race analysis tool that uses a local Ollama LLM or the Claude API to summarise iRacing races from YouTube transcripts.

## Project overview

- Fetches YouTube video transcripts via `youtube_transcript_api`
- Fetches the driver roster from the iRaceResults API and injects it into the system prompt so the AI can resolve phonetic transcription errors
- Sends the transcript to either a local Ollama instance or the Claude API for race summary and analysis
- Outputs the analysis to a `.md` file and the raw transcript to a `.txt` file
- Caches transcripts on disk to avoid re-downloading

## Files

- `poc1.py` — Basic proof of concept: hardcoded transcript, straight LLM call
- `poc2.py` — Full pipeline with regex-based driver name normalisation (superseded by poc4)
- `poc3.py` — Intermediate: fetch YouTube transcript, analyse (no name normalisation)
- `poc4.py` — Current main script (see below)
- `config.md` — Runtime configuration (video ID, LLM provider, drivers API URL)
- `prompt.md` — System and user prompts with `{drivers}` and `{transcript}` placeholders
- `drivers_page.html` — Saved JSON snapshot of the drivers API response (despite the `.html` extension)

## poc4.py pipeline

1. Load `config.md` and `prompt.md`
2. Fetch driver names from the iRaceResults API; inject as a bullet list into the system prompt via `{drivers}`
3. Check for a cached `transcript_{video_id}.txt`; download from YouTube if not present
4. Call the configured LLM provider with the system + user prompts
5. Save analysis to `analysis_{video_id}.md`

## Configuration — config.md

```
llm_provider=ollama        # ollama | claude
video_id=<YouTube video ID>
drivers_url=<iRaceResults drivers endpoint>
```

## Prompts — prompt.md

Uses two markdown sections:

```
# System
... system instructions ...
{drivers}   ← replaced with bullet list of driver names at runtime

# User
... {transcript} ...   ← replaced with the race transcript at runtime
```

## Tech stack

- Python 3
- `ollama` — local LLM client (model: `qwen3:14b`)
- `anthropic` — Claude API client (model: `claude-opus-4-6`)
- `youtube_transcript_api` — YouTube transcript fetching
- `requests` — HTTP calls to iRaceResults API

## Development notes

- When using `llm_provider=claude`, set `ANTHROPIC_API_KEY` as an environment variable
- Ollama must be running locally when using `llm_provider=ollama`
- The drivers URL in `config.md` is season-specific; update it each season
- Generated `transcript_*.txt` and `analysis_*.md` files are gitignored
