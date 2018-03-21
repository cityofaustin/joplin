import os
import textwrap
from pathlib import Path

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page
from yaml import load

from base.models import TranslatedImage, Topic, Department, ServicePage


def load_images(data):
    for image_data in data['images']:
        yield load_image(image_data)


def load_image(data):
    data = {k.replace('alt_text', 'title') if k.startswith('alt_text') else k: v for k, v in data.items()}
    data['title'] = data['title_en']

    filename = data.pop('filename')
    filepath = Path(filename)
    with open(filename, 'rb') as f:
        data['file'] = ImageFile(f, name=filepath.name)
        image_regex = f'original_images/{filepath.stem}'
        image, created = TranslatedImage.objects.update_or_create(file__startswith=image_regex, defaults=data)

    print(f'{"✅  Created" if created else "⭐  Updated"} {filepath.name} => {image.file.name}')

    return image


def load_topics(data):
    for topic_data in data['topics']:
        yield load_topic(topic_data)


def load_topic(data):
    topic, created = Topic.objects.update_or_create(slug=data['slug'], defaults=data)

    print(f'{"✅  Created" if created else "⭐  Updated"} {topic.slug}')

    return topic


def load_departments(data):
    for department_data in data['departments']:
        yield load_department(department_data)


def load_department(data):
    contact = data.pop('contact')

    image_name = data.pop('image')
    if image_name:
        image_regex = f'original_images/{image_name}'
        data['image'] = TranslatedImage.objects.get(file__startswith=image_regex)

    department, created = Department.objects.update_or_create(slug=data['slug'], defaults=data)

    print(f'{"✅  Created" if created else "⭐  Updated"} {department.slug}')

    return department


def ulify(listy):
    step_list_items = []
    for item in listy:
        if isinstance(item, list):
            step_list_items.append(f'<li>{ulify(item)}</li>')
        else:
            step_list_items.append(f'<li><p>{item}</p></li>')

    result = textwrap.dedent(f'''
        <ul>
            {''.join(step_list_items)}
        </ul>
    ''').strip()

    return result


def load_service(data):
    print(f'-  Cleaning up data...\r', end='')
    slug = data['slug']
    for k in ['meta_description_ar', 'meta_description_en', 'meta_description_es', 'meta_description_vi', 'meta_tags', 'meta_title_ar', 'meta_title_en', 'meta_title_es', 'meta_title_vi']:
        data.pop(k, None)

    for key in data:
        if key.startswith('steps_'):
            data[key] = ulify(data[key])
    data['steps'] = data['steps_en']
    data['additional_content'] = data['additional_content_en']
    print('✅')

    print(f'-  Loading homepage...\r', end='')
    home = Page.objects.get(slug='home')
    print('✅')

    print(f'-  Loading topic page...\r', end='')
    topic_slug = data.pop('topic')
    data['topic'] = Topic.objects.get(slug=topic_slug)
    print('✅')

    print(f'-  Loading image...\r', end='')
    image_name = data.pop('image')
    image_regex = f'original_images/{image_name}'
    data['image'] = TranslatedImage.objects.get(file__startswith=image_regex)
    print('✅')

    print(f'-  Loading child page "{slug}"...\r', end='')
    created = False
    try:
        page = ServicePage.objects.get(slug=slug)
        for k, v in data.items():
            setattr(page, k, v)
    except Exception as e:
        page = ServicePage(**data)
        home.add_child(instance=page)
        created = True

    page.save_revision().publish()
    print(f'{"✅  Created" if created else "⭐  Updated"}')

    yield page


class Command(BaseCommand):
    help = 'Loads initial content'
    LINE_LENGTH = 100

    def add_arguments(self, parser):
        parser.add_argument('fixtures', nargs='+', type=str)

    def handle(self, *args, **options):
        loaders = {
            'images': load_images,
            'topics': load_topics,
            'services': load_service,
            'departments': load_departments,
        }
        for filename in options['fixtures']:
            paths = []
            p = Path(filename)
            if p.is_dir():
                paths = list(p.iterdir())
                loader_type = p.parts[-1]
            else:
                paths = [p]
                loader_type = p.stem if p.parts[-2] == 'fixtures' else p.parts[-2]

            for p in paths:
                title = f'Loading {loader_type} from {p.name}'
                spaces = self.LINE_LENGTH - len(title) - 1
                print(f'{title} {"=" * spaces}')

                with p.open() as f:
                    data = load(f)

                loader = loaders[loader_type]
                list(loader(data))

                print(f'{"=" * self.LINE_LENGTH}\n')

        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
