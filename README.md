# No-HEADACHE-DJANGO

> NO-HEADACHE-DJANGO helps you developing your
> django application in the same environment as
> your production server!

*Supporting all versions of django and python.*

NO-HEADACHE-DJANGO is an automatic project dockerization tool for both newly created projects and old projects.

Start your project with NO-DJANGO-HEADACHE and enjoy:
  - automatic Dockerfile creation
  - automatic docker-compose.yaml creation
  - automatic deploy function and docker swarm deploy.yaml file which helps you deploy your newly created application using nginx, gunicorn and docker swarm.

# Features:

  - NO-HEADACHE-DJANGO automatically detects your project structure and build appropriate docker-compose.yaml and deploy.yaml(swarm) file.
  - NO-HEADACHE-DJANGO supports almost all of the popular databases including postgres and mysql.


It Also does:
  - Automatically creation of README.me, git, .gitignore and requirements.txt files if needed. 
  - Tools for easily managing your application during development.


> NO-HEADACHE-DJANGO is created for developers 
> who want their project working under on any machine
> without any problems but don't want to learn stuff 
> like Docker or deployment processes.
> This will help them deploy almost any django project 
> in seconds. easy and reliable.


### Tech

NO-HEADACHE-DJANGO is specially designed for ubuntu systems and needs python >= 3 to run, but remember you need to install your desired versin of python if you are willing to create a project using that version.


### Installation

You need to install docker, docker-compose, python3 and virtualenv in order to use NO-HEADACHE-DJANGO.

Install the dependencies:

```sh
$ apt update
$ apt install python3
$ apt install docker docker.io
$ apt install docker-compose
$ apt install virtualenv
```

### Using NO-HEADACHE-DJANGO:
NO-HEADACHE-DJANGO works perfectly with projects that follow the standard project structure of django or projects that are created using NO-HEADACHE-DJANGO, although it supports dockerizing other projects but this is not reliable and may not work as expected.

*So the best way to have a fully dockerized django is using NO-HEADACHE-DJANGO while starting the project*

starting a project:
```sh
$ no-headache startproject <project_name> <project_root> <database> <python_versioin>
```
exp:
```sh
$ no-headache startproject amazing_project . postgres 3.6
```
This will a create a project named 'amazing_project' in your current directory using postgres database and python3.6

Dockerizing a project:
```sh
$ no-headache dockerize <project_root> <database> <python_version>
```
exp:
```sh
$ no-headache dockerize ./an_old_project mysql 2.7
```
This will dockerize an existing project in a folder named an_old_project in your current directory which is written in python2.7 using mysql.

