from . import helpers
from .. import image_processor
from ..constants import ImageFileFormats


def test_to_jpeg(mongo):
    image_doc = helpers.create_image_doc()
    image, image_format = image_processor.convert_to_jpeg(image_doc)
    assert image_format == ImageFileFormats.JPEG
    helpers.assert_image_equals(image, 'test_jpeg_image.jpeg')


def test_to_grayscale(mongo):
    image_doc = helpers.create_image_doc()
    image, image_format = image_processor.convert_to_grayscale(image_doc)
    assert image_format == ImageFileFormats.PNG
    helpers.assert_image_equals(image, 'test_grayscale_image.png')


def test_to_mirror(mongo):
    image_doc = helpers.create_image_doc()
    image, image_format = image_processor.convert_to_mirror(image_doc)
    assert image_format == ImageFileFormats.PNG
    helpers.assert_image_equals(image, 'test_mirror_image.png')


def test_to_png(mongo):
    image_doc = helpers.create_image_doc()
    image, image_format = image_processor.convert_to_png(image_doc)
    assert image_format == ImageFileFormats.PNG
    helpers.assert_image_equals(image, 'test_png_image.png')
