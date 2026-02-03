import time
from agents.controller_agent import ControllerAgent
from scripts import sequence_manager as sm

ctrl = ControllerAgent(simulate=True)
max_iters = 500
iters = 0
while iters < max_iters:
    iters += 1
    active = ctrl.scan_active()
    if not active:
        print('No active sequence; done.')
        break
    seq_id = active.get('active_sequence')
    todos = sm._load_todos()
    open_todos = [k for k,v in (todos or {}).items() if v.get('seq_id')==seq_id and v.get('status')!='done']
    if not open_todos:
        print('No open todos; finishing check...')
        sm._maybe_finish_sequence(seq_id)
        time.sleep(0.1)
        continue
    # run one assignment to process a todo
    progressed = ctrl.assign_and_run_one()
    print('Progressed:', progressed, '; remaining open:', len(open_todos)-1)
    time.sleep(0.05)
else:
    print('Max iterations reached; aborting.')
