# install Django
    pip install django

# install google-genai
    pip install google-generativeai

# Others 
    pip install django-widget-tweaks
    pip install django-crispy-forms
    pip install crispy-tailwind



# create virtual environment 
    python -m venv venv
    .\venv\Scripts\activate

# Other cmds 
    django-admin startproject virtual_library
    cd virtual_library
    python manage.py startapp library


    python manage.py makemigrations
    python manage.py migrate


# To run the system 
    python manage.py runserver

# Access the admin interface at 
    http://127.0.0.1:8000/admin/ 
## to upload books. 

# Public users can access the library at 
    http://127.0.0.1:8000/


# i have create admin users by 

    (venv) PS D:\Python Project\Library_manage\virtual_library> python manage.py createsuperuser
    Username (leave blank to use 'lenovo'): admin
    Email address: ppmmpm11@gmail.com
    Password: admin@123
    Password (again): admin@123
    The password is too similar to the username.
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.

