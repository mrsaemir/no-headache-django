from exceptions import LinuxProgramNotInstalled
from validators import *
import initiators


def init():
    project_name = None
    project_path = None
    python_version = None
    database = None

    # getting project name
    while not project_name:
        pn = input("What is the name of your new project? ").strip(' ')
        if has_valid_django_name(pn):
            project_name = pn
        else:
            print(f"--> '{pn}' is not a valid name. Try Again.")

    while not project_path:
        pp = input("\nWhat is the path for your new project? ").strip(" ")
        if has_valid_project_path(pp):
            project_path = os.path.join(pp, 'project_' + project_name)
            if os.path.exists(project_path):
                print("\n This Project already exists. Either change path or re-start the initializer.")
                project_path = None
                continue
            else:
                break
        print(f"--> '{pp}' is not a valid path. Try Again.")

    while not python_version:
        pv = input(f"\nWhat is the python version you want for your project? Choices: {PYTHON_VERSIONS} ")
        if has_valid_python_version(pv):
            python_version = pv
            if not is_installed(f'python{python_version}'):
                raise LinuxProgramNotInstalled(f'python{python_version}')
        else:
            print(f"--> '{pv}' is not a valid python version. Try Again.")

    while not database:
        db = input(f"\nWhat is your database? Choices: {DATABASES} ").strip(" ")
        if has_valid_database(db):
            database = db
        else:
            print(f"--> '{db}' is not a valid database. Try Again.")

    if not is_installed('git'):
        raise LinuxProgramNotInstalled(f'git')

    if not is_installed('virtualenv'):
        raise LinuxProgramNotInstalled('virtualenv')

    try:
        r = initiators.init_django(project_name, project_path, python_version)
        r = r + initiators.init_requirements(project_path, project_name, database)
        r = r + initiators.init_dockerfile(os.path.join(project_path, project_name), python_version, db=database)
        r = r + initiators.init_docker_compose(os.path.join(project_path, project_name), db=database)
        r = r + initiators.init_entrypoint(project_name, os.path.join(project_path, project_name))
        r = r + initiators.init_readme(os.path.join(project_path, project_name))
        r = r + initiators.init_envvars(project_name, os.path.join(project_path, project_name), db=database)
        r = r + initiators.init_git(os.path.join(project_path, project_name))

        if r == 0:
            print(f"Successfully created {project_name}")
        else:
            print("Can't create project. Rolling back ...")
            os.system(f'rm -r {project_path}')
    except Exception as e:
        print(e)
        print("Can't create project. Rolling back ...")
        os.system(f'rm -r {project_path}')


if __name__ == '__main__':
    init()
