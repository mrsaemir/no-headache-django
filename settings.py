import os
from pyeditor import PyEditor

BASE_CHANGES = {
    "SECRET_KEY": "os.environ.get('SECRET_KEY', None)",
    "DEBUG": "True if os.environ.get('DEBUG', 'false') == 'True' else False",
    "ALLOWED_HOSTS": "json.loads(os.environ.get('ALLOWED_HOSTS'))",
    "STATIC_ROOT": "'/home/user/static/'",
    "MEDIA_ROOT": "'/home/user/media/'",
}


BASE_DEFAULTS = {
    "SECRET_KEY": "top_secret",
    "DEBUG": "True",
    "ALLOWED_HOSTS": '["localhost", "127.0.0.1"]',
}

POSTGRES_CHANGES = {
    "DATABASES": """{
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT'),
    }
}
    """
}

POSTGRES_DEFAULTS = {
    "DB_NAME": "some_db",
    "DB_USER": "some_user",
    "DB_PASSWORD": "some_password",
    "DB_HOST": "db",
    "DB_PORT": "5432",
}

MYSQL_CHANGES = {
    "DATABASES": """{
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
          'autocommit': True,
        },
    }
}
    """
}

MYSQL_DEFAULTS = {
    "DB_NAME": "django_db",
    "DB_USER": "django",
    "DB_PASSWORD": "django_password",
    "DB_HOST": "mysql",
    "DB_PORT": "3306",
}

MONGO_CHANGES = {
    "DATABASES": """{
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': True,
        'NAME': os.environ.get('DB_NAME', None),
        'CLIENT': {
            'host': f'mongodb://{os.environ.get("DB_USER", None)}:{os.environ.get("DB_PASSWORD", None)}@'
                    f'{os.environ.get("DB_HOST", None)}:{int(os.environ.get("DB_PORT", None))}/'
                    f'{os.environ.get("DB_NAME", None)}',
            'port': int(os.environ.get('DB_PORT', None)),
            'username': os.environ.get('DB_USER', None),
            'password': os.environ.get('DB_PASSWORD', None),
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        }
    }
}
    """
}

MONGO_DEFAULTS = {
    "DB_NAME": "some_db",
    "DB_USER": "some_user",
    "DB_PASSWORD": "some_password",
    "DB_HOST": "db",
    "DB_PORT": "27017",
}


def add_single_envvar(env_file_path, key, val):
    try:
        env_file_path = os.path.join(env_file_path, 'vars.env')
        if not os.path.exists(env_file_path):
            with open(env_file_path, 'w') as file:
                file.write(f"\n{key}={val}")
        else:
            with open(env_file_path, 'a') as file:
                file.write(f"\n{key}={val}")
        return 0
    except Exception as e:
        print(e)
        return 1


def add_bulk_envvar(env_file_path, key_val_dict):
    r = 0
    for k, v in key_val_dict.items():
        r += add_single_envvar(env_file_path, k, v)
    return r


def change_base_settings(settings_path):
    r = 0
    try:
        env_path = os.path.dirname(os.path.dirname(settings_path))
        editor = PyEditor(settings_path)
        # adding base changes
        editor.bulk_exchange(BASE_CHANGES)
        editor.add_to_imports('json')
    except Exception as e:
        print(e)
        return 1

    # adding base changes
    r += add_bulk_envvar(env_path, BASE_DEFAULTS)

    return r


def add_postgres(settings_path):
    r = 0
    try:
        env_path = os.path.dirname(os.path.dirname(settings_path))
        editor = PyEditor(settings_path)
        # adding base changes
        editor.bulk_exchange(POSTGRES_CHANGES)
    except Exception as e:
        print(e)
        return 1

    # adding base changes
    r += add_bulk_envvar(env_path, POSTGRES_DEFAULTS)

    return r


def add_mysql(settings_path):
    r = 0
    try:
        env_path = os.path.dirname(os.path.dirname(settings_path))
        editor = PyEditor(settings_path)
        # adding base changes
        editor.bulk_exchange(MYSQL_CHANGES)
    except Exception as e:
        print(e)
        return 1

    # adding base changes
    r += add_bulk_envvar(env_path, MYSQL_DEFAULTS)

    return r


def add_mongo(settings_path):
    r = 0
    try:
        env_path = os.path.dirname(os.path.dirname(settings_path))
        editor = PyEditor(settings_path)
        # adding base changes
        editor.bulk_exchange(MONGO_CHANGES)
    except Exception as e:
        print(e)
        return 1

    # adding base changes
    r += add_bulk_envvar(env_path, MONGO_DEFAULTS)

    return r
