import os
from pages.news_page.fixtures.helpers.create_fixture import create_fixture
import pages.news_page.fixtures.helpers.components as components
import snippets.contact.fixtures.helpers.components as contact_components
from groups.fixtures.test_cases.mvp_news_aph import mvp_news_aph





def fifty_written_by_APH():
    departments = [mvp_news_aph()]
    news_titles = []

    # let's have some fun with this test data 🤠
    for i in ['', ' 🦦', ' 🦥', ' 🦩', ' 🦒']:
        news_titles.extend([
            {'en': f'Health Authorities Continue to Stress the Importance of Stay at Home & Social Distancing Guidelines{i}', 'es': f'{i}'},
            {'en': f'COVID-19 Information Hotline for Restaurants Launched for Austin-Travis County{i}', 'es': f'{i}'},
            {'en': f'Austin-Travis County COVID-19 Child Care Task Force activated to support local community{i}', 'es': f'{i}'},
            {'en': f'Warn Central Texas Notification System Reminds Everyone to Stay Home, Stay Safe this Holiday Weekend{i}', 'es': f'{i}'},
            {'en': f'City Council approves Relief in a State of Emergency Fund to provide immediate and direct relief for vulnerable Austinites{i}', 'es': f'{i}'},
            {'en': f'Surge Plan Developed to Treat COVID-19 Patients if Hospitals are Overwhelmed{i}', 'es': f'{i}'},
            {'en': f'Places of Worship in Austin-Travis County Observe Local Stay-at-Home Plea{i}', 'es': f'{i}'},
            {'en': f'City of Austin Parks Will Close Easter Weekend{i}', 'es': f'{i}'},
            {'en': f'Austin-Travis County Adopts CDC Guidelines Regarding Public Use Fabric Face Coverings {i}', 'es': f'{i}'},
            {'en': f'Austin-Travis County Creates a Social Service Branch for Emergency Response Efforts{i}', 'es': f'{i}'},    
        ])

    for counter, title in enumerate(news_titles):
        page_data = {
            "imported_revision_id": None,
            "live": True,
            "parent": components.home(),
            "coa_global": False,
            "title": title['en'],
            "title_es": title['es'],
            "slug": f'mvp-news-by-aph-{counter}',
            "body": components.mvp_news_body,
            "body_es": components.google_translated_mvp_news_body,
            "contact": contact_components.mvp_news_contact(),
            "add_departments": {
                "departments": departments
            },
        }

        yield create_fixture(page_data, os.path.basename(__file__))
