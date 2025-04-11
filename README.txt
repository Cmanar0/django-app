# 🐍 DJANGO PROJECT SETUP GUIDE



----------------------------------------   ENVIRONMENT ----------------------------------------

### When do you need a virtual environment?

| Situation                                   | New venv required?           |
|---------------------------------------------|------------------------------|
| 🚀 Creating a new Django project            | ✅ Yes – create a fresh venv |
| 📥 Cloning an existing project              | ✅ Yes – create once         |
| 🧠 Reopening terminal for existing project  | ❌ No – just activate it     |

### Commands

python3 -m venv venv  
source venv/bin/activate  (Mac/Linux)  
venv\Scripts\activate     (Windows)  



----------------------------------------   DEPENDENCIES ----------------------------------------

pip install --upgrade pip  
pip install -r requirements.txt  

Anytime you install or remove a Python package:

pip install somepackage  
pip freeze > requirements.txt  
git add requirements.txt  

----------------------------------------   DATABASE ----------------------------------------

python manage.py makemigrations  
python manage.py migrate  

----------------------------------------   CREATING A CORE APP ----------------------------------------

python manage.py startapp core  

An app is a modular part of a Django project that handles a specific set of responsibilities or features.

Then:

- Register the new `core` app in `INSTALLED_APPS` in settings.py  
- Add a new file `core/urls.py`  
- Create the first view in `core/views.py`  
- Register the new URL you created in `core/urls.py` inside the main `myapp/urls.py`  

This setup allows the app to respond to HTTP requests using the logic defined in views, and the project knows how to route those requests using the URL config.

You can also create a templates folder and static folder inside the core app to handle rendering HTML pages and including assets like CSS or JS.

----------------------------------------   LOCAL SERVER ----------------------------------------

python manage.py runserver  
python manage.py collectstatic  
python manage.py createsuperuser  

----------------------------------------   DEPLOYMENT (LINODE VPS + DOCKER) ----------------------------------------

cd /docker/testing-Django-Docker/  
git pull  
docker compose down  
docker compose up -d --build  
