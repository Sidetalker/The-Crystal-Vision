# Local Machine Snapshot — 2026-07-17

This folder preserves the files uploaded from the CrystalArchitect's local Windows
machine on 2026-07-17, before that machine was returned. It is a **snapshot for
safekeeping**, kept separate from the repository's main structure so nothing in the
existing site or `clementine/` package is overwritten. Merging the two lines of
development is future work.

## What is here

| Folder / file | Contents |
|---|---|
| `README.md`, `CLEMENTINE.md`, `GOVERNANCE.md`, `MILESTONES.md`, `BRIDGE.md` | Updated docs from the local **CrystalCore v0.13.x** line (SpaceXAI opt-in provider, voice) |
| `clementine.py` | Terminal companion, v0.13.x — adds `/provider`, `/optin`, `/optout`, `/expose`, multi-line paste handling |
| `clementine_web.py` | Single-file local web UI, v0.13.x — on-device voice (speech synthesis + mic), provider picker, transparency endpoints (`/api/expose`, `/api/conversation`, `/api/prompt`) |
| `crystalcore/` | Partial package snapshot (older generation): `__init__.py`, `__main__.py`, `companion.py`, `memory.py`, `expose.py` |
| `site/` | Updated static site for teraustralis.com.au (index, crystalcore, codex, apocryphon, clementine pages + CSS + CNAME) |
| `seven-sisters/` | The Seven Sisters Songline documents and CrystalCore protocol pack (manuals, path logs, water brief, transmit pack, landing page) |
| `.env.example` | Template for the SpaceXAI opt-in key (`XAI_API_KEY`). **Never commit a real `.env`.** |
| `Start*.bat` | Windows launchers (local Ollama, web UI, SpaceXAI mode) |
| `_clean_memory.py` | One-shot local memory cleanup utility |

## Known-incomplete: missing source files

The v0.13.x code in this snapshot **does not run as-is**. `crystalcore/__init__.py` and
`clementine.py` import modules that were never uploaded before the machine went back:

- `crystalcore/node.py`
- `crystalcore/ollama.py`
- `crystalcore/version.py`
- `crystalcore/status.py`
- the SpaceXAI provider module (and `load_dotenv` / `xai_api_key_present` helpers)
- `tests/` (including `tests/test_provider.py`)
- `cli/crystalcore.ps1` (referenced by the protocol pack)

Only compiled `.pyc` bytecode for some of these was uploaded; bytecode is not committed.
If the local machine (or a backup) is ever available again, recovering those files is
the first priority.

## Relationship to the rest of the repository

The repository's `clementine/` package is a **diverged sibling** of this snapshot:
it has the self-naming feature (v12) and the Svelte web interface (`server.py` +
`webapp/`), which this local line does not; this local line has SpaceXAI opt-in,
voice, and the expose/transparency layer, which the repository does not. Neither
supersedes the other yet.

Deliberately **excluded** from this snapshot: real credentials (`.env` with a live
key, Grok CLI `auth.json`), private Grok CLI session data (chat history, event logs,
telemetry), Python bytecode, and machine-local editor/permission settings.
