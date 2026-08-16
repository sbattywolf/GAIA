# Lessons Learned

> Recovery status: Reconstructed  
> Source basis: surviving Sprint references, NEXT_STEPS, GAIA_MODEL, and conversation history  
> Confidence: Medium  
> Preservation rule: This file retains its original role. Reconstructed passages are not presented as verbatim recovery.

- Working software should reduce uncertainty, not silently become architecture.
- Deterministic paths are valuable for speed, reliability and explainability.
- One state snapshot per aggregate request prevents inconsistent reports.
- Runtime domains and human semantic categories are different; `light` is not always “lighting”.
- Home Assistant should remain authoritative for home state while GAIA adds interpretation and bounded capability.
- A second Telegram polling process creates conflicts; process ownership must be explicit.
- Test-environment compatibility hacks must not leak into production architecture.
- Generated documentation needs source Mermaid plus rendered figures and checksums.
- Git safety and narrow milestones matter for a solo maintainer.
- Local-first is demonstrated by degraded operation and recovery, not by model location alone.
