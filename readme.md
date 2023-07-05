# Elearning
Elearning is a Django app that connects students and teachers together, it's flexible enough to be used in a school/university or as a standalone course site

## Requirements
1. Landing page
2. About us page
3. User dashboard
4. User authentication
    1. Teacher users
    2. Student users
    3. Admins
5. Students can:
    1. View courses they're assigned to
    2. View course contents
6. Teachers can:
    1. Add course materials
    2. Assign students to courses
7. Admins can:
    1. Invite teachers to platform
    2. Create new courses
    3. Assign teachers to course
    4. View course assignments
    5. Assign and unassign students from courses

## Development Environment
To get elearning up and running you need python `3.10` or higher, and django `4.2`

### Windows
Download python from https://www.python.org/downloads/

Or from windows store https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5

In powershell or cmd 
```shell
cd path\to\project
pip install # or pipenv install if you have it
```

### MacOS
Open the terminal and hit the following commands
```shell
brew install python@3.10 # or just python for latest
cd path/to/project
pip install # or pipenv install if you have it
```

### Ubuntu
Open the terminal and hit the following commands
```shell
sudo apt install python3.10 # or just python for latest
cd path/to/project
pip install # or pipenv install if you have it
```

### Starting the app
```shell
python manage.py runserver
```

and navigate to http://127.0.0.1:8000

### Migrations and Admin
Create an admin user using
```shell
python manage.py migrate
python manage.py seed_user_groups_and_permissions
python manage.py createsuperuser
```

And follow the instructions

After creation, navigate to http://127.0.0.1:8000/admin to create teachers and students

Then you can login using http://127.0.0.1/dashboard and create courses and assign students and teachers to them

### Credits
1. [Boostrap Modern Business Theme](https://github.com/StartBootstrap/startbootstrap-modern-business/tree/master)
2. [Boostrap 5](https://getbootstrap.com/)
3. [Django](https://www.djangoproject.com/)