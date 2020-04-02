import os
import datetime
import dependencies
from helpers import create_hash_name, replace_word_in_file
import settings

# location of package files.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def init_django(project_name, path, python_version, django_version=None):
    # NOTE: r is the return code of each run
    # creating virtuelenv
    venv_path = os.path.join('../', path, 'venv')
    r = os.system(f'virtualenv --python python{python_version} {venv_path}')

    # installing django
    if django_version:
        r = r + os.system(f'{os.path.join(venv_path, "bin/pip")} install django=={django_version}')
        # creating the project
        r = r + os.system(f'cd {path} && {os.path.join(venv_path, "bin/django-admin")} startproject {project_name}')

    else:
        r = r + os.system(f'{os.path.join(venv_path, "bin/pip")} install django')
        # creating the project
        r = r + os.system(f'cd {path} && {os.path.join(venv_path, "bin/django-admin")} startproject {project_name}')

    if r == 0:
        print("Added Django project")
    return r


def init_git(path):
    r = os.system(f'cd {path} && git init')
    r = r + os.system(f'cd {path} && touch .gitignore')
    if r == 0:
        print("(++) Added .gitignore file")
    return r


def init_readme(path):
    readme_path = os.path.join(path, 'README.rst')

    try:
        with open(readme_path, 'w') as readme:
            readme.write(
                f"## Created on {datetime.date.today()} using NO-HEADACHE-DJANGO automatic project initializer.")
        print("(++) Added README.rst file")
        return 0
    except Exception as e:
        print(e)
        return 1


def init_requirements(path, project_name, db):
    req_path = os.path.join(os.path.join(path, project_name), 'requirements.txt')
    r = os.system(f'cd {os.path.join(path, project_name)} && touch requirements.txt')

    r = r + dependencies.inspect_django_dependency(req_path, path)
    r = r + dependencies.inspect_gunicorn_dependency(req_path)

    if db == 'sqlite':
        # no action needed
        pass
    elif db == 'postgres':
        r = r + dependencies.inspect_postgres_dependency(req_path)
    elif db == 'mysql':
        r = r + dependencies.inspect_mysql_dependency(req_path)
    else:
        print(f"Can't work with {db}")
        r = r + 1

    if r == 0:
        print(f"(++) Added Requirements.txt file")
    return r


# this function creates a Dockerfile.
# python version is the version specified for the Dockerfile and is required.
def init_dockerfile(path, python_version, db):
    docker_path = os.path.join(path, 'Dockerfile')

    try:
        # creating Dockerfile
        with open(docker_path, 'w') as docker_file:
            # no-headache-django
            docker_file.write("\n# This docker file is automatically created by NO-HEADACHE-DJANGO")
            docker_file.write("\n# Please star me on github: http://github.com/mrsaemir/no-headache-django")

            # including desired python version.
            docker_file.write("\n\n# Base Python docker image:")
            docker_file.write(f"\nFROM python:{python_version}")

            # general python env vars.
            docker_file.write("\n\n# These variables are required for Python:")
            docker_file.write("\nENV PYTHONDONTWRITEBYTECODE 1")
            docker_file.write("\nENV PYTHONUNBUFFERED 1")

            # database-required libraries
            docker_file.write("\n\n# Database-related libraries:")
            if db == 'sqlite':
                # no action needed
                pass
            elif db == 'postgres':
                docker_file.write("\nRUN apt update && apt install -y libpq-dev")
            elif db == 'mysql':
                docker_file.write("\nRUN apt update && apt install -y python-mysqldb")
            else:
                raise NotImplementedError()

            # creating a non-root user
            docker_file.write("\n\n# Creating a non-root user:")
            docker_file.write("\nRUN useradd -ms /bin/bash user")

            # creating project core folder.
            docker_file.write("\n\n# Setting project's working directory:")
            docker_file.write("\nWORKDIR /home/user/project_core")
            docker_file.write("\nCOPY . /home/user/project_core")

            # managing staticfiles
            docker_file.write("\n\n# Static Files:")
            docker_file.write("\nRUN mkdir -p /home/user/media")
            docker_file.write("\nRUN mkdir -p /home/user/static")

            # installing pip requirements
            docker_file.write("\n\n# Installing project requirement:")
            docker_file.write(
                f"\nRUN pip install -r ./requirements.txt"
            )

            # setting right file permissions
            docker_file.write("\n\n# Setting right file permissions:")
            docker_file.write("\nRUN chmod -R 777 /home/user")
            docker_file.write(f"\nRUN chmod +x ./entrypoint.sh")

            # changing to non-root user
            docker_file.write(f"\n\n# Changing to non-root user:")
            docker_file.write("\nUSER user")

            # opening port 8000
            docker_file.write("\n\n# Opening port 8000:")
            docker_file.write("\nEXPOSE 8000")
            docker_file.write("\nCMD ['bash', './entrypoint.sh']")

        print(f"(++) Added Dockerfile")
        return 0
    except Exception as e:
        print(e)
        return 1


def init_docker_compose(path, db):
    try:
        docker_compose_path = os.path.join(path, "docker-compose.yaml")
        devel_data = f'../development_data_{create_hash_name(6)}'

        if db == 'sqlite':
            os.system(f'cp {os.path.join(BASE_DIR, "docker-compose/sqlite/docker-compose.yaml")} {docker_compose_path}')
            replace_word_in_file(docker_compose_path, '../development_data', devel_data)
            pass

        elif db == 'postgres':
            os.system(f'cp {os.path.join(BASE_DIR, "docker-compose/postgres/docker-compose.yaml")} {docker_compose_path}')
            replace_word_in_file(docker_compose_path, '../development_data', devel_data)

        elif db == 'mysql':
            os.system(f'cp {os.path.join(BASE_DIR, "docker-compose/mysql/docker-compose.yaml")} {docker_compose_path}')
            replace_word_in_file(docker_compose_path, '../development_data', f"../{devel_data}")
        else:
            raise NotImplementedError(f"{db} Not Supported")
        os.system(f"mkdir -p {os.path.join(os.path.dirname(docker_compose_path), devel_data, 'media')}")
        os.system(f"mkdir -p {os.path.join(os.path.dirname(docker_compose_path), devel_data, 'static')}")
        return 0
    except Exception as e:
        print(e)
        return 1


def init_entrypoint(project_name, path):
    entrypoint_path = os.path.join(path, 'entrypoint.sh')
    # creating entrypoint.sh file
    try:
        with open(entrypoint_path, 'w') as entrypoint_file:
            entrypoint_file.write("# This file is automatically created by 'no-headache-django' project.\n")
            entrypoint_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            entrypoint_file.write("#!/bin/bash\n\n")
            entrypoint_file.write(f"python manage.py makemigrations\n")
            entrypoint_file.write(f"python manage.py migrate\n")
            entrypoint_file.write(f"python manage.py collectstatic --noinput\n")
            entrypoint_file.write(f"gunicorn {project_name}.wsgi:application -w 2 -b :8000\n")
        print(f"(++) entrypoints.sh file created in {entrypoint_path}")
        return 0
    except Exception as e:
        print(e)
        return 1


def init_envvars(project_name, path, db):

    r = settings.change_base_settings(os.path.join(path, f'{project_name}/settings.py'))

    # handling db
    if db == 'sqlite':
        # no action needed
        pass
    elif db == 'postgres':
        r += settings.add_postgres(os.path.join(path, f'{project_name}/settings.py'))
    elif db == 'mysql':
        r += settings.add_mysql(os.path.join(path, f'{project_name}/settings.py'))
    else:
        raise NotImplementedError(f"{db} Not Supported")

    return r
