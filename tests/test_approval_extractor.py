import json
from scripts import approval_extractor as ae


def make_req(request_id=None, trace_id=None, task_id=None):
    return {'type': 'approval.request', 'request_id': request_id, 'trace_id': trace_id, 'task_id': task_id}


def make_recv(request_id=None, trace_id=None, task_id=None):
    return {'type': 'approval.received', 'request_id': request_id, 'trace_id': trace_id, 'task_id': task_id}


def test_match_by_request_id():
    req = make_req(request_id='r1')
    recv = make_recv(request_id='r1')
    res = ae.extract_approval_pairs([req, recv])
    assert len(res['matched']) == 1
    assert res['matched'][0][0]['request_id'] == 'r1'


def test_match_by_trace_id():
    req = make_req(trace_id='t1')
    recv = make_recv(trace_id='t1')
    res = ae.extract_approval_pairs([req, recv])
    assert len(res['matched']) == 1


def test_match_by_task_id():
    req = make_req(task_id='task-1')
    recv = make_recv(task_id='task-1')
    res = ae.extract_approval_pairs([req, recv])
    assert len(res['matched']) == 1


def test_missing_and_unmatched():
    req1 = make_req(request_id='r-missing')
    recv1 = make_recv(request_id='r-unmatched')
    res = ae.extract_approval_pairs([req1, recv1])
    assert len(res['matched']) == 0
    assert len(res['missing_requests']) == 1
    assert len(res['unmatched_received']) == 1
