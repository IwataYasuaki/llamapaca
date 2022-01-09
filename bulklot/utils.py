from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from time import sleep
from django_rq import job

@job
def login_to_tmgbc(sport, location_page, location_id, date, time):
    url = "https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html"
    options = Options()
    options.add_argument('--headless')
    wd = webdriver.Chrome(options=options)
    wd.get(url)
    wd.find_element_by_id('login').click()
    sleep(4)
    wd.find_element_by_id('userid').send_keys('86772511')
    wd.find_element_by_id('passwd').send_keys('19890101')
    wd.find_element_by_id('login').click()
    sleep(0.5)
    wd.find_element_by_id('goLotSerach').click()
    sleep(0.5)
    wd.find_element_by_css_selector('input[value="' + sport + '"]').click()
    wd.find_element_by_id('doSearch').click()
    sleep(0.5)
    while not wd.find_element_by_id('offset').get_attribute('value') == location_page:
        wd.find_element_by_id('goNextPager').click()
        sleep(0.5)
    wd.find_element_by_name('layoutChildBody:childForm:igcdListItems:' + location_id + ':doAreaSet').click()
    sleep(0.5)
    wd.find_element_by_css_selector('a.calclick[onclick="javascript:selectCalendarDate(' + date + ');return false;"]').click()
    sleep(0.5)
    wd.find_element_by_css_selector('input[value="' + time + '"]').click()
    wd.find_element_by_id('doDateTimeSet').click()
    sleep(0.5)
    wd.find_element_by_id('doOnceFix').click()
    wait = WebDriverWait(wd, 10)
    wait.until(expected_conditions.alert_is_present())
    Alert(wd).accept()
    sleep(0.5)
    wd.quit()

