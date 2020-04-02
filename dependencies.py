import os


# this function checks if a certain requirements file contains gunicorn.
def inspect_gunicorn_dependency(requirements_path):
    try:
        with open(requirements_path, 'r+') as requirements_file:
            requirements = requirements_file.read()
            if 'gunicorn' not in requirements.lower():
                print('(++) Adding Gunicorn to project requirements.')
                requirements_file.write('\ngunicorn==20.0.4')
        return 0
    except Exception as e:
        print(e)
        return 1


def inspect_postgres_dependency(requirements_path):
    try:
        with open(requirements_path, 'r+') as requirements_file:
            requirements = requirements_file.read()
            if 'psycopg2-binary' not in requirements.lower():
                print('(++) Adding Postgres to project requirements.')
                requirements_file.write('\n\npsycopg2-binary==2.8.4')
        return 0
    except Exception as e:
        print(e)
        return 1


def inspect_mysql_dependency(requirements_path):
    try:
        with open(requirements_path, 'r+') as requirements_file:
            requirements = requirements_file.read()
            if 'mysqlclient' not in requirements.lower():
                print('(++) Adding MYSQL to project requirements.')
                requirements_file.write('\n\nmysqlclient==1.4.6')
        return 0
    except Exception as e:
        print(e)
        return 1


def inspect_django_dependency(requirements_path, path):
    try:
        with open(requirements_path, 'r+') as requirements_file:
            requirements = requirements_file.read()
            if 'django' not in requirements.lower():
                # checking if venv exists in project:
                venv_path = os.path.join(path, 'venv')
                if os.path.exists(venv_path):
                    r = os.system(
                        f"\n\n{os.path.join(venv_path, 'bin/pip')} freeze --version | grep Django >> {requirements_path}")
                else:
                    print('(++) Adding Django to project requirements.')
                    requirements_file.write('\n\nDjango')
        return r
    except Exception as e:
        print(e)
        return 1
