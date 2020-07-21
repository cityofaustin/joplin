from os import path
import json
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
        CT = timezone('US/Central')
        def make_date(datetime_instance):
            return datetime(datetime_instance.year, datetime_instance.month, datetime_instance.day, 0, 0, 0, 0, CT)

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
            print("It's not Monday or Wednesday. You don't get to make a report today.")
            return

        published_pages = {}
        # Get all revisions for time interval in descending order
        revisions = PageRevision.objects.filter(created_at__gte=lower_bound, created_at__lt=upper_bound).order_by('-created_at')
        # Find all pages that were published during time interval
        for r in revisions:
            page_id = r.page_id
            page = r.page
            if page.live and not published_pages.get(page_id):
                # Find the last revision when this page was published, right before the queried time interval
                page_revisions = PageRevision.objects.filter(created_at__lt=lower_bound, page_id=page_id).order_by('-created_at')
                published_before = False
                for pr in page_revisions:
                    pr_live = json.loads(pr.content_json)["live"]
                    if pr_live:
                        published_before = True
                        published_pages[page_id] = {
                            "type": "updated",
                            "page": page,
                            "old_revision": pr,
                            "new_revision": page.get_latest_revision(),
                        }
                        break
                # If this is the first time the page was published, then there is no last published revision to compare with
                if not published_before:
                    published_pages[page_id] = {
                        "type": "new",
                        "page": page,
                        "new_revision": page.get_latest_revision(),
                    }

        context = Context({
            'start_date': lower_bound.strftime("%b %d %Y"),
            'end_date': upper_bound.strftime("%b %d %Y"),
            'published_pages': published_pages,
        })

        template_file = open(path.join(path.dirname(__file__), f'{settings.BASE_DIR}/joplin/templates/joplin_UI/reports/pages_to_translate.html'), "r")
        template_to_render = Template(template_file.read())
        rendered_template = template_to_render.render(context)
        print(rendered_template)
