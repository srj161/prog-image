import pathlib

from constants import ImageFileFormats


def get_image_file_format_from_name(file_name):
    """
    Returns an `ImageFileFormats` constant based on the suffix of this
    `file_name`.
    Raises Exception if the filename suffix is not an accepted format.
    """
    extension = pathlib.Path(file_name).suffix
    if extension in ['.jpg', '.jpeg']:
        return ImageFileFormats.JPEG

    if extension == '.png':
        return ImageFileFormats.PNG

    raise Exception(f'{extension} not an accepted image format')


def get_image_content_type_from_format(image_format):
    """
    Returns the correct content type given an `ImageFileFormats` constant.
    The content type is most commonly used as a MIME format in an http header.
    Raises if `image_format` hasn't been configured in this function.
    """
    if image_format == ImageFileFormats.JPEG:
        return 'image/jpeg'

    if image_format == ImageFileFormats.PNG:
        return 'image/png'

    raise Exception(f'Unknown image format: {image_format}')
