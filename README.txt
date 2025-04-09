

Situation:	                                     Do you need a new venv? 
🚀 Creating a new Django project	            ✅ Yes — create a fresh venv
📥 Cloning an existing project	                ✅ Yes — create it only once
🧠 Reopening terminal for existing project	    ❌ No — just activate existing venv

- Creating new environment: ------- python -m venv venv



Activate venv (Windows):            	venv\Scripts\activate  (always when you open new terminal)



crete the main core app: ------- python manage.py startapp core
    - register the new core app in the installed apps in settings.py
    - add a new file in the core/urls.py (and then create first view in core/views.py) - tehn register new url you created in core/urls.py in the main myapp/urls.py



run server:  -------  python manage.py runserver

create the default tables in your database (SQLite by default): ------- python manage.py migrate
 