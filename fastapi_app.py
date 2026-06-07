import os

# Ensure Django settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srt_flower_stall.settings')

from fastapi import FastAPI
from django.core.asgi import get_asgi_application

# Create Django ASGI application
django_asgi_app = get_asgi_application()

app = FastAPI(title='FastAPI + Django')

# Mount the Django app at the root path so the existing Django pages are served
app.mount("/", django_asgi_app)

@app.get('/_health')
async def health():
    return {"status": "ok"}
