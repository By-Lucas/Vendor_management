from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    'Em caso de erro, deixar somente o value em vez de value.name'
    ext = os.path.splitext(value.name)## cover-image.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de arquivo não suportado. extensões permitidas: ' +str(valid_extensions))


def allow_only_arquives_validator(value):
    'Em caso de erro, deixar somente o value em vez de value.name'
    ext = os.path.splitext(value.name)[1] # arquive.pdf
    print(ext)
    valid_extensions = ['.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de arquivo não suportado. extensões permitidas: ' +str(valid_extensions))