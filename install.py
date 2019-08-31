import os
import getpass


INSTALL_FOLDER = '/home/' + getpass.getuser() + '/.no-headache'
BASHRC = '/home/' + getpass.getuser() + '/.bashrc'

try:

    os.system("mkdir -p " + INSTALL_FOLDER)
    os.system("cp -r . " + INSTALL_FOLDER)
    os.system("""echo "alias no-headache='python3 """ + INSTALL_FOLDER + """/main.py'" >> """ + BASHRC)
    print("Successfully installed no-headache-django")

except:

    os.system('rm -r ' + INSTALL_FOLDER)
    print("Failed Installing no-headache-django")
