from flask import Flask, render_template, request
#from selenium import webdriver
import pymysql
import privateInfo
app=Flask(__name__)

@app.route('/')
def hello():
    return 'hell world!'
@app.route('/login',methods=['POST'])
def login():
    #Options = webdriver.ChromeOptions()
    #Options.add_argument('--headless')
    #driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=Options)
    #driver.get('https://kupis.konkuk.ac.kr/NxKonkuk/KUPIS/index.html')
    #driver.implicitly_wait(5)
    #driver.find_element_by_id('mainframe_childframe_form_div_cts_edSingleId_input').send_keys(set[0])
    #driver.find_element_by_id('mainframe_childframe_form_div_cts_edPassword_input').click()
    #driver.find_element_by_id('mainframe_childframe_form_div_cts_edPassword_input').send_keys(set[1])
    #driver.find_element_by_id('mainframe_childframe_form_div_cts_btnOkTextBoxElement').click()
    #driver.implicitly_wait(5)
    #try:
        #driver.find_element_by_id('mainframe_childframe_form_dvmain_dvsub_tvMenu_body_gridrow_2_cell_2_0_controltreeTextBoxElement').click()
    #except Exception as ex:
        #driver.close()
        #driver.quit()
        #return "아이디와 비밀번호를 확인하세요!"
    #driver.close()
    #driver.quit()
    table = pymysql.connect(host='localhost', user=privateInfo.user, password=privateInfo.password, db=privateInfo.db)
    curs = table.cursor()
    insertQuery = "INSERT INTO users VALUES ('" + request.form['Id'] + "','" + request.form['Pw'] + "','" + request.form['PhoneID'] + "');"
    curs.execute(insertQuery)
    table.commit()
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)