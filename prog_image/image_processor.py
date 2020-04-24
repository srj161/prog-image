"""
Module contains a collection of functions that take a `models.Image` document and return
a tuple `(<byte_string>, <file_format>)`.

byte_string: A byte string representation of the image file after conversion has been applied
file_format: An `ImageFileFormats` constant representing the new image format
"""
import io
from PIL import Image

from constants import ImageFileFormats


def convert_to_jpeg(image_doc):
    def _to_jpeg(image):
        image = image.convert('RGB')
        return image, ImageFileFormats.JPEG
    return _convert(image_doc, _to_jpeg)


def convert_to_grayscale(image_doc):
    def _to_grayscale(image):
        image = image.convert('L')
        return image, image_doc.image_format
    return _convert(image_doc, _to_grayscale)


def convert_to_mirror(image_doc):
    def _to_mirror(image):
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        return image, image_doc.image_format
    return _convert(image_doc, _to_mirror)


def convert_to_png(image_doc):
    def _to_png(image):
        return image, ImageFileFormats.PNG
    return _convert(image_doc, _to_png)


def _convert(image_doc, conversion_func):
    """
    Helper function to simplify conversions.
    `conversion_func` must take a `PIL.Image` and return a new `Image` and
    a new `ImageFileFormats` const.
    """
    image = Image.open(image_doc.image)
    image, file_format = conversion_func(image)
    f = io.BytesIO()
    image.save(f, file_format)
    f.seek(0)
    return f.read(), file_format
