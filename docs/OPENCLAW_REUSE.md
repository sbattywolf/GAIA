# Reusing external/openclaw as a Reference for Telegram Integration

This document explains recommended ways to reuse code from `external/openclaw` as a reference or source-of-truth when integrating Telegram functionality into GAIA.

Purpose
- Capture options for reusing `external/openclaw` (vendor, package, or reference).
- Provide minimal steps and risks so maintainers can choose the right strategy.

Options

1) Vendor a small subset (recommended for quick reuse)
- Copy only the TypeScript files you need (e.g., `src/telegram/*`, any lightweight utils) into `external/openclaw-vendor/` or `third_party/openclaw/`.
- Keep a small README describing original commit/tag and license.
- Pros: simple, predictable, no submodule or dependency management.
- Cons: you must manually apply upstream fixes.

2) Keep as tracked tree (what we currently have)
- We converted `external/openclaw` into tracked files in-tree. This makes referencing code straightforward.
- Pros: immediate access, no submodule pitfalls.
- Cons: large surface area; keep CI and linting boundaries clear.

3) Package or workspace dependency (longer-term)
- If you plan to reuse regularly, publish a scoped package or convert `external/openclaw` into a local package consumed via a monorepo/workspace (pnpm/yarn/lerna) or as an npm package.
- Pros: clean dependency surface, versioned upgrades.
- Cons: higher maintenance; requires build/packaging setup.

How to reuse pieces for Telegram integration

- Identify the minimal surface you need (e.g., `src/telegram/*`, `src/infra/*` helpers).
- If using TypeScript code from `external/openclaw` as reference only, copy the example logic and re-implement idiomatically in Python (or Node) inside `agents/` or `scripts/`.
- If you want to call Node-based components from Python, keep them isolated in `external/openclaw/` and provide a small adapter script that exposes required functionality over stdin/stdout or via a local HTTP endpoint.

Practical steps (quick path)

1. Pick approach: vendor or keep tracked tree.
2. Create `docs/OPENCLAW_REUSE.md` entry (this file) and add a short `external/openclaw/README.md` noting origin and commit hash.
3. For vendor copy: copy only needed files into `third_party/openclaw/`, add a COPYRIGHT/NOTICE, and note upstream source (URL + commit).
4. For calling Node code from Python: create `external/openclaw/adapter/` with a small Node entrypoint (e.g., `bin/adapter.js`) that accepts JSON requests and returns JSON responses.
   - Example invocation from Python: `subprocess.run(['node', 'external/openclaw/adapter/bin/adapter.js'], input=json_bytes)`

Testing and CI

- Keep tests for reused components separate from GAIA tests; add a light smoke test that runs any Node-based adapter during CI smoke step (optional, see `.github/workflows/ci.yml`).
- If you vendor code, run upstream unit-tests locally before copying to ensure compatibility.

Licensing and attribution

- Verify the upstream license for `openclaw` and add proper attribution and license files in `external/openclaw/` or the vendored path.

Next actions

- Add a short `external/openclaw/README.md` with original repo URL and commit.
- If you prefer, I can scaffold a minimal `adapter/bin/adapter.js` plus a Python wrapper in `agents/` to demonstrate calling the Node code — tell me if you want that.

----
Generated: Feb 4, 2026
