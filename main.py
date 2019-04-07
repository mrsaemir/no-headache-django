import os
import helpers
from file_handlers import can_sudo, get_settings_file, get_managepy_path
import sys


# starting a new project
def startproject(project_name, project_root, db, python_version):
    if not helpers.has_valid_name_django(project_name):
        raise IOError("(!!) Project names only have numbers, letters or underscores.")

    project_path = os.path.join(project_root, project_name)

    if os.path.exists(project_path):
        print(f"(!!) A project named {project_name} already exists in {project_root}.")
        print(f"If you Continue there may be bad consequences!")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print(f"(!!) Avoiding creation of of project {project_name} in {project_root}")
            return

    try:

        print(f"(++) Initializing project {project_name} with python{python_version}")
        # starting project
        helpers.init_dj_project(project_name, project_path, python_version)
        helpers.design_settings_file(project_name, project_path, db, python_version)
        # checking dependencies
        requirements_path = helpers.get_or_create_requirements(project_path)
        helpers.inspect_django_dependency(requirements_path, project_root)
        helpers.inspect_gunicorn_dependency(requirements_path)

        if db == 'postgres':
            helpers.inspect_postgres_dependency(requirements_path)
        elif db == 'mysql':
            helpers.inspect_mysql_dependency(requirements_path)
        else:
            raise NotImplementedError()

        # creating Dockerfile
        helpers.create_entrypoint(project_path)
        helpers.create_Dockerfile(project_path, f"python:{python_version}", db=db)
        # creating docker-compose file
        helpers.create_docker_compose(project_path, db)
        # starting version control
        helpers.init_git(os.path.join(project_path, project_name))
        # adding readme.rst
        helpers.add_readme_file(os.path.join(project_path, project_name))

    except PermissionError as e:
        if can_sudo():
            pass
        else:
            raise PermissionError("(!!) Permission Required!. Run as Administrator or change permissions.")

    except Exception as e:
        raise

    finally:
        if can_sudo():
            print("(!!) Resetting permissions")
            os.system(f'chmod 777 -R {project_path}')


# for the use of projects that are not initiated using this awesome script
def dockerize(project_root, python_version):
    # assuming no settings are disabled at first.
    disabled_settings = False

    if not os.path.exists(project_root):
        raise FileNotFoundError("Can not find your project.")

    print('(!!) Use with CAUTION! Your projects structure may be not standard and running this project may cause problems in your scripts. Take backups.')

    choice = input("To continue press c/C: ")
    if choice.lower() != 'c':
        print("(!!) Avoiding Dockerization.")
        return

    try:
        try:
            get_settings_file(project_root)
        except FileExistsError:
            # disabling settings that are not our desired ones.
            disabled_settings = helpers.disable_other_settings(project_root)

        # auto-detecting database system
        db = helpers.detect_database(get_settings_file(project_root))
        if not db:
            print('(!!) Can not auto-detect your database system.')
            db = input('(!!) What is your database? example: postgres\n')
        helpers.patch_settings(project_root, db)
        requirements_file = helpers.get_or_create_requirements(project_root)
        helpers.inspect_postgres_dependency(requirements_file)
        helpers.inspect_gunicorn_dependency(requirements_file)
        helpers.inspect_django_dependency(requirements_file, project_root)
        helpers.create_entrypoint(project_root)
        helpers.create_Dockerfile(project_root, f"python:{python_version}", 'postgres')
        helpers.create_docker_compose(project_root, db)

        print("(!!) Successfully dockerized your project. Dockerization may have problems in some cases which project structure is not standard.")
        print("(!!) Check standard project structure in http://github.com/mrsaemir/no-headache-django README.md")

    except PermissionError as e:
        if can_sudo():
            pass
        else:
            print("(!!) Permission Required! Run as Administrator or change permissions.")
            return

    except Exception as e:
        raise

    finally:
        if disabled_settings:
            # enabling disabled settings.
            helpers.enable_other_settings(disabled_settings)
        if can_sudo():
            print("(!!) Resetting permissions")
            os.system(f'chmod 777 -R {project_root}')


def up(project_root=None, daemon=False):
    import exceptions
    if not can_sudo():
        raise PermissionError('You need sudo access to run docker!')
    else:
        if not (helpers.is_installed('docker') and helpers.is_installed('docker-compose')):
            raise exceptions.LinuxProgramNotInstalled("Requirements Not installed! Run: 'apt install docker docker.io docker-compose'")
        if project_root:
            # preferred dir
            compose = os.path.join(os.path.dirname(get_managepy_path(project_root)),
                                   'docker-compose.yaml')
        else:
            # current dir
            compose = '.'
        if not daemon:
            os.system(f'cd {os.path.dirname(compose)} && docker-compose up')
        else:
            os.system(f'cd {os.path.dirname(compose)} && docker-compose up -d')


def down(project_root=None):
    import exceptions
    if not can_sudo():
        raise PermissionError('You need sudo access to run docker!')
    else:
        if not (helpers.is_installed('docker') and helpers.is_installed('docker-compose')):
            raise exceptions.LinuxProgramNotInstalled("Requirements Not installed! Run: 'apt install docker docker.io docker-compose'")
        if project_root:
            # preferred dir
            compose = os.path.join(os.path.dirname(get_managepy_path(project_root)),
                                   'docker-compose.yaml')
        else:
            # current dir
            compose = '.'
        os.system(f'cd {os.path.dirname(compose)} && docker-compose down')


# getting a shell inside your docker container
def shell(project_root=None):
    import exceptions
    if not can_sudo():
        raise PermissionError('You need sudo access to run docker!')
    else:
        if not (helpers.is_installed('docker') and helpers.is_installed('docker-compose')):
            raise exceptions.LinuxProgramNotInstalled("Requirements Not installed! Run: 'apt install docker docker.io docker-compose'")
        if project_root:
            # preferred dir
            compose = os.path.join(os.path.dirname(get_managepy_path(project_root)),
                                   'docker-compose.yaml')
        else:
            # current dir
            compose = '.'
        os.system(f'cd {os.path.dirname(compose)} && docker-compose exec web bash')


# total shit!
if __name__ == "__main__":
    if sys.argv[1].lower() == 'startproject':
        startproject(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))

    elif sys.argv[1].lower() == 'dockerize':
        dockerize(os.path.abspath(sys.argv[2]), sys.argv[3])

    elif sys.argv[1].lower() == 'up':
        try:
            is_daemon = sys.argv[3]
            if is_daemon.lower() == 'daemon':
                up(os.path.abspath(sys.argv[2]), True)
            else:
                up(os.path.abspath(sys.argv[2]), False)
        except IndexError:
            up(os.path.abspath(sys.argv[2]), False)

    elif sys.argv[1].lower() == 'down':
        down(os.path.abspath(sys.argv[1]))

    elif sys.argv[1].lower() == 'shell':
        shell(os.path.abspath(sys.argv[2]))

    else:
        raise NotImplemented("Command Not Found.")
