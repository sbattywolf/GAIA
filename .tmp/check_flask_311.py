import importlib.util, sys
print('EXE:'+sys.executable)
print('HAS_FLASK:'+str(importlib.util.find_spec('flask') is not None))
