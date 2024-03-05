"""

统一身份认证页面自动登录
(作为测试样例,当前脚本登录后默认跳转至 应用平台 ,如有其他需要,请自行更改)

"""
import time
import ddddocr
import Config
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 自定义内容
username = Config.StudentID
password = Config.password0

# 创建 ChromeOptions 实例
chrome_options = webdriver.ChromeOptions()
# 设置忽略 SSL 错误和忽略 SSL 错误提示
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
# 创建 Chrome WebDriver 实例时将选项传递给 options 参数
driver = webdriver.Chrome(options=chrome_options,service=Service(Config.ChromedriverPath))
chrome_options.add_argument('--headless')
driver.maximize_window()
# 打开网页
targeturl="https://jwgl-443.wvpn.hrbeu.edu.cn/jwapp/sys/emaphome/portal/index.do#/"
driver.get(targeturl)

# time.sleep(1)

def Fill(res):
    # 输入学号
    username_input = driver.find_element(By.CSS_SELECTOR, "#username")
    # username_input.clear()  # 清空输入框
    username_input.send_keys(username) 
    # 输入密码
    password_input = driver.find_element(By.CSS_SELECTOR, "#password")
    # password_input.clear()  # 清空输入框
    password_input.send_keys(password)
    # 等待验证码输入框可见
    verify_code_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "captcha")))
    # 输入验证码
    # verify_code_input.clear()  # 清空输入框
    verify_code_input.send_keys(res)

def CasIdentify():
    if "cas-443.wvpn.hrbeu.edu.cn" in driver.current_url:
        # 识别验证码
        # 等待图片元素可见
        image_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[width="93"][height="42"]')))
        # 提取图片的 Base64 编码字符串
        vcodesrc = image_element.get_attribute("src").replace("%0A", "")
        ocr = ddddocr.DdddOcr()
        res = ocr.classification(base64.b64decode(vcodesrc[len("data:image/jpeg;base64,"):]))
        print("验证码识别结果为:",res)
        # 填充账户、密码、验证码
        Fill(res)
        # 等待“登录”按钮可点击，并点击
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit"))).click()

CasIdentify()
if  "jwgl-443.wvpn.hrbeu.edu.cn" in driver.current_url:
    print("登录成功")

# 无限期暂停程序执行
while True:
    time.sleep(1)