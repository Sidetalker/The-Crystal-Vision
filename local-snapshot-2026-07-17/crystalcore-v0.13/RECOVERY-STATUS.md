# crystalcore v0.13 — recovery in progress

This folder holds the **v0.13.x generation** of the CrystalCore package (the
SpaceXAI opt-in line), uploaded directly from the local machine on 2026-07-17.
It is being assembled here so nothing is lost before the laptop is reset.

## Present (uploaded, verbatim)

- `__init__.py` — v0.13 exports (adds SpaceXAI + envutil surface)
- `__main__.py` — `python -m crystalcore` → status board / expose
- `companion.py` — the full brain: local Ollama default + SpaceXAI opt-in with
  explicit consent (`cloud_opt_in`, timestamps, per-provider honest prompts)
- `envutil.py` — `.env` loader + `xai_api_key_present()`
- `expose.py` — v0.13 transparency dump (knows about spacexai + status modules)

## Carried forward (generation-compatible)

- `node.py`, `ollama.py`, `profiles.py` — copied from the recovered package one
  folder up. `__init__.py`/`companion.py` import the same names from these, so
  they fit v0.13 unchanged.

## STILL NEEDED before this package will import

Three files are imported by the code above but have not been uploaded yet:

- **`spacexai.py`** — the SpaceXAI (xAI API) client. Imported by `__init__.py`,
  `companion.py`, `expose.py` for: `SpaceXAIClient`, `BASE_URL`, `DEFAULT_MODEL`,
  `looks_like_spacexai_model`, `user_facing_spacexai_error`.
- **`status.py`** — the live status board. Imported by `__main__.py`
  (`from .status import main`).
- **`memory.py` (v0.13)** — `companion.py` sets `personality.provider`,
  `personality.cloud_opt_in`, and `personality.cloud_opt_in_at`, so the
  `Personality` dataclass in this generation has those fields. The older
  `memory.py` one folder up does **not**, so the v0.13 version is needed.

Until those three arrive (from the laptop or a backup), this folder preserves
everything received but does not yet run.
