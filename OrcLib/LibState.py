# coding=utf-8
class RunState:

    state_new = 'NEW'
    state_waiting = 'WAITING'
    state_not_run = 'NOT_RUN'
    state_pass = 'PASS'
    state_fail = 'FAIL'

    def __init__(self):
        pass


class RunStatus(object):

    new_ = 'new'
    waiting_ = 'waiting'
    running_ = 'running'
    pass_ = 'pass'
    fail_ = 'fail'

    def __init__(self):
        object.__init__(self)