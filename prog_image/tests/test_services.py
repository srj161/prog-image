import pytest
from nameko.testing.services import worker_factory
from nameko.constants import SERIALIZER_CONFIG_KEY
from . import helpers
from ..constants import ImageFileFormats
from ..models import Image
from .. import services


class TestHttpAPIService:
    def test_upload_image(self, mongo, runner_factory, rabbit_config,
                          web_config, web_session):
        runner_factory(
            {**rabbit_config, **web_config, SERIALIZER_CONFIG_KEY: 'pickle'},
            services.HttpAPIService,
            services.ImageUploadService
        ).start()

        with open(f'{helpers.PROG_IMAGE_DIR}/test_data/test_image.png', 'rb') as f:
            image = f.read()
        rv = web_session.post('/upload_file', files={'image': ('test_image.png', image)})

        assert rv.status_code == 200
        Image.objects.get(id=str(rv.content, 'utf-8'))

    def test_upload_image_fails_if_image_missing(
            self, mongo, runner_factory, rabbit_config, web_config, web_session):
        runner_factory(
            {**rabbit_config, **web_config, SERIALIZER_CONFIG_KEY: 'pickle'},
            services.HttpAPIService,
            services.ImageUploadService
        ).start()

        rv = web_session.post('/upload_file')

        assert rv.status_code == 500
        assert str(rv.content, 'utf-8') == 'Error: Exception: image not provided in request\n'

    def test_image_as_jpeg_returns_image_correctly(
            self, mongo, runner_factory, rabbit_config, web_config, web_session):
        image_doc = helpers.create_image_doc()
        runner_factory(
            {**rabbit_config, **web_config, SERIALIZER_CONFIG_KEY: 'pickle'},
            services.HttpAPIService,
            services.ImageConvertJpegService
        ).start()

        rv = web_session.get(f'/{str(image_doc.id)}/jpeg')

        assert rv.status_code == 200
        helpers.assert_image_equals(rv.content, 'test_jpeg_image.jpeg')

    def test_image_as_grayscale_returns_image_correctly(
            self, mongo, runner_factory, rabbit_config, web_config, web_session):
        image_doc = helpers.create_image_doc()
        runner_factory(
            {**rabbit_config, **web_config, SERIALIZER_CONFIG_KEY: 'pickle'},
            services.HttpAPIService,
            services.ImageConvertGrayScaleService
        ).start()

        rv = web_session.get(f'/{str(image_doc.id)}/grayscale')

        assert rv.status_code == 200
        helpers.assert_image_equals(rv.content, 'test_grayscale_image.png')

    def test_image_as_mirror_returns_image_correctly(
            self, mongo, runner_factory, rabbit_config, web_config, web_session):
        image_doc = helpers.create_image_doc()
        runner_factory(
            {**rabbit_config, **web_config, SERIALIZER_CONFIG_KEY: 'pickle'},
            services.HttpAPIService,
            services.ImageConvertMirrorService
        ).start()

        rv = web_session.get(f'/{str(image_doc.id)}/mirror')

        assert rv.status_code == 200
        helpers.assert_image_equals(rv.content, 'test_mirror_image.png')


class TestImageUploadService:
    def test_saves_image_and_returns_id(self, mongo):
        with open(f'{helpers.PROG_IMAGE_DIR}/test_data/test_image.png', 'rb') as f:
            image_b_str = f.read()

        service = worker_factory(services.ImageUploadService)
        image_id = service.upload_image(image_b_str, 'test_image.png')

        image = Image.objects.get(id=image_id)
        assert image.name == 'test_image.png'
        assert image.image_format == ImageFileFormats.PNG
        helpers.assert_image_equals(image_b_str, 'test_image.png')

    def test_saves_jpg_image_with_the_correct_format(self, mongo):
        with open(f'{helpers.PROG_IMAGE_DIR}/test_data/test_image.png', 'rb') as f:
            image_b_str = f.read()

        service = worker_factory(services.ImageUploadService)
        image_id = service.upload_image(image_b_str, 'test_image.jpeg')

        image = Image.objects.get(id=image_id)
        assert image.name == 'test_image.jpeg'
        assert image.image_format == ImageFileFormats.JPEG


class TestConvertJpegService:
    def tests_returns_jpeg_image(self, mongo):
        image_doc = helpers.create_image_doc()

        service = worker_factory(services.ImageConvertJpegService)
        image, image_format = service.convert_image(str(image_doc.id))

        assert image_format == ImageFileFormats.JPEG
        helpers.assert_image_equals(image, 'test_jpeg_image.jpeg')

    def test_raises_if_image_id_is_unknown(self, mongo):
        service = worker_factory(services.ImageConvertJpegService)
        with pytest.raises(Exception) as execinfo:
            service.convert_image('5cef9e7a74f27f00011c6627')
        assert str(execinfo.value) == 'Image matching query does not exist.'


class TestConvertGrayScaleService:
    def tests_returns_converted_image(self, mongo):
        image_doc = helpers.create_image_doc()

        service = worker_factory(services.ImageConvertGrayScaleService)
        image, image_format = service.convert_image(str(image_doc.id))

        assert image_format == ImageFileFormats.PNG
        helpers.assert_image_equals(image, 'test_grayscale_image.png')

    def test_raises_if_image_id_is_unknown(self, mongo):
        service = worker_factory(services.ImageConvertGrayScaleService)
        with pytest.raises(Exception) as execinfo:
            service.convert_image('5cef9e7a74f27f00011c6627')
        assert str(execinfo.value) == 'Image matching query does not exist.'


class TestConvertMirrorService:
    def tests_returns_converted_image(self, mongo):
        image_doc = helpers.create_image_doc()

        service = worker_factory(services.ImageConvertMirrorService)
        image, image_format = service.convert_image(str(image_doc.id))

        assert image_format == ImageFileFormats.PNG
        helpers.assert_image_equals(image, 'test_mirror_image.png')

    def test_raises_if_image_id_is_unknown(self, mongo):
        service = worker_factory(services.ImageConvertMirrorService)
        with pytest.raises(Exception) as execinfo:
            service.convert_image('5cef9e7a74f27f00011c6627')
        assert str(execinfo.value) == 'Image matching query does not exist.'


class TestConvertPngService:
    def tests_returns_png_image(self, mongo):
        image_doc = helpers.create_image_doc()

        service = worker_factory(services.ImageConvertPNGService)
        image, image_format = service.convert_image(str(image_doc.id))

        assert image_format == ImageFileFormats.PNG
        helpers.assert_image_equals(image, 'test_png_image.png')

    def test_raises_if_image_id_is_unknown(self, mongo):
        service = worker_factory(services.ImageConvertPNGService)
        with pytest.raises(Exception) as execinfo:
            service.convert_image('5cef9e7a74f27f00011c6627')
        assert str(execinfo.value) == 'Image matching query does not exist.'
