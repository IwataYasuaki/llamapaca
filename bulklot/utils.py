from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from time import sleep
from django_rq import job

@job
def login_to_tmgbc(lotReqTime, sport, location_page, location_id, date, time):

    try:
        print(lotReqTime.member, date, time)

        # ステータスを処理中に変更
        lotReqTime.status = '20'
        lotReqTime.save()
    
        # Selenium Web Driver 初期設定
        options = Options()
        options.add_argument('--headless')
        wd = webdriver.Chrome(options=options)
    
        # TMGBCトップ
        wd.get("https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html")
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_id('login').click()
    
        # ログイン
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        if wd.title == 'ログイン／TMGBC':
            sleep(4)
            wd.find_element_by_id('userid').send_keys(lotReqTime.member.tmgbc_id)
            wd.find_element_by_id('passwd').send_keys(lotReqTime.member.tmgbc_password)
            wd.find_element_by_id('login').click()
    
        # マイページメイン
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_id('goLotSerach').click()
    
        # 抽選種目
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_css_selector('input[value="' + sport + '"]').click()
        wd.find_element_by_id('doSearch').click()
    
        # 抽選公園一覧
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        while not wd.find_element_by_id('offset').get_attribute('value') == location_page:
            wd.find_element_by_id('goNextPager').click()
            sleep(0.5)
        wd.find_element_by_name('layoutChildBody:childForm:igcdListItems:' + location_id + ':doAreaSet').click()
    
        # 抽選申込日時設定
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_css_selector('a.calclick[onclick="javascript:selectCalendarDate(' + date + ');return false;"]').click()
        sleep(0.5)
        wd.find_element_by_css_selector('input[value="' + time + '"]').click()
        wd.find_element_by_id('doDateTimeSet').click()
    
        # 抽選申込内容確認
        sleep(0.5)
        print("=============================================================")
        print("title: ", wd.title)
        print(wd.find_element_by_tag_name('body').text)
        wd.find_element_by_id('doOnceFix').click()
        wait = WebDriverWait(wd, 10)
        wait.until(expected_conditions.alert_is_present())
        Alert(wd).accept()
    
        # 抽選申込完了
        sleep(0.5)
        body = wd.find_element_by_tag_name('body').text
        print("=============================================================")
        print("title: ", wd.title)
        print(body)

        # ステータスを完了に変更
        if '抽選の申込みが完了しました。' in body:
            lotReqTime.status = '30'
            lotReqTime.save()
        else:
            raise Exception('抽選申込が正常に完了しませんでした。')

        # Selenium Web Driver 終了
        wd.quit()

    except Exception as e:

        print("=============================================================")
        print(e)

        # ステータスをエラーに変更
        lotReqTime.status = '40'
        lotReqTime.save()


def get_result(member):
    # Selenium Web Driver 初期設定
    options = Options()
    options.add_argument('--headless')
    wd = webdriver.Chrome(options=options)

    # TMGBCトップ
    wd.get("https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html")
    sleep(0.5)
    print("=============================================================")
    print("title: ", wd.title)
    print(wd.find_element_by_tag_name('body').text)
    wd.find_element_by_id('login').click()

    # ログイン
    sleep(0.5)
    print("=============================================================")
    print("title: ", wd.title)
    print(wd.find_element_by_tag_name('body').text)
    if wd.title == 'ログイン／TMGBC':
        sleep(4)
        wd.find_element_by_id('userid').send_keys(member.tmgbc_id)
        wd.find_element_by_id('passwd').send_keys(member.tmgbc_password)
        wd.find_element_by_id('login').click()

    # マイページメイン
    sleep(0.5)
    print("=============================================================")
    print("title: ", wd.title)
    print(wd.find_element_by_tag_name('body').text)
    lotStatusListItems = wd.find_elements_by_css_selector('#lotStatusListItems > tr')
    results = []

    # 抽選結果を取得
    for lotStatusListItem in lotStatusListItems:
        ymd = lotStatusListItem.find_element(By.ID, 'useymdLabel').text
        stime = lotStatusListItem.find_element(By.ID, 'stimeLabel').text
        etime = lotStatusListItem.find_element(By.ID, 'etimeLabel').text
        status = lotStatusListItem.find_element(By.ID, 'lotStateLabel').text
        results.append({'ymd': ymd, 'stime': stime, 'etime': etime, 'status': status})

    # Selenium Web Driver 終了
    wd.quit()

    return results


def get_result_test(member):
    #raise ValueError("error!")
    if member.name == '岩田康明':
        return [{'ymd': '2022年4月16日 土曜日',
                 'stime': '15時',
                 'etime': '17時',
                 'status': '【当選】確定する'},
                {'ymd': '2022年4月16日 土曜日',
                 'stime': '15時',
                 'etime': '17時',
                 'status': '落選'}]
    elif member.name == '岩田弓華':
        return [{'ymd': '2022年4月2日 土曜日',
                 'stime': '15時',
                 'etime': '17時',
                 'status': '【当選】確定する'},
                {'ymd': '2022年4月16日 土曜日',
                 'stime': '15時',
                 'etime': '17時',
                 'status': '落選'}]



