from mongoengine import Document, fields


class Image(Document):
    name = fields.StringField(required=True)
    image_format = fields.StringField(required=True)
    image = fields.FileField(required=True)
