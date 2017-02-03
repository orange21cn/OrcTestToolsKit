import subprocess
from subprocess import CalledProcessError
import socket
from OrcLib.LibLog import OrcLog
from OrcLib import init_log

init_log()

abc = OrcLog("api.driver")

abc.info("abcdef")

def ccc(p_logger=None):
    aaaa = 3 if p_logger is None else p_logger
    print aaaa
    aaaa.info("AAAAA")


ccc(abc)