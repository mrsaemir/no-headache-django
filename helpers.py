# main functions for either initializing a
# new project or Dockerizing an existing one.

import os
import file_handlers as handlers
from exceptions import (EntryPointNotAvailable,
                        RequirementsNotAvailable)


# this function creates a Dockerfile.
# python version is the version specified for the Dockerfile and is required.
def create_Dockerfile(project_root, python_version, requirements_file=None,
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
            # creating project core folder.
            docker_file.write("WORKDIR /project_core\n")
            docker_file.write("COPY . /project_core\n\n")
            # managin staticfiles
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
            docker_file.write(f"""CMD ["{os.path.join('./', entrypoint_file)}"]\n""")

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
            entrypoint_file.write("# This docker file is automatically created by 'no-headache-django' project.\n")
            entrypoint_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            entrypoint_file.write("#!/bin/bash\n\n")
            managepy_relative_path = os.path.join(handlers.get_relative_path(managepy_abs_path,
                                                                             os.path.dirname(entrypoint_path)),
                                                  'manage.py'
                                                  )
            entrypoint_file.write(f"python {managepy_relative_path} migrate\n")
            entrypoint_file.write(f"python {managepy_relative_path} collectstatic --noinput\n")
            # setting wsgi file.
            wsgi_file = handlers.get_relative_path(handlers.get_wsgi_file(project_root),
                                                   os.path.dirname(entrypoint_path))
            wsgi_file_dir_name = os.path.dirname(wsgi_file)
            entrypoint_file.write(f"gunicorn {wsgi_file_dir_name}.wsgi:application -w 2 -b :8000\n")

            print(f"(++) entrypoints.sh file created in {entrypoint_path}")
    except Exception as e:
        print('(!!) An error occurred. rolling back ... ')
        os.system(f'rm {entrypoint_path}')
        print('(!!) Docker file deleted. raising the exception ...')
        raise
    return entrypoint_path


def create_requirements(project_root):
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    requirements_file_path = os.path.join(managepy_abs_path, 'requirements.txt')
    if not os.path.exists(requirements_file_path):
        with open(requirements_file_path, 'w') as requirements_file:
            requirements_file.write("# This docker file is automatically created by 'no-headache-django' project.\n")
            requirements_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            requirements_file.write('\ngunicorn==19.9.0')
    return requirements_file_path


# this function checks if a certain requiremets file contains gunicorn.
def inspect_requirements(requirements_path):
    with open(requirements_path) as requirements_file:
        requirements = requirements_file.read()
        if 'gunicorn' not in requirements.lower():
            print('(++) Adding Gunicorn to project requirements.')
            requirements_file.write('\ngunicorn==19.9.0')
