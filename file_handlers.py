# these functions are not written for high performance use.
import os
from exceptions import ManageFileNotAvailable, SettingsFileNotAvailable, WsgiFileNotAvailable


# this function returns the absolute path of the
# file specified with filename. it searches for
# the file recursively and returns all possible
# answers.
# root_dir is the top directory of our search
def get_absolute_path(root_dir, filename):
    result = []
    contents = os.listdir(root_dir)
    for content in contents:
        # determining contents absolute path
        content = os.path.join(root_dir, content)

        if os.path.isdir(content):
            res = get_absolute_path(content, filename)
            if res:
                # this for loop is needed for avoiding nested python lists.
                for item in res:
                    result.append(item)

        # if the file path ends with our desired filename, then it is our case!
        elif content.endswith(filename):
            result.append(content)

    return result


# returns the same part of two different paths.
# exp: path1 = '/home/user/project2/src'
# path2 = '/user/project2/src'
# result would be: '/user/projec2/src'
def get_relative_path(path1, path2):
    from pathlib import Path
    return Path(path1).relative_to(path2)


# this module will join txt files together.
# file1 and file2 are abs path for two files.
# it adds file2 to the end of file1 in a new file.
def join_files(file1, file2, newfile_path):
    with open(newfile_path, 'w') as out_file:
        for file in (file1, file2):
            with open(file) as in_file:
                out_file.write(in_file.read())
    return newfile_path


# this will add a txt to a text file(abs path required).
# add_to_top is True is adds it to the top of the text file.
# this function automatically adds newline when required.
def add_to_file(text, file, add_to_top=False):

    if add_to_top:
        with open(file) as in_file:
            file_contents = in_file.read()

        # removing the file
        os.system(f"rm {file}")

        with open(file, 'w') as out_file:
            out_file.write(text)
            out_file.write('\n')
            out_file.write(file_contents)
    else:
        with open(file, 'a') as file:
            # going to new line
            file.write('\n')
            file.write(text)

    # returning the path for result file.
    return file


def get_managepy_path(project_root):
    # finding manage.py abs path
    managepy = get_absolute_path(project_root, 'manage.py')

    if not managepy:
        raise ManageFileNotAvailable(
            f"(!!) Can not find 'manage.py' file within directory: {project_root}"
        )

    # if there are more than one manage.py module then raise an error.
    managepy_len = len(managepy)
    if managepy_len != 1:
        raise FileExistsError(
            f"""(!!) There are more than one manage.py modules within this directory ({project_root}),
            Try resolving this problem by giving the exact project root.
            Found manage.py modules are:
            {managepy}
            """
        )

    return managepy[0]


def get_wsgi_file(project_root):
    managepy_abs_path = get_managepy_path(project_root)
    wsgi_file = get_absolute_path(os.path.dirname(managepy_abs_path), 'wsgi.py')
    if not wsgi_file:
        raise WsgiFileNotAvailable(
            f"(!!) Can not find 'wsgi.py' file within directory: {project_root}"
        )
    if len(wsgi_file) != 1:
        raise FileExistsError(
            f"""(!!) There are more than one wsgi.py modules within this directory ({project_root}),
            Found wsgi.py modules are:
            {wsgi_file}
            """
        )
    return wsgi_file[0]


def get_settings_file(project_root):
    try:
        manage_py_path = get_managepy_path(project_root)
        settings_abs_path = get_absolute_path(os.path.dirname(manage_py_path), 'settings.py')
        if not settings_abs_path:
            raise SettingsFileNotAvailable(
                f"(!!) Can not find 'settings.py' file within directory: {project_root}"
            )
        if len(settings_abs_path) != 1:
            raise FileExistsError(
                f"""(!!) There are more than one settings.py modules within this directory ({project_root}),
                Found settings.py modules are:
                {settings_abs_path}
                """
            )
        return settings_abs_path[0]
    except PermissionError as e:
        raise PermissionError("Need root access")


# a function that says if a user is admin
def can_sudo():
    import os
    user = os.getenv("SUDO_USER")
    if user is None:
        return False
    return True


def replace_word_in_file(file_path, original, replace_with):
    with open(file_path, 'r') as f:
        file = f.read()
        file = file.replace(original, replace_with)
    with open(file_path, 'w') as f:
        f.write(file)


def create_hash_name(len):
    import random
    import string
    rand_str = lambda n: ''.join(
        [random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(n)])

    return rand_str(len)

