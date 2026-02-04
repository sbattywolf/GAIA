# Checklist to enable internet-capable skills for Alby 0.3

1. Set the required API tokens as environment variables or in your .env file:

```powershell
setx ALBY_INTERNET_TOKEN "__REPLACE_WITH_TOKEN__"
setx CI_TOKEN "__REPLACE_WITH_CI_TOKEN__"
```

2. Run smoke tests locally to verify skills:

```powershell
py -3 AGENT_TASKS/agent_runtime/alby_0_2/tests/baby_born_test.py
py -3 AGENT_TASKS/agent_runtime/alby_0_2/smoke_skills.py --mode mock
```

3. Required packages to be downloaded and made available to the agent:
- packageA==1.2.3
- packageB>=4.0
