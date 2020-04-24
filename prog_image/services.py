import io
from werkzeug.wrappers import Response
from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from nameko_mongoengine import MongoEngine

import utils
import image_processor
from models import Image


class HttpAPIService:
    """
    Service contains the entry point for the external facing http api.
    Designed to be lightweight and do minimal processing, shipping the heavy lifting
    off to each of the other services.
    """
    name = "http_api_service"

    image_upload_service = RpcProxy('image_upload_service')
    image_convert_jpeg_service = RpcProxy('image_convert_jpeg_service')
    image_convert_png_service = RpcProxy('image_convert_png_service')
    image_convert_grayscale_service = RpcProxy('image_convert_grayscale_service')
    image_convert_mirror_service = RpcProxy('image_convert_mirror_service')

    @http('POST', '/upload_file')
    def upload_file(self, request):
        """
        Upload file handle takes 'image' from the request body and saves the image.
        Returns:
            image_id(str): to be used in subsequent API requests.
        """
        image = request.files.get('image')

        if not image:
            raise Exception('image not provided in request')

        return self.image_upload_service.upload_image(
            image.read(),
            image.filename
        )

    @http('GET', '/<string:image_id>/jpeg')
    def image_as_jpeg(self, request, image_id):
        """
        Returns image in JPEG format
        """
        return self._image_conversion_call(
            self.image_convert_jpeg_service, image_id)

    @http('GET', '/<string:image_id>/png')
    def image_as_png(self, request, image_id):
        """
        Returns image in PNG format
        """
        return self._image_conversion_call(
            self.image_convert_png_service, image_id)

    @http('GET', '/<string:image_id>/grayscale')
    def image_as_grayscale(self, request, image_id):
        """
        Returns image converted to grayscale
        """
        return self._image_conversion_call(
            self.image_convert_grayscale_service, image_id)

    @http('GET', '/<string:image_id>/mirror')
    def image_as_mirror(self, request, image_id):
        """
        Returns image fliped horizontally
        """
        return self._image_conversion_call(
            self.image_convert_mirror_service, image_id)

    def _image_conversion_call(self, rpc_proxy_service, image_id):
        """
        Helper function to simplify image conversion calls.
        Calls `rpc_proxy_service.convert_image(image_id)` and returns an image formatted
        HTTP response.
        """
        image_b_str, image_format = rpc_proxy_service.convert_image(image_id)
        f = io.BytesIO(image_b_str)
        return Response(
            f,
            mimetype=utils.get_image_content_type_from_format(image_format),
            direct_passthrough=True
        )


class ImageUploadService:
    name = "image_upload_service"
    engine = MongoEngine()

    @rpc
    def upload_image(self, image_b_str, image_name):
        """
        Creates a new `Image` document in mongo with `image_b_str` and `image_name`.
        Returns the `image_id`
        """
        f = io.BytesIO(image_b_str)

        image_format = utils.get_image_file_format_from_name(image_name)
        image_content_type = utils.get_image_content_type_from_format(image_format)

        image = Image(name=image_name, image_format=image_format)
        image.image.put(f, content_type=image_content_type)
        image.save()
        return str(image.id)


class ImageConvertJpegService:
    name = "image_convert_jpeg_service"
    engine = MongoEngine()

    @rpc
    def convert_image(self, image_id):
        image_doc = Image.objects.get(id=image_id)
        return image_processor.convert_to_jpeg(image_doc)


class ImageConvertGrayScaleService:
    name = "image_convert_grayscale_service"
    engine = MongoEngine()

    @rpc
    def convert_image(self, image_id):
        image_doc = Image.objects.get(id=image_id)
        return image_processor.convert_to_grayscale(image_doc)


class ImageConvertMirrorService:
    name = "image_convert_mirror_service"
    engine = MongoEngine()

    @rpc
    def convert_image(self, image_id):
        image_doc = Image.objects.get(id=image_id)
        return image_processor.convert_to_mirror(image_doc)


class ImageConvertPNGService:
    name = "image_convert_png_service"
    engine = MongoEngine()

    @rpc
    def convert_image(self, image_id):
        image_doc = Image.objects.get(id=image_id)
        return image_processor.convert_to_png(image_doc)
