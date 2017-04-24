from OrcLib import init_log
from OrcMem.MemDb import MemServer

if __name__ == '__main__':
    init_log()
    server = MemServer('localhost', 6002)
    server.start()