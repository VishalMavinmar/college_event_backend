# backend/api/models.py
import os
from django.db import models

# Upload path function
def student_image_path(instance, filename):
    token = instance.token_number if instance.token_number else 'temp'
    return f'students/{token}/{filename}'

# CR model
class CR(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Student model
class Student(models.Model):
    cr = models.ForeignKey(CR, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)  # ✅ Unique WhatsApp number
    student_class = models.CharField(max_length=50)
    image = models.ImageField(upload_to=student_image_path, blank=True, null=True)
    token_number = models.AutoField(primary_key=True)  # Auto token generation ✅

    def save(self, *args, **kwargs):
        new_image = False
        if self.pk is None and self.image:
            new_image = True
            old_image = self.image
            self.image = None  # temporarily remove image

        super().save(*args, **kwargs)  # Save first to generate token_number

        if new_image:
            ext = os.path.splitext(old_image.name)[1]
            new_path = f'students/{self.token_number}/{os.path.basename(old_image.name)}'
            full_path = os.path.join('media', new_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'wb') as f:
                f.write(old_image.read())

            self.image = new_path
            super().save(update_fields=['image'])

    def __str__(self):
        return f"{self.name} - Token: {self.token_number}"
