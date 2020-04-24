import pytest

from .. import utils
from ..constants import ImageFileFormats


class TestGetImageFileFormatFromName:
    def test_jpg_extension_returns_JPEG_type(self):
        file_type = utils.get_image_file_format_from_name('test.jpg')
        assert file_type == ImageFileFormats.JPEG

    def test_jpeg_extension_returns_JPEG_type(self):
        file_type = utils.get_image_file_format_from_name('test.jpeg')
        assert file_type == ImageFileFormats.JPEG

    def test_png_extension_returns_PNG_type(self):
        file_type = utils.get_image_file_format_from_name('test.png')
        assert file_type == ImageFileFormats.PNG

    def test_unknown_extension_raises(self):
        with pytest.raises(Exception) as excinfo:
            utils.get_image_file_format_from_name('test.unknown')
        assert '.unknown not an accepted image format' in str(excinfo.value)

    def test_recognises_path_correctly(self):
        file_type = utils.get_image_file_format_from_name('/home/documents/test.png')
        assert file_type == ImageFileFormats.PNG

    def test_with_multiple_points_in_name(self):
        file_type = utils.get_image_file_format_from_name('test.test.png')
        assert file_type == ImageFileFormats.PNG


class TestGetImageContentTypeFromFormat:
    def test_with_JPEG_format(self):
        content_type = utils.get_image_content_type_from_format(
            ImageFileFormats.JPEG)
        assert content_type == 'image/jpeg'

    def test_with_PNG_format(self):
        content_type = utils.get_image_content_type_from_format(
            ImageFileFormats.PNG)
        assert content_type == 'image/png'

    def test_raises_on_unknown_format(self):
        with pytest.raises(Exception) as excinfo:
            utils.get_image_content_type_from_format('unknown')
        assert 'Unknown image format: unknown' in str(excinfo.value)
