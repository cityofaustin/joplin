from os import path
from pytz import timezone
from datetime import datetime, timedelta
from django.conf import settings
from wagtail.core.models import PageRevision
from wagtail.core.models import Page
from django.template import Context, Template
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


'''
    Creates a report that contains all pages that have to be translated.

    There is a report run on Monday, which contains all page updates from the prior Wednesday through Sunday.
    And there is a report run on Wednesday, which contains all page updates from the prior Monday and Tuesday.
'''
class Command(BaseCommand):
    help = "Sends a report to alert translators about pages requiring translation."

    def handle(self, *args, **options):
        def make_date(datetime_instance):
            return datetime(datetime_instance.year, datetime_instance.month, datetime_instance.day, 0, 0, 0, 0, CT)

        CT = timezone('US/Central')
        now = datetime.now(CT)
        weekday = now.weekday()
        upper_bound = make_date(now)

        # Monday job
        if weekday == 0:
            last_wednesday = now - timedelta(days=5)
            lower_bound = make_date(last_wednesday)
        # Wednesday job
        elif weekday == 2:
            last_monday = now - timedelta(days=2)
            lower_bound = make_date(last_monday)
        else:
            print("You don't get to make a report today, silly goose.")
            # return
            two_days_ago = now - timedelta(days=2)
            lower_bound = make_date(two_days_ago)
            upper_bound = make_date(now + timedelta(days=2))

        pages_to_translate = {}

        # Get revisions for time interval in ascending order
        revisions = PageRevision.objects.filter(created_at__gte=lower_bound, created_at__lt=upper_bound).order_by('created_at')

        for r in revisions:
            page_id = r.page_id
            page = Page.objects.get(id=page_id)
            title = page.title
            if not pages_to_translate.get(page_id):
                # Get the last revision for this page, right before the queried time interval
                prior_revision = PageRevision.objects.filter(created_at__lt=lower_bound, page_id=page_id).order_by('-created_at').first()
                if not prior_revision:
                    # If there isn't a version before the time interval, then it must be a new page
                    pages_to_translate[page_id] = {
                        "type": "new",
                        "title": title,
                    }
                else:
                    old_revision = prior_revision.id
                    new_revision = page.get_latest_revision().id
                    pages_to_translate[page_id] = {
                        "type": "update",
                        "title": title,
                        "old_revision": old_revision,
                        "new_revision": new_revision,
                    }

        authors = "Gaby and Inara"
        start_date = lower_bound.strftime("%b %d %Y")
        end_date = upper_bound.strftime("%b %d %Y")
        new_pages = {page_id:data for page_id,data in pages_to_translate.items() if data["type"] == "new"}
        new_count = len(new_pages)
        updated_pages = {page_id:data for page_id,data in pages_to_translate.items() if data["type"] == "update"}
        updated_count = len(updated_pages)

        context = Context({
            'authors': authors,
            'start_date': start_date,
            'end_date': end_date,
            'new_pages': new_pages,
            'new_count': new_count,
            'updated_pages': updated_pages,
            'updated_count': updated_count,
        })

        template_file = open(path.join(path.dirname(__file__), f'{settings.BASE_DIR}/joplin/templates/joplin_UI/reports/pages_to_translate.html'), "r")
        template_to_render = Template(template_file.read())
        rendered_template = template_to_render.render(context)
        print(rendered_template)
