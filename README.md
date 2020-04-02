# NO-HEADACHE-DJANGO
NHD is a django project initializer that easily assembles a full project
for you!

By using NHD you will have instant access to these requirements for
every modern project:
  - Your Django Project
  - Dockerfile that is designed for your project
  - docker-compose.yaml suitable for firing your project
  - requirements.txt file
  - vars.env file
  - README.rst file
  - Git source code controller
  - and a bunch of other needed actions in order to produce a stable project that is ready to deploy

### Generating A New Project using NO-HEADACHE-DJANGO:

NHD requires python3, python3-pip and virtualenv. So you need to install them
before attempting to generate a new project.

Install the dependencies (For Ubuntu)

```sh
$ git clone https://github.com/mrsaemir/no-headache-django.git
$ sudo apt install python3 python3-pip  virtualenv docker docker.io docker-compose
$ cd no-headache-django
$ python3 main.py
```

### Developing a Django project using NHD:

Developing a Django project is extremely easy this way.
You have this chance to develop a project in the exact same environment
as deployment.

To work on a newly generated project, follow these steps:
```sh
$ cd <your_project_path>
$ cd <your_project_name>
$ sudo docker-compose up
```
After running your created project, you can continue coding using any desired IDE. For more comfort you can use the venv folder within your project.
Your project is available at: http://127.0.0.1:8000/

To Turn off a running project:
```sh
$ CTRL + C
```

**Free Software, Hell Yeah!**