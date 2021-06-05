import elevate
import getpass
import sys
import os
import sqlite3
import binascii
import hashlib
import subprocess

def is_root():
    return os.getuid() == 0

def GetVariables():
    homedir = os.path.expanduser("~")
    appdir = homedir + "/.LinuxTool"
    venvdir = appdir + "/.venv"
    username = getpass.getuser()

    root = is_root()

    variables = []
    working_dir = ""

    if not root:
        with open("/tmp/variables.txt", "w+") as f:
            f.write(appdir)
            f.write("\n")
            f.write(os.path.abspath("."))
    else:
        with open("/tmp/variables.txt","r") as appdir_file:
            appdir = appdir_file.readline()
            appdir = appdir.rstrip()
            working_dir = appdir_file.readline()
            #os.remove("/tmp/user.txt")
    variables.append(appdir)
    variables.append(working_dir)
    return variables

def CreateUser(appdir):
    from LinuxInstallerClass import LinuxInstaller
    from PyQt5.QtWidgets import QApplication

    root = is_root()

    if root:
        variables = GetVariables() 
        venvdir = variables[0] +"/.venv"

        with open("/etc/rsyslog.d/20-ufw.conf", "w") as f:
            f.write(':msg,contains,"[netfilter] " -/var/log/iptables.log')
            f.write("& stop")
            f.close()
            os.system("systemctl restart rsyslog")

        os.environ["DISPLAY"] = ":0"
        # under the virtualenv /path/to/virtualenv/
        python_bin = venvdir + "/bin/python3"
        # Path to the script that must run under the virtualenv
        script_file = variables[1] + "/elevate_helper.py"
        script_file = os.path.abspath(script_file)

        subprocess.Popen([python_bin, script_file])

if __name__ == "__main__":
    appdir = GetVariables()
    root = is_root()
    if not root:
        os.system("xhost +")
    elevate.elevate()
    CreateUser(appdir)
