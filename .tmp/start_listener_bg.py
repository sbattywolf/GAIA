import subprocess, sys, os
py = sys.executable
script = os.path.join(os.getcwd(), 'scripts', 'approval_listener.py')
out = os.path.join(os.getcwd(), '.tmp', 'logs', 'approval_listener.out.log')
err = os.path.join(os.getcwd(), '.tmp', 'logs', 'approval_listener.err.log')
os.makedirs(os.path.dirname(out), exist_ok=True)
# Use Windows-specific DETACHED flags if available
creationflags = 0
if os.name == 'nt':
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
cmd = [py, script, '--timeout', '86400', '--poll', '300']
# Start detached
subprocess.Popen(cmd, stdout=open(out, 'a'), stderr=open(err, 'a'), creationflags=creationflags)
print('started background listener')
