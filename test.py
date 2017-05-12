import socket
import sys
import json
import time


from OrcLib.LibNet import OrcSocketResource
from OrcLib.LibNet import OrcResource


def orc_time(p_func, *args, **kwargs):
    begin = time.time()

    p_func(*args, **kwargs)

    end = time.time()
    print '--', begin
    print '---', end - begin

res = OrcSocketResource('MEM')
orc_time(res.get, dict(TABLE='RunTime', CMD='SEARCH', PARA=dict()))

abc = OrcResource("Data")
orc_time(abc.get, parameter=dict(id=10))

