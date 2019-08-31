# Execute commands
```bash
/opt/Python37/bin/python3 -m venv ./venv
source venv/bin/activate

pip3 install --upgrade pip setuptools
pip3 install django

django-admin startproject mysite
cd mysite/
python3 manage.py runserver

pip3 install uWSGI

cd /home/harny/Github/Hobby/uWSGI/mysite
uwsgi --http :8080 --home /home/harny/Github/Hobby/uWSGI/venv/ --chdir /home/harny/Github/Hobby/uWSGI/mysite/ --module=mysite.wsgi:application
```
