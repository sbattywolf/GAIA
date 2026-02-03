import time

from agents.role_arbiter import RoleArbiter, RoleDescriptor


def test_role_arbiter_handler_runs():
    arb = RoleArbiter()
    arb.add_role(RoleDescriptor(name='worker', skills=['task']))

    def handler(task_ctx):
        # immediate completion
        return {'status': 'done', 'result': 'ok'}

    arb.register_handler('worker', handler)
    arb.start_executor(num_threads=1)
    arb.schedule_job('worker', {'job_id': 1})
    # wait briefly for worker to pick up
    time.sleep(0.05)
    arb.stop_executor()
    acts = arb.get_activations()
    assert any(a.get('status') in ('done', 'completed') for a in acts)
