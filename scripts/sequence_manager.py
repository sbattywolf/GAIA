"""Sequence manager for step-by-step action lists sent over Telegram.

Usage:
- `create_sequence(chat_id, steps, title)` saves a sequence and sends the first step.
- Steps are list of dicts: {'title': str, 'detail': str, 'extra': optional str}

Callback buttons are sent for each step: Do / More / Skip. Callbacks use:
- `seq:do:<seq_id>:<index>`
- `seq:more:<seq_id>:<index>`
- `seq:skip:<seq_id>:<index>`

The approval listener delegates these callbacks to `handle_callback` below.
"""
from pathlib import Path
import json
import uuid
import os
from scripts import telegram_client as tc
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
SEQ_FILE = ROOT / '.tmp' / 'sequences.json'
PROPOSAL_FILE = ROOT / 'doc' / 'SEQUENCE_PROPOSALS.md'
ACTIVE_FILE = ROOT / '.tmp' / 'active_task.json'
SEQ_TODO_FILE = ROOT / '.tmp' / 'sequence_todos.json'
ARCHIVE_FILE = ROOT / 'doc' / 'SEQUENCE_ARCHIVE.md'


def _load():
    try:
        return json.loads(SEQ_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _save(obj):
    SEQ_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEQ_FILE.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def create_sequence(token, chat_id, steps, title=None):
    data = _load()
    seq_id = str(uuid.uuid4())
    # allow optimization: group related steps into sub-steps
    optimized = _optimize_steps(steps)
    seq = {
        'id': seq_id,
        'chat_id': str(chat_id),
        'title': title or 'Sequence',
        'steps': [dict(s, status='pending') for s in optimized],
        'created': None,
        'last_message_id': None
    }
    data[seq_id] = seq
    _save(data)
    # evaluate size: if sequence is large, create a proposal and active task
    # count actionable items: each simple step counts 1, composite counts len(sub_steps)
    count_actions = 0
    for s in seq['steps']:
        if s.get('sub_steps'):
            count_actions += len(s.get('sub_steps'))
        else:
            count_actions += 1

    THRESHOLD = int(os.environ.get('SEQUENCE_PROPOSAL_THRESHOLD', '6'))
    if count_actions > THRESHOLD:
        # too large to run interactively — create a proposal and push to todo
        _propose_sequence(seq_id, seq)
        _set_active_task(seq_id)
        return seq_id

    # send first step
    send_step(token, seq_id, 0)
    return seq_id


def _propose_sequence(seq_id, seq):
    """Append a human-readable proposal to `doc/SEQUENCE_PROPOSALS.md`.

    This is used when a sequence is judged too large for an interactive run.
    The proposal file is a living draft that can be merged into the official
    documentation once the associated todo tasks are completed.
    """
    PROPOSAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    header = f"## Proposal: {seq.get('title')} — {seq_id}\n" + f"Created: {datetime.utcnow().isoformat()}Z\n\n"
    md_lines = [header]
    md_lines.append('Steps:')
    for i, s in enumerate(seq.get('steps') or []):
        if s.get('sub_steps'):
            md_lines.append(f"- {i+1}. {s.get('title')} (composite, {len(s.get('sub_steps'))} sub-steps)")
            for j, ss in enumerate(s.get('sub_steps')):
                md_lines.append(f"  - {i+1}.{j+1} {ss.get('title')}: {ss.get('detail','')}")
        else:
            md_lines.append(f"- {i+1}. {s.get('title')}: {s.get('detail','')}")
    md_lines.append('\n---\n')
    with open(PROPOSAL_FILE, 'a', encoding='utf-8') as f:
        f.write('\n'.join(md_lines) + '\n')
    # create granular todo items for the sequence so agents can pick them up
    _create_todo_items_for_sequence(seq_id, seq)


def _set_active_task(seq_id):
    ACTIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    obj = {'active_sequence': seq_id, 'assigned': None, 'created': datetime.utcnow().isoformat() + 'Z'}
    ACTIVE_FILE.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def _create_todo_items_for_sequence(seq_id, seq):
    """Create granular todo entries for each actionable (sub)step.

    Stores them in `.tmp/sequence_todos.json` with statuses.
    """
    SEQ_TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    todos = _load_todos()
    # create entries: each simple step -> one todo; each sub_step -> one todo
    created = []
    for si, s in enumerate(seq.get('steps') or []):
        if s.get('sub_steps'):
            for sj, ss in enumerate(s.get('sub_steps')):
                tid = f"{seq_id}:{si}:{sj}"
                entry = {
                    'id': tid,
                    'seq_id': seq_id,
                    'step_index': si,
                    'sub_index': sj,
                    'title': ss.get('title'),
                    'detail': ss.get('detail'),
                    'status': 'open'
                }
                todos[tid] = entry
                created.append(tid)
        else:
            tid = f"{seq_id}:{si}"
            entry = {
                'id': tid,
                'seq_id': seq_id,
                'step_index': si,
                'sub_index': None,
                'title': s.get('title'),
                'detail': s.get('detail'),
                'status': 'open'
            }
            todos[tid] = entry
            created.append(tid)
    _save_todos(todos)
    return created


def _load_todos():
    try:
        return json.loads(SEQ_TODO_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _save_todos(obj):
    SEQ_TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEQ_TODO_FILE.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def _mark_todo_done(seq_id, step_index, sub_index=None):
    todos = _load_todos()
    if sub_index is None:
        tid = f"{seq_id}:{step_index}"
    else:
        tid = f"{seq_id}:{step_index}:{sub_index}"
    t = todos.get(tid)
    if not t:
        return False
    t['status'] = 'done'
    t['done_at'] = datetime.utcnow().isoformat() + 'Z'
    _save_todos(todos)
    # append progress to proposal doc
    _append_progress_to_proposal(seq_id, t)
    return True


def _append_progress_to_proposal(seq_id, todo_entry):
    # write an entry into PROPOSAL_FILE noting the completed todo
    note = f"- [{todo_entry.get('id')}] DONE {todo_entry.get('title')} @ {datetime.utcnow().isoformat()}Z\n"
    with open(PROPOSAL_FILE, 'a', encoding='utf-8') as f:
        f.write(note)


def _maybe_finish_sequence(seq_id):
    todos = _load_todos()
    # find any open todos for this seq
    for k, v in todos.items():
        if v.get('seq_id') == seq_id and v.get('status') != 'done':
            return False
    # all done -> merge proposal into archive and clear active task
    _merge_proposal_into_archive(seq_id)
    # clear active
    try:
        if ACTIVE_FILE.exists():
            af = json.loads(ACTIVE_FILE.read_text(encoding='utf-8'))
            if af.get('active_sequence') == seq_id:
                ACTIVE_FILE.unlink()
    except Exception:
        pass
    return True


def _merge_proposal_into_archive(seq_id):
    # find proposal section for seq_id in PROPOSAL_FILE and append to ARCHIVE_FILE
    try:
        text = PROPOSAL_FILE.read_text(encoding='utf-8')
    except Exception:
        text = ''
    # naive: append entire proposals file to archive with a header
    ARCHIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    header = f"\n## Merged Proposal {seq_id} — {datetime.utcnow().isoformat()}Z\n"
    with open(ARCHIVE_FILE, 'a', encoding='utf-8') as af:
        af.write(header)
        af.write(text)
    # remove proposal file
    try:
        PROPOSAL_FILE.unlink()
    except Exception:
        pass


def _optimize_steps(steps):
    """Group contiguous action-like steps into composite steps with `sub_steps`.

    Heuristic: consecutive steps whose `title` or `detail` contain keywords
    like 'inspect', 'investig', 'fix', 'test', 'restart' are grouped when
    the run length >= 2.
    """
    if not steps:
        return []
    keywords = ('inspect', 'investig', 'investigate', 'check', 'diagnos', 'debug', 'fix', 'restart', 'patch', 'test', 'verify')
    out = []
    buf = []

    def flush_buf():
        if not buf:
            return
        if len(buf) >= 2:
            # create composite step
            titles = [b.get('title') or '' for b in buf]
            composite = {
                'title': f"Batch: {titles[0]} (+{len(buf)-1} more)",
                'detail': '\n'.join([f"{i+1}. {b.get('title')}" for i, b in enumerate(buf)]),
                'sub_steps': buf.copy()
            }
            out.append(composite)
        else:
            out.extend(buf)
        buf.clear()

    for s in steps:
        txt = (s.get('title') or '') + ' ' + (s.get('detail') or '')
        txtl = txt.lower()
        if any(k in txtl for k in keywords):
            buf.append(s)
            continue
        else:
            # non-matching step: flush buffer then append this
            flush_buf()
            out.append(s)
    flush_buf()
    return out


def send_step(token, seq_id, index):
    data = _load()
    seq = data.get(seq_id)
    if not seq:
        return None
    steps = seq.get('steps') or []
    if index < 0 or index >= len(steps):
        return None
    step = steps[index]
    title = seq.get('title') or 'Sequence'
    text_lines = [f"{title} — Step {index+1}/{len(steps)}:", step.get('title', '')]
    detail = step.get('detail') or ''
    # keep concise initially
    preview = detail if len(detail) < 400 else detail[:397] + '...'
    if preview:
        text_lines.append('')
        text_lines.append(preview)

    text = '\n'.join(text_lines)

    # buttons: Do / More / Skip
    buttons = [
        [ {'text': 'Do', 'callback_data': f'seq:do:{seq_id}:{index}'}, {'text': 'More', 'callback_data': f'seq:more:{seq_id}:{index}'} ],
        [ {'text': 'Skip', 'callback_data': f'seq:skip:{seq_id}:{index}'} ]
    ]
    reply_markup = {'inline_keyboard': buttons}
    try:
        res = tc.send_message(token, seq.get('chat_id'), text, reply_markup=reply_markup)
        mid = (res.get('result') or {}).get('message_id')
        seq['last_message_id'] = mid
        _save(data)
        return res
    except Exception:
        return None


def handle_callback(token, callback, data_str, actor_id=None):
    """Handle seq:* callback strings coming from Telegram callback_query.

    data_str is the raw callback data, e.g. 'seq:do:<seq_id>:<index>'.
    """
    parts = data_str.split(':')
    # expect ['seq', verb, seq_id, index]
    if len(parts) < 4:
        return
    _, verb, seq_id, idx = parts[0], parts[1], parts[2], parts[3]
    try:
        index = int(idx)
    except Exception:
        index = 0

    data = _load()
    seq = data.get(seq_id)
    if not seq:
        return
    steps = seq.get('steps') or []
    if index < 0 or index >= len(steps):
        return
    step = steps[index]

    # convenience send helper
    def _send_to_actor(txt):
        try:
            tc.send_message(token, actor_id, txt)
        except Exception:
            pass

    if verb == 'do':
        # if composite step with sub_steps, start subflow
        if step.get('sub_steps'):
            # start sub-step 0
            send_sub_step(token, seq_id, index, 0, actor_id=actor_id)
            return
        step['status'] = 'done'
        _save(data)
        _send_to_actor(f"Marked step {index+1} as done: {step.get('title')}")
        # send next step if exists
        if index+1 < len(steps):
            send_step(token, seq_id, index+1)
        else:
            _send_to_actor(f"Sequence {seq.get('title')} complete.")
    elif verb == 'more':
        extra = step.get('extra') or step.get('detail') or '(no extra details)'
        # send concise extra and offer to Do or Skip
        txt = f"Details for step {index+1}:\n{extra}"
        _send_to_actor(txt)
        # re-send the step message so inline buttons are available again
        send_step(token, seq_id, index)
    elif verb == 'skip':
        step['status'] = 'skipped'
        _save(data)
        _send_to_actor(f"Skipped step {index+1}: {step.get('title')}")
        if index+1 < len(steps):
            send_step(token, seq_id, index+1)
        else:
            _send_to_actor(f"Sequence {seq.get('title')} complete (some steps skipped).")
    elif verb == 'subdo' or verb == 'subskip' or verb == 'submore':
        # format: seq:subdo:seq_id:step_index:sub_index
        # we accept both 5-part and 4-part (tolerant)
        parts2 = data_str.split(':')
        # expect ['seq','subdo', seq_id, step_index, sub_index]
        if len(parts2) < 5:
            return
        _, sv, sseq_id, sidx, subidx = parts2[:5]
        try:
            s_index = int(sidx)
            sub_index = int(subidx)
        except Exception:
            return
        seq = data.get(sseq_id)
        if not seq:
            return
        ssteps = seq.get('steps') or []
        if s_index < 0 or s_index >= len(ssteps):
            return
        comp = ssteps[s_index]
        sub_steps = comp.get('sub_steps') or []
        if sub_index < 0 or sub_index >= len(sub_steps):
            return
        if sv == 'subdo':
            # mark substep done
            sub_steps[sub_index]['status'] = 'done'
            _save(data)
            _send_to_actor(f"Marked sub-step {sub_index+1} done: {sub_steps[sub_index].get('title')}")
            # advance
            if sub_index+1 < len(sub_steps):
                send_sub_step(token, sseq_id, s_index, sub_index+1, actor_id=actor_id)
            else:
                # mark composite step done and continue main sequence
                comp['status'] = 'done'
                _save(data)
                _send_to_actor(f"Composite step complete: {comp.get('title')}")
                if s_index+1 < len(ssteps):
                    send_step(token, sseq_id, s_index+1)
                else:
                    _send_to_actor(f"Sequence {seq.get('title')} complete.")
        elif sv == 'subskip':
            sub_steps[sub_index]['status'] = 'skipped'
            _save(data)
            _send_to_actor(f"Skipped sub-step {sub_index+1}: {sub_steps[sub_index].get('title')}")
            if sub_index+1 < len(sub_steps):
                send_sub_step(token, sseq_id, s_index, sub_index+1, actor_id=actor_id)
            else:
                comp['status'] = 'done'
                _save(data)
                _send_to_actor(f"Composite step complete (some sub-steps skipped): {comp.get('title')}")
                if s_index+1 < len(ssteps):
                    send_step(token, sseq_id, s_index+1)
                else:
                    _send_to_actor(f"Sequence {seq.get('title')} complete.")
        elif sv == 'submore':
            extra = sub_steps[sub_index].get('extra') or sub_steps[sub_index].get('detail') or '(no extra)'
            _send_to_actor(f"Details for sub-step {sub_index+1}:\n{extra}")
            # re-send the sub-step message
            send_sub_step(token, sseq_id, s_index, sub_index, actor_id=actor_id)


def send_sub_step(token, seq_id, index, sub_index, actor_id=None):
    data = _load()
    seq = data.get(seq_id)
    if not seq:
        return None
    steps = seq.get('steps') or []
    if index < 0 or index >= len(steps):
        return None
    comp = steps[index]
    sub_steps = comp.get('sub_steps') or []
    if sub_index < 0 or sub_index >= len(sub_steps):
        return None
    s = sub_steps[sub_index]
    text_lines = [f"{seq.get('title')} — Step {index+1}.{sub_index+1}/{len(sub_steps)}:", s.get('title', '')]
    detail = s.get('detail') or ''
    preview = detail if len(detail) < 400 else detail[:397] + '...'
    if preview:
        text_lines.append('')
        text_lines.append(preview)
    text = '\n'.join(text_lines)
    buttons = [
        [ {'text': 'Done', 'callback_data': f'seq:subdo:{seq_id}:{index}:{sub_index}'}, {'text': 'More', 'callback_data': f'seq:submore:{seq_id}:{index}:{sub_index}'} ],
        [ {'text': 'Skip', 'callback_data': f'seq:subskip:{seq_id}:{index}:{sub_index}'} ]
    ]
    reply_markup = {'inline_keyboard': buttons}
    try:
        res = tc.send_message(token, seq.get('chat_id'), text, reply_markup=reply_markup)
        mid = (res.get('result') or {}).get('message_id')
        seq['last_message_id'] = mid
        _save(data)
        return res
    except Exception:
        return None
