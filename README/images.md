### Uploading Images
Uploading an image through the Joplin CMS in staging or production will upload that image to the CMS_MEDIA s3 images bucket. And it also add entries for that image to the `base_translatedimage` and `base_translatedimagerendition` database tables. `base_translatedimage` is the primary image information table, and `base_translatedimagerendition` is a child table that contains all the different image sizes that are available on s3.

For example:
```
base_translatedimage:
id |      title       |               file
----+------------------+----------------------------------
21 | love-chicken.jpg | original_images/love-chicken.jpg

base_translatedimagerendition:
id  |                file
-----+-------------------------------------
183 | images/love-chicken.width-640.jpg
184 | images/love-chicken.width-720.jpg
185 | images/love-chicken.width-750.jpg
186 | images/love-chicken.width-828.jpg
187 | images/love-chicken.width-1080.jpg
188 | images/love-chicken.width-1440.jpg
189 | images/love-chicken.width-2160.jpg
190 | images/love-chicken.max-165x165.jpg
```

When displaying images on Janis, you would need to use one of the filepaths that is stored in the `base_translatedimagerendition` table.

#### TODO / Need to Know:
- graphql does not recognize a foreign relation between `base_translatedimage` and `base_translatedimagerendition`. Where is our graphql schema set up? We'll need to change that, otherwise I'll have the manually parse `base_translatedimage.title` and guess at the base_translatedimagerendition to use.
- Why was `filename` added to graphql schema for images (joplin/api/schema.py)? How is it different than `title`? Where does it come from?
- Our `TranslatedImageRendition` class in `models.py` does not behave consistently. For example, some images have the renditions "x.original.jpg" and "x.max-800x600.jpg" generated, but "love-chicken" does not. This could be an issue if your Janis page expects to use a particular size/rendition that does not exist for your image.
- Bug: You can't delete images. I accidentally uploaded Farah-2.jpg twice and couldn't delete one of them without Django throwing an error message about foreign key dependencies. Luqmaan intentionally set this dependen
- Images saved in staging and production are saved in the same S3 Bucket destination. However, there are not entires generated in `base_translatedimage` table for both staging and production. For instance, if I upload an image in staging, I can't access that image in prod even though it's in the same S3 Bucket. So to see an image in both staging and prod, you'd have to upload that image twice. There could be other issues that result from this prod/staging storage contamination.
- There is no way to set the alt-text for an image in Joplin CMS? (Setting the fields title_en, title_es, title_vi, title_ar).
- Once the alt-text for each language can be set, we need to change Janis's 1 `static.config.js` to pull those fields dynamically based on what language is selected.
- There need to be headshot-sized image renditions. Maybe the CMS image uploader needs to differentiate between banner-images and headshot-images.
