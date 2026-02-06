#!/usr/bin/env python3
from gaia.secrets import SecretsManager
import json

sm = SecretsManager()
print(json.dumps([p.name for p in sm.providers]))
