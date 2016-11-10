import subprocess
from OrcLib import get_config

configer = get_config()
home = configer.get_option("DEFAULT", "root")

case = subprocess.Popen(["python", "%s/OrcApi/start_api.py" % home])
run = subprocess.Popen(["python", "%s/OrcApi/start_run.py" % home])
driver = subprocess.Popen(["python", "%s/OrcDriver/start_driver.py" % home])
driver_web = subprocess.Popen(["python", "%s/OrcDriver/start_socket.py" % home])
