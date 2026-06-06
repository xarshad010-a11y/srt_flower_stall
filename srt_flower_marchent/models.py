from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import os


class Garland(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='garlands/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def flower_count(self):
        return self.flowers.count()
    flower_count.short_description = 'Flower count'


class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_stock = models.PositiveIntegerField(default=0)
    garland = models.ForeignKey(
        Garland,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flowers',
    )
    image = models.ImageField(upload_to='flowers/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='flowers/thumbs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Defaults (can regenerate later via management command)
        max_size = (600, 600)
        thumb_size = (100, 100)
        main_quality = 75
        thumb_quality = 75

        if self.image and hasattr(self.image, 'file'):
            try:
                img = Image.open(self.image)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.LANCZOS

                # Resize main image if larger than max_size
                if img.width > max_size[0] or img.height > max_size[1]:
                    main_img = img.copy()
                    main_img.thumbnail(max_size, resample=resample)
                    buffer = BytesIO()
                    main_img.save(buffer, format='JPEG', quality=main_quality)
                    file_name = self.image.name
                    self.image.save(file_name, ContentFile(buffer.getvalue()), save=False)

                # Create thumbnail
                thumb_img = img.copy()
                thumb_img.thumbnail(thumb_size, resample=resample)
                thumb_buffer = BytesIO()
                thumb_img.save(thumb_buffer, format='JPEG', quality=thumb_quality)
                base, _ = os.path.splitext(self.image.name)
                thumb_name = f"{base}_thumb.jpg"
                self.thumbnail.save(thumb_name, ContentFile(thumb_buffer.getvalue()), save=False)
            except Exception:
                pass

        super().save(*args, **kwargs)
