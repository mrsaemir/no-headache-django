# main functions for either initializing a
# new project or Dockerizing an existing one.

import os
import file_handlers as handlers
from exceptions import (EntryPointNotAvailable,
                        RequirementsNotAvailable,
                        LinuxProgramNotInstalled)


# this function creates a Dockerfile.
# python version is the version specified for the Dockerfile and is required.
def create_Dockerfile(project_root, python_version, db, requirements_file=None,
                      entrypoint_file=None):
    # Dockerfile path
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    docker_path = os.path.join(managepy_abs_path, 'Dockerfile')

    # if the docker file already exists, then do nothing
    docker_file_check = handlers.get_absolute_path(project_root, 'Dockerfile')
    if docker_file_check:
        print(
            f"(!!) A Dockerfile already exists in {docker_file_check}"
        )
        print(f"If you continue, a new Docker file will be created in {docker_path}")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print("(!!) Avoiding creation of a new Dockerfile")
            return

    # creating Dockerfile
    try:
        with open(docker_path, 'w') as docker_file:
            docker_file.write("# This docker file is automatically created by 'no-headache-django' project.\n")
            docker_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            # including desired python version.
            docker_file.write(f"\nFROM {python_version}\n\n")
            # settings general env vars.
            docker_file.write("ENV PYTHONDONTWRITEBYTECODE 1\n")
            docker_file.write("ENV PYTHONUNBUFFERED 1\n\n")
            if db == 'postgres':
                docker_file.write("RUN apt update && install libpq-dev\n\n")
            elif db == 'mysql':
                #docker_file.write("RUN apt update && apt install libmysqlclient-dev\n\n")
                pass
            else:
                raise NotImplementedError()
            # creating project core folder.
            docker_file.write("WORKDIR /project_core\n")
            docker_file.write("COPY . /project_core\n\n")
            # managing staticfiles
            docker_file.write("RUN mkdir -p media\n")
            docker_file.write("RUN mkdir -p static\n\n")
            # opening port 8000 by default.
            docker_file.write("EXPOSE 8000\n\n")

            # finding requirements.txt or using the provided one.\
            if requirements_file:
                requirements_file = [requirements_file]
            else:
                requirements_file = handlers.get_absolute_path(project_root, 'requirements.txt')

            if not requirements_file:
                raise RequirementsNotAvailable(
                    f"""(!!) requirements file not found in {project_root}.
                    This file is required in order to install python dependencies using pip.
                    Either create one named "requirements.txt" or represent yours.
                    """
                )
            if len(requirements_file) != 1:
                raise FileExistsError(
                    f"""(!!) There are more than one requirements file in your project root: {project_root}
                    please specify one: {requirements_file}
                    """
                )
            requirements_file = requirements_file[0]
            docker_file.write(f"RUN pip install -r {handlers.get_relative_path(requirements_file, os.path.dirname(docker_path))}\n\n")

            # finding entrypoint.sh or using the provided one.
            if entrypoint_file:
                entrypoint_file = [entrypoint_file]
            else:
                entrypoint_file = handlers.get_absolute_path(project_root, 'entrypoint.sh')

            if not entrypoint_file:
                raise EntryPointNotAvailable(
                    f"""(!!) entrypoint file not found in {project_root}.
                    This file is required in order to be run when an instance of docker is initialized.
                    Either create one named "entrypoint.sh" or represent yours.
                    """
                )
            if len(entrypoint_file) != 1:
                raise FileExistsError(
                    f"""(!!) There are more than one requirements file in your project root: {project_root}
                    please specify one: {entrypoint_file}
                    """
                )
            entrypoint_file = entrypoint_file[0]
            # relative path to Dockerfile
            entrypoint_file = handlers.get_relative_path(entrypoint_file, os.path.dirname(docker_path))
            docker_file.write(f"RUN chmod +x {entrypoint_file}\n\n")
            docker_file.write(f"""CMD ["bash", "{os.path.join('/project_core/', entrypoint_file)}"]\n""")

        print(f"(++) Docker file created in {docker_path}")
    except Exception as e:
        print('(!!) An error occurred. rolling back ... ')
        os.system(f'rm {docker_path}')
        print('(!!) Docker file deleted. raising the exception ...')
        raise


def create_entrypoint(project_root):
    # Dockerfile path
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    entrypoint_path = os.path.join(managepy_abs_path, 'entrypoint.sh')

    # checking if there are no entrypoints available.
    entrypoint_check = handlers.get_absolute_path(project_root, 'entrypoint.sh')
    if entrypoint_check:
        print(
            f"(!!) An entrypoint.sh file already exists in {entrypoint_check}"
        )
        print(f"If you continue, a new entrypoint file will be created in {entrypoint_path}")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print("(!!) Avoiding creation of a new entrypoint.sh file")
            return

    # creating entrypoint.sh file
    try:
        with open(entrypoint_path, 'w') as entrypoint_file:
            entrypoint_file.write("# This file is automatically created by 'no-headache-django' project.\n")
            entrypoint_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            entrypoint_file.write("#!/bin/bash\n\n")
            managepy_relative_path = os.path.join(handlers.get_relative_path(managepy_abs_path,
                                                                             os.path.dirname(entrypoint_path)),
                                                  'manage.py'
                                                  )
            entrypoint_file.write(f"python {managepy_relative_path} makemigrations\n")
            entrypoint_file.write(f"python {managepy_relative_path} migrate\n")
            entrypoint_file.write(f"python {managepy_relative_path} collectstatic --noinput\n")
            # setting wsgi file.
            wsgi_file = handlers.get_wsgi_file(project_root)
            wsgi_file_rel_path = handlers.get_relative_path(os.path.dirname(wsgi_file), managepy_abs_path)

            entrypoint_file.write(f"gunicorn {wsgi_file_rel_path}.wsgi:application -w 2 -b :8000\n")

            print(f"(++) entrypoints.sh file created in {entrypoint_path}")
    except Exception as e:
        print('(!!) An error occurred. rolling back ... ')
        os.system(f'rm {entrypoint_path}')
        print('(!!) Entrypoint.sh file deleted. raising the exception ...')
        raise
    return entrypoint_path


def get_or_create_requirements(project_root):
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    requirements_file_path = os.path.join(managepy_abs_path, 'requirements.txt')
    if not os.path.exists(requirements_file_path):
        try:
            with open(requirements_file_path, 'w') as requirements_file:
                print(f"(++) Requirements.txt file created in {requirements_file_path}")
        except Exception as e:
            print('(!!) An error occurred. rolling back ... ')
            os.system(f'rm {requirements_file_path}')
            print('(!!) Requirements.txt file deleted. raising the exception ...')
            raise
    # inspecting requirements ...
    inspect_django_dependency(requirements_file_path, project_root)
    inspect_gunicorn_dependency(requirements_file_path)
    return requirements_file_path


# this function checks if a certain requirements file contains gunicorn.
def inspect_gunicorn_dependency(requirements_path):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'gunicorn' not in requirements.lower():
            print('(++) Adding Gunicorn to project requirements.')
            requirements_file.write('\ngunicorn==19.9.0')


def inspect_postgres_dependency(requirements_path):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'psycopg2-binary' not in requirements.lower():
            print('(++) Adding Postgres to project requirements.')
            requirements_file.write('\n\npsycopg2-binary==2.7.4')


def inspect_mysql_dependency(requirements_path):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'mysqlclient' not in requirements.lower():
            print('(++) Adding MYSQL to project requirements.')
            requirements_file.write('\n\nmysqlclient==1.4.2')


def inspect_django_dependency(requirements_path, project_root):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'django' not in requirements.lower():
            # checking if venv exists in project:
            venv_path = os.path.join('../', project_root, 'venv')
            if os.path.exists(venv_path):
                #raise IOError()
                os.system(f"{os.path.join(venv_path, 'bin/pip')} freeze --version | grep Django >> {requirements_path}")
            else:
                print('(++) Adding Django to project requirements.')
                requirements_file.write('\nDjango')


# for new projects only!
def design_settings_file(project_name, project_root, db, python_version):
    settings_module = handlers.get_settings_file(project_root)
    settings_backup = settings_module + '.backup'

    try:
        # replacing the new one.
        if python_version >= 3:
            if db == 'postgres':
                os.system(f'mv {settings_module} {settings_backup}')
                os.system(f'cp ./dj/dj2/postgres/settings.py {settings_module}')
                inspect_postgres_dependency(get_or_create_requirements(project_root))
                os.system(f"rm {settings_backup}")

                with open(settings_module, 'a+') as settings:
                    settings.write(f"\n\nROOT_URLCONF = '{project_name}.urls'")
                    settings.write(f"\nWSGI_APPLICATION = '{project_name}.wsgi.application'")
            elif db == 'mysql':
                os.system(f'mv {settings_module} {settings_backup}')
                os.system(f'cp ./dj/dj2/mysql/settings.py {settings_module}')
                inspect_mysql_dependency(get_or_create_requirements(project_root))
                os.system(f"rm {settings_backup}")

                with open(settings_module, 'a+') as settings:
                    settings.write(f"\n\nROOT_URLCONF = '{project_name}.urls'")
                    settings.write(f"\nWSGI_APPLICATION = '{project_name}.wsgi.application'")
            else:
                raise NotImplementedError()
        else:
            if db == 'postgres':
                os.system(f'mv {settings_module} {settings_backup}')
                os.system(f'cp ./dj/dj1/postgres/settings.py {settings_module}')
                inspect_mysql_dependency(get_or_create_requirements(project_root))
                os.system(f"rm {settings_backup}")

                with open(settings_module, 'a+') as settings:
                    settings.write(f"\nROOT_URLCONF = '{project_name}.urls'")
                    settings.write(f"\nWSGI_APPLICATION = '{project_name}.wsgi.application'")
            elif db == 'mysql':
                os.system(f'mv {settings_module} {settings_backup}')
                os.system(f'cp ./dj/dj1/mysql/settings.py {settings_module}')
                inspect_mysql_dependency(get_or_create_requirements(project_root))
                os.system(f"rm {settings_backup}")

                with open(settings_module, 'a+') as settings:
                    settings.write(f"\nROOT_URLCONF = '{project_name}.urls'")
                    settings.write(f"\nWSGI_APPLICATION = '{project_name}.wsgi.application'")
            else:
                raise NotImplementedError("version 1 settings")

    except Exception as e:
        print('(!!) An error occurred designing settings file. rolling back ... ')
        os.system(f"mv {settings_backup} {settings_module}")
        raise


# inspects if a program is installed in linux
def is_installed(program_name):
    from shutil import which
    return which(program_name) is not None


# python/django version are version numbers.
def init_dj_project(project_name, project_root, python_version, django_version=None):
    project_path = os.path.exists(os.path.join(project_root, project_name))
    if project_path:
        print('(!!) Project already exists. avoiding creation')
        return

    if not is_installed(f'python{python_version}'):
        raise LinuxProgramNotInstalled(f'python{python_version}')

    if not is_installed('virtualenv'):
        raise LinuxProgramNotInstalled('virtualenv')

    # creating virtuelenv
    venv_path = os.path.join('../', project_root, 'venv')
    if not os.path.exists(venv_path):
        os.system(f'virtualenv --python python{python_version} {venv_path}')

    # installing django
    if django_version:
        os.system(f'{os.path.join(venv_path, "bin/pip")} install django=={django_version}')
        # creating the project
        try:
            os.system(f'cd {project_root} && {os.path.join(venv_path, "bin/django-admin")} startproject {project_name}')
            inspect_django_dependency(get_or_create_requirements(project_root), project_root)
        except:
            print("(!!) Error. Rolling back ... ")
            os.system(f'rm -rf {project_path}')
            raise
    else:
        os.system(f'{os.path.join(venv_path, "bin/pip")} install django')
        # creating the project
        os.system(f'cd {project_root} && {os.path.join(venv_path, "bin/django-admin")} startproject {project_name}')
        inspect_django_dependency(get_or_create_requirements(project_root), project_root)


def init_git(project_root):
    try:
        if not is_installed(f'git'):
            raise LinuxProgramNotInstalled(f'git')
        # creating Git only if it does not exist.
        if not os.path.exists(os.path.join('../', project_root, '.git')):
            os.system(f'cd {project_root} && git init')
            if not os.path.exists(os.path.join(project_root, '.gitignore')):
                print("(++) Added .gitignore file")
                os.system(f'cd {project_root} && touch .gitignore')
        else:
            print('(!!) Git repository already exists. Avoiding creation.')
    except:
        pass


def add_readme_file(project_root):
    readme_path = os.path.join(project_root, 'README.rst')
    if not os.path.exists(readme_path):
        import datetime
        print("(++) Added README.rst file")
        with open(readme_path, 'w') as readme:
            readme.write(f"Created on {datetime.date.today()} using no-headache-django automatic project initializer.")


def create_docker_compose(project_root, db):
    manage_py_path = os.path.dirname(handlers.get_managepy_path(project_root))
    docker_compose_path = os.path.join(manage_py_path, 'docker-compose.yaml')

    # avoiding creation if it exists.
    if os.path.exists(docker_compose_path):
        print(
            f"(!!) A docker-compose file already exists in {manage_py_path}"
        )
        print(f"If you continue, a new docker compose file will be created in {docker_compose_path}")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print("(!!) Avoiding creation of a new Dockerfile")
            return
    docker_compose_path = os.path.join(os.path.dirname(handlers.get_managepy_path(project_root)), "docker-compose.yaml")
    if db == 'postgres':
        os.system(f'cp ./docker-compose/postgres/docker-compose.yaml {docker_compose_path}')
        handlers.replace_word_in_file(docker_compose_path, '../development_data', f'../development_data_{handlers.create_hash_name(6)}')

    elif db == 'mysql':
        os.system(f'cp ./docker-compose/mysql/docker-compose.yaml {docker_compose_path}')
        handlers.replace_word_in_file(docker_compose_path, '../development_data',
                                      f'../development_data_{handlers.create_hash_name(6)}')
    else:
        raise NotImplementedError()


def has_valid_name_django(name):
    import re
    return re.fullmatch(r'[a-z0-9_]+', name.lower())


# patching settings for old projects that are not initialized by this script
def patch_settings(project_root, db):
    settings_module = handlers.get_settings_file(project_root)
    settings_backup = settings_module + '.backup'
    try:
        os.system(f'cp {settings_module} {settings_backup}')
        if db == 'postgres':
            with open('./patches/postgres/patches.py', 'r') as patch:
                patch = patch.read()
            handlers.add_to_file(patch, settings_module)
            inspect_postgres_dependency(get_or_create_requirements(project_root))
            os.system(f"rm {settings_backup}")
            print("(++) Successfully patched your project to be used with postgres")
        elif db == 'mysql':
            with open('./patches/mysql/patches.py', 'r') as patch:
                patch = patch.read()
            handlers.add_to_file(patch, settings_module)
            inspect_postgres_dependency(get_or_create_requirements(project_root))
            os.system(f"rm {settings_backup}")
            print("(++) Successfully patched your project to be used with mysql")

        else:
            raise NotImplementedError()

    except Exception as e:
        print("(!!) Can not patch. rolling back ...")
        os.system(f"mv {settings_backup} {settings_module}")
        raise


def disable_other_settings(project_root):
    settings_modules = handlers.get_absolute_path(project_root, 'settings.py')
    if len(settings_modules) > 1:
        print("(!!) Found more than one settings module.")
        print("(??) Which one is your desired one? ")
        for i in range(len(settings_modules)):
            print(f"{i} - {settings_modules[i]}")
        choice = int(input("Enter your project setting's index number: "))
        assert (-1 < choice < len(settings_modules))
        settings_modules.pop(choice)
        for settings in settings_modules:
            os.system(f'mv {settings} {settings}.tmp 2>/dev/null ')
        # returning the list of disabled settings
        return settings_modules


def enable_other_settings(disabled_settings):
    if disabled_settings:
        for settings in disabled_settings:
            os.system(f'mv {settings}.tmp {settings} 2>/dev/null ')


def detect_database(settings_path):
    with open(settings_path, 'r') as settings:
        settings = settings.read()
    if 'django.db.backends.postgresql' in settings:
        return 'postgres'
    elif 'django.db.backend.mysql' in settings:
        return 'mysql'
    else:
        return None
