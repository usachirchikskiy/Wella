from . import ma
from .models import Dress, Category, Banner,Partner, CategoryDress, Gallery

class PartnerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Partner
        oredered = True

class GallerySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        oredered = True
        model = Gallery

class BannerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        oredered = True
        model = Banner

class CategorySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        oredered = True
        model = Category


class DressSchema(ma.SQLAlchemyAutoSchema):

    categories = ma.Nested(CategorySchema, many=True)

    class Meta:
        oredered = True
        model = Dress

class CategoryDressSchema(ma.SQLAlchemyAutoSchema):

    dresses = ma.Nested(DressSchema, many=True)

    class Meta:
        oredered = True
        model = Category



    # def make_object(self, data):
    #     print(data)
    #     return Category(**data)
