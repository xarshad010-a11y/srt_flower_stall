PythonAnywhere deployment steps
--------------------------------

1. Push your project to GitHub
   - Initialize a repo, commit, and push your code to GitHub.

2. Sign in to PythonAnywhere and create a new Web app
   - Choose "Manual configuration" and select the correct Python version (3.11/3.10/3.9 depending on your runtime).

3. Set up a virtualenv and install requirements
   - In the Bash console on PythonAnywhere:

     python -m venv ~/venv
     source ~/venv/bin/activate
     pip install --upgrade pip
     pip install -r /home/yourusername/yourrepo/requirements.txt

4. Configure the Web app WSGI file
   - Edit the WSGI configuration on the Web tab to point to your project. Example WSGI snippet:

     import os
     import sys
     path = '/home/yourusername/yourrepo'
     if path not in sys.path:
         sys.path.insert(0, path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'srt_flower_stall.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()

5. Environment variables
   - In the Web -> Environment variables section, set:
     - `DJANGO_SECRET_KEY` (a long secret string)
     - `DJANGO_DEBUG` = `False`
     - `DJANGO_ALLOWED_HOSTS` = yourdomain.pythonanywhere.com

6. Static files
   - On PythonAnywhere Web tab, under "Static files", add a mapping:
     - URL `/static/` -> `/home/yourusername/yourrepo/staticfiles/`
   - Run `python manage.py collectstatic` on PythonAnywhere to populate `staticfiles/`.

7. Database & migrations
   - Run `python manage.py migrate` on PythonAnywhere.

8. Reload the web app from the PythonAnywhere web UI.

Security notes
 - Do not commit your `DJANGO_SECRET_KEY` to the repo.
 - Use environment variables for all secrets and `DEBUG=False` in production.
