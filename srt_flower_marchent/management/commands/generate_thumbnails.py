from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os

from srt_flower_marchent.models import Flower


class Command(BaseCommand):
    help = 'Generate thumbnails for existing Flower image files'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Regenerate thumbnails even if present')
        parser.add_argument('--thumb-size', type=int, default=100, help='Thumbnail max side size in pixels')
        parser.add_argument('--max-size', type=int, default=600, help='Main image max side size in pixels')
        parser.add_argument('--quality', type=int, default=75, help='JPEG quality for thumbnails and main image')

    def handle(self, *args, **options):
        qs = Flower.objects.filter(image__isnull=False)
        total = qs.count()
        self.stdout.write(f'Found {total} flowers with images')
        for flower in qs:
            if flower.thumbnail and not options['force']:
                self.stdout.write(f'Skipping {flower.pk} (thumbnail exists)')
                continue
            try:
                img = Image.open(flower.image)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # choose resampling filter compatible with Pillow versions
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.LANCZOS

                thumb_size = (options['thumb_size'], options['thumb_size'])
                thumb_img = img.copy()
                thumb_img.thumbnail(thumb_size, resample=resample)

                buffer = BytesIO()
                thumb_img.save(buffer, format='JPEG', quality=options['quality'])
                base, _ = os.path.splitext(flower.image.name)
                thumb_name = f"{base}_thumb.jpg"
                flower.thumbnail.save(thumb_name, ContentFile(buffer.getvalue()), save=False)

                # Optionally resize main image if larger than max-size
                max_side = options['max_size']
                if img.width > max_side or img.height > max_side:
                    main_img = img.copy()
                    main_img.thumbnail((max_side, max_side), resample=resample)
                    main_buffer = BytesIO()
                    main_img.save(main_buffer, format='JPEG', quality=options['quality'])
                    flower.image.save(flower.image.name, ContentFile(main_buffer.getvalue()), save=False)

                flower.save(update_fields=['thumbnail', 'image'])
                self.stdout.write(f'Generated thumbnail for Flower id={flower.pk}')
            except Exception as exc:
                self.stderr.write(f'Failed for Flower id={flower.pk}: {exc}')
