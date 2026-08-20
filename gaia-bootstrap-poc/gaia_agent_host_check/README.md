# GAIA Agent Host Check Toolkit v0.3

Status: IMPLEMENTATION PACKAGE — HUMAN OWNER VALIDATION REQUIRED.

Reusable bounded read-only toolkit. Profiles: generic/1070/3090. Skill profiles:
home_collaborator/coding_agent/vision_agent/voice_agent. Runtime: auto/native/container.

Core tests are fixture-based and require no real 1070/3090:
`PYTHONPATH=. python -m unittest discover -s tests -q`

No host/model/Docker/Home Assistant/Git mutation or secret-value collection is
performed by default. Engineer workspace != Human Owner authoritative checkout.
