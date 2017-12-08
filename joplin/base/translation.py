from modeltranslation.translator import translator, TranslationOptions

from .models import ServicePage


class ServicePageTranslationOptions(TranslationOptions):
    fields = (
        # TODO: This field comes from Page and django-modeltranslation complains about it
        # 'title',
        'content',
    )


translator.register(ServicePage, ServicePageTranslationOptions)
