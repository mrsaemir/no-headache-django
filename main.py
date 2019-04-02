import os
import helpers
from file_handlers import can_sudo
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
            raise PermissionError("(!!) Run as Administrator or change permissions.")

    except Exception as e:
        raise

    finally:
        if can_sudo():
            print("(!!) Resetting permissions")
            os.system(f'chmod 777 -R {project_path}')


# for the use of projects that are not initiated using this awesome script
def dockerize(project_root, python_version, db):
    if not os.path.exists(project_root):
        raise FileNotFoundError("Can not find your project.")

    print('(!!) Use with CAUTION! Your projects structure may be not standard and running this project may cause problems in your scripts. Take backups.')

    choice = input("To continue press c/C: ")
    if choice.lower() != 'c':
        print("(!!) Avoiding Dockerization.")
        return

    try:
        # disabling settings that are not our desired ones.
        disabled_settings = helpers.disable_other_settings(project_root)
        helpers.patch_settings(project_root, db)
        requirements_file = helpers.get_or_create_requirements(project_root)
        helpers.inspect_postgres_dependency(requirements_file)
        helpers.inspect_gunicorn_dependency(requirements_file)
        helpers.inspect_django_dependency(requirements_file, project_root)
        helpers.create_entrypoint(project_root)
        helpers.create_Dockerfile(project_root, f"python:{python_version}", 'postgres')
        helpers.create_docker_compose(project_root, db)
        # enabling disabled settings.


        print("(!!) Successfully dockerized your project. Dockerization may have problems in some cases which project structure is not standard.")
        print("(!!) Check standard projec structure in http://github.com/mrsaemir/no-headache-django README.md")

    except PermissionError as e:
        if can_sudo():
            pass
        else:
            raise PermissionError("(!!) Run as Administrator or change permissions.")

    except Exception as e:
        raise

    finally:
        helpers.enable_other_settings(disabled_settings)
        if can_sudo():
            print("(!!) Resetting permissions")
            os.system(f'chmod 777 -R {project_root}')

            
if __name__ == "__main__":
    if sys.argv[1].lower() == 'startproject':
        startproject(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))
