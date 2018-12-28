from selenium import webdriver
from bs4 import BeautifulSoup
from pyfcm import FCMNotification
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymysql
import privateInfo
push_service = FCMNotification(api_key=privateInfo.serverKey)

getSQL = "SELECT %s FROM %s %s;" # 실행 할 쿼리문 입력
setSQL = "UPDATE subjects SET grade = '%s' %s;"
insertSQL = "INSERT INTO subjects VALUES ('%s','%s','%s');"

optionsa = webdriver.ChromeOptions()
optionsa.add_argument('headless')
optionsa.add_argument('window-size=1920x1080')
optionsa.add_argument("disable-gpu") #gpu 관련 에러가 나는경우 추가할 옵션. gpu를 이용해 js렌더링을 가속하는 옵션을 꺼줌

driver = webdriver.Chrome(privateInfo.chromeDriverPath, options=optionsa)
subjectIncluder = "mainframe_childframe_form_dvmain_dvsub_TabMainFrame_GradNowShtmGradeInq_dvFrame_gdGradeList_bodyGridBandContainerElement"
driver.get('https://kupis.konkuk.ac.kr/NxKonkuk/KUPIS/index.html')
wait = WebDriverWait(driver, 20)
while True:
    table = pymysql.connect(host=privateInfo.host, port=privateInfo.port, user=privateInfo.user, password=privateInfo.password, db=privateInfo.db)
    curs = table.cursor()
    curs.execute(getSQL%('*','users',''))
    sets = curs.fetchall()
    for set in sets:
        print(set[0])
        wait.until(EC.presence_of_element_located((By.ID, "mainframe_childframe_form_div_cts_edSingleId_input")))
        driver.find_element_by_id('mainframe_childframe_form_div_cts_edSingleId_input').send_keys(set[0])
        driver.find_element_by_id('mainframe_childframe_form_div_cts_edPassword_input').click()
        driver.find_element_by_id('mainframe_childframe_form_div_cts_edPassword_input').send_keys(set[1])
        driver.find_element_by_id('mainframe_childframe_form_div_cts_btnOkTextBoxElement').click()
        wait.until(EC.presence_of_element_located((By.ID, 'mainframe_childframe_form_dvmain_dvsub_tvMenu_body_gridrow_2_cell_2_0_controltreeTextBoxElement')))
        try:
            driver.find_element_by_id('mainframe_childframe_form_dvmain_dvsub_tvMenu_body_gridrow_2_cell_2_0_controltreeTextBoxElement').click()
            wait.until(EC.presence_of_element_located((By.ID,
                                                       'mainframe_childframe_form_dvmain_dvsub_tvMenu_body_gridrow_4_cell_4_0_controltreeTextBoxElement')))
            driver.find_element_by_id('mainframe_childframe_form_dvmain_dvsub_tvMenu_body_gridrow_4_cell_4_0_controltreeTextBoxElement').click()
        except:
            print("login error")
            driver.quit()
            driver = webdriver.Chrome(privateInfo.chromeDriverPath, options=optionsa)
            driver.get('https://kupis.konkuk.ac.kr/NxKonkuk/KUPIS/index.html')
            continue
        #-----------여기까지 성적조회페이지 들어오는 구간 -----------------
        wait.until(EC.presence_of_element_located((By.ID, subjectIncluder)))
        time.sleep(1)
        html = driver.find_element_by_id(subjectIncluder).get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        subjectNames = soup.select('div[id$=5GridCellTextContainerElement]')
        subjectGrades = soup.select('div[id$=10GridCellTextContainerElement]')
        for subjectName, subjectGrade in zip(subjectNames, subjectGrades):
            curs.execute(getSQL% ('*', 'subjects', "WHERE name = '"+subjectName.text+"' AND portalID = '"+set[0]+"'"))
            result = curs.fetchone()
            if(result):
                curs.execute(getSQL%('grade', 'subjects', "WHERE name = '"+subjectName.text+"' AND portalID = '"+set[0]+"'"))
                if(subjectGrade.text != curs.fetchone()[0]):
                    print(set[2])
                    registration_id = set[2];
                    message_title = "성적알림"
                    message_body = subjectName.text + " 과목의 성적이 변경되었습니다! 확인해보세요"
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,message_body=message_body)
                    print("성적이 변경되었습니다")
                    curs.execute(setSQL%(subjectGrade.text, "WHERE name = '"+subjectName.text+"' AND portalID = '"+set[0]+"'"))
                    table.commit()
            else:
                curs.execute(insertSQL%(subjectName.text,subjectGrade.text,set[0]))
                table.commit()
            print(subjectName.text)
            print(subjectGrade.text)
        driver.refresh()
    print("routine 1 ends")
    table.close()
    curs.close()

driver.close()
driver.quit()
print("done!")

