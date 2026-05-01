import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def save_uploaded_file(uploaded_file):
    fs = FileSystemStorage()
    ext = uploaded_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    saved_name = fs.save(filename, uploaded_file)
    return fs.path(saved_name), fs.url(saved_name)

def get_output_path(filename, suffix=""):
    name, ext = os.path.splitext(os.path.basename(filename))
    out_name = f"{name}_{suffix}{ext}"
    out_path = os.path.join(settings.MEDIA_ROOT, out_name)
    out_url = f"{settings.MEDIA_URL}{out_name}"
    return out_path, out_url
