from shutil import which
import os
import re

PYTHON_VERSIONS = [3.6, 3.7, 3.8]
DATABASES = ['postgres', 'mysql', 'sqlite']


# inspects if a program is installed in linux
def is_installed(program_name):
    return which(program_name) is not None


def has_valid_django_name(name):
    return re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]*', name.lower())


def has_valid_project_path(path):
    return os.path.exists(path)


def has_valid_python_version(version):
    try:
        v = float(version)
        if v in PYTHON_VERSIONS:
            return True
        return False
    except ValueError:
        return False


def has_valid_database(db):
    return db in DATABASES
