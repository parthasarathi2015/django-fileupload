from __future__ import unicode_literals

from django.db import models
from fileupload.settings import MEDIA_ROOT
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv','.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only allowed: .csv,.xlsx')

def upload_to(instance,filename):
    return f'{MEDIA_ROOT}/doc_{filename}'

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=upload_to,validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)





