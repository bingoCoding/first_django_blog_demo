from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile


class WaterMakeStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        if 'image' in content.content_type:
            # 加水印
            image = self.water_make_with_text(content, 'Django Blog Program', 'red')
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length)

    def convert_image_to_file(self, image, name):
        buffer = BytesIO()
        image.save(buffer, 'png')
        file_size = buffer.tell()
        return InMemoryUploadedFile(buffer, None, name, 'image/png', file_size, None)


    def water_make_with_text(self, content, text, color, fontfamily=None):
        image = Image.open(content).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width - margin)/2
        y = height - text_height - margin
        draw.text((x, y), text, font=font, fill=color)
        return image
