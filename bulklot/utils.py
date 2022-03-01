from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from time import sleep
from django_rq import job

@job
def login_to_tmgbc(lotReqTime, sport, location_page, location_id, date, time):

    print(lotReqTime.member, date, time)

    # ステータスを処理中に変更
    lotReqTime.status = '20'
    lotReqTime.save()

    # Selenium Web Driver 初期設定
    options = Options()
    options.add_argument('--headless')
    wd = webdriver.Chrome(options=options)

    try:
        # TMGBCトップ
        wd.get("https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html")
        sleep(0.5)
        print("title: ", wd.title)
        # print("title: ", wd.page_source)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_id('login').click()
    
        # ログイン
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        if wd.title == 'ログイン／TMGBC':
            sleep(4)
            wd.find_element_by_id('userid').send_keys(lotReqTime.member.tmgbc_id)
            wd.find_element_by_id('passwd').send_keys(lotReqTime.member.tmgbc_password)
            wd.find_element_by_id('login').click()
    
        # マイページメイン
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_id('goLotSerach').click()
    
        # 抽選種目
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_css_selector('input[value="' + sport + '"]').click()
        wd.find_element_by_id('doSearch').click()
    
        # 抽選公園一覧
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        while not wd.find_element_by_id('offset').get_attribute('value') == location_page:
            wd.find_element_by_id('goNextPager').click()
            sleep(0.5)
        wd.find_element_by_name('layoutChildBody:childForm:igcdListItems:' + location_id + ':doAreaSet').click()
    
        # 抽選申込日時設定
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_css_selector('a.calclick[onclick="javascript:selectCalendarDate(' + date + ');return false;"]').click()
        sleep(0.5)
        wd.find_element_by_css_selector('input[value="' + time + '"]').click()
        wd.find_element_by_id('doDateTimeSet').click()
    
        # 抽選申込内容確認
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_id('doOnceFix').click()
        wait = WebDriverWait(wd, 10)
        wait.until(expected_conditions.alert_is_present())
        Alert(wd).accept()
    
        # 抽選申込完了
        sleep(0.5)
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)

        # Selenium Web Driver 終了
        wd.quit()

        # ステータスを完了に変更
        lotReqTime.status = '30'
        lotReqTime.save()

    except Exception as e:

        print(e)

        # ステータスをエラーに変更
        lotReqTime.status = '40'
        lotReqTime.save()


