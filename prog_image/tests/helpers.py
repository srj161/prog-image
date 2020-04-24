import os
from ..models import Image
from ..constants import ImageFileFormats

PROG_IMAGE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_image_doc():
    image = Image(
        name='test_image.png', image_format=ImageFileFormats.PNG)
    with open(f'{PROG_IMAGE_DIR}/test_data/test_image.png', 'rb') as f:
        image.image.put(f)

    image.save()
    return image


def assert_image_equals(image_bytes, test_image_name):
    with open(f'{PROG_IMAGE_DIR}/test_data/{test_image_name}', 'rb') as f:
        assert image_bytes == f.read()
