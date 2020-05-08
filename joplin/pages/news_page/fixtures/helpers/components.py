'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage


def home():
    return HomePage.objects.first()

mvp_news_title = 'Health Authorities Continue to Stress the Importance of Stay at Home & Social Distancing Guidelines'

mvp_news_body = '<p>Austin, TX — An individual in their 20s is in critical condition at a local hospital. Austin-Travis County Interim Health Authority, Dr. Mark Escott, continues to urge the public to stay home except for essential activities to reduce the risk of spreading COVID-19.</p><p></p><p>“The health of the public is in the hands of the community,” said Dr. Escott. “It is important to understand that young people are not immune from serious illness. We implore the community to stay at home even if you are not feeling ill, and before leaving your house ask yourself ‘Is this trip necessary?’ It is the entire community’s responsibility to stop the spread, including our young adults and teens.”</p><p></p><p>People with mild symptoms may significantly contribute to further viral spread to others–including other patients and medical staff.</p><p></p><p>“Those who only present mild symptoms may be a significant contribution to spread and therefore, everyone should stay home unless absolutely necessary,” added Dr. Escott.</p><p></p><p>If you are exhibiting COVID-19 symptoms such as fever, dry cough and shortness of breath, call your health care provider or use <a href=\"http://fake.base.url/telehealth-resources/\">telehealth resources</a> before visiting a hospital or urgent care clinic. Individuals who are uninsured or without an established provider can call the CommUnity Care COVID-19 Hotline at <a href=\"tel:512-978-8775\">512-978-8775</a> for guidance.</p><p></p><p>A healthcare provider will determine if there is another plausible diagnosis with similar symptoms (i.e. influenza). For suspected COVID-19 cases, your doctor will fill out a form. Austin Public Health (APH) will use this information to assess risk and criteria to determine whether a test is appropriate.</p><p></p><p>APH continues to stress the importance of practicing good personal hygiene and maintaining social distance during essential activities to disrupt the spread of the virus.</p><p></p><p>Proper hygiene practices include:</p><ul><li>Wash your hands often with soap and water for at least 20 seconds. If soap and water are unavailable, use an alcohol-based hand sanitizer.</li><li>Avoid touching your eyes, nose, and mouth with unwashed hands.</li><li>Avoid close contact with people who are sick.</li><li>Stay home when you are sick.</li><li>Cough or sneeze into your elbow or use a tissue to cover it, then throw the tissue in the trash.</li><li>Clean and disinfect frequently touched objects and surfaces.</li></ul><p>For more information and updates, visit <a href=\"http://www.AustinTexas.gov/COVID19\">www.AustinTexas.gov/COVID19</a>.</p>'


