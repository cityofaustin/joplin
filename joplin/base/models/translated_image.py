from django.db import models

from wagtail.images.models import AbstractImage, Image, AbstractRendition

# one reason why this may be abstract: wagtail-modeltranslation will patch
# wagtail images directly to add translated fields which seems messy


class TranslatedImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    def __str__(self):
        return self.title or self.title_en


class TranslatedImageRendition(AbstractRendition):
    image = models.ForeignKey(TranslatedImage, related_name='renditions', on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
