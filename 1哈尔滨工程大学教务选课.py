"""

教务选课页面自动登录
(该页面验证码识别正确率不足100%,如若遇到失败，请重新尝试)
(作者太懒了,懒得去用其他的库)

"""
import time
import ddddocr
import base64
import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 自定义内容
username = Config.StudentID
password = Config.password0

# indexurl = "https://jwxk.hrbeu.edu.cn/xsxk/elective/grablessons?batchId=5500614d49a44ded84b68e244ae5010a" # 退补选
indexurl =  "https://jwxk.hrbeu.edu.cn/xsxk/elective/grablessons?batchId=222f7276d4b34668b0f92a28f7fb7a53" #重修

def Identify():
    # 声明 res 为全局变量
    global res 
    # 添加延迟确保页面完全加载
    time.sleep(0.5)
    # 获取图片的src属性值
    ssrc = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "vcodeImg"))).get_attribute("src")
    # 去除字符串前缀
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(base64.b64decode(ssrc[len("data:image/png;base64,"):]))
    print("识别结果：", res)
    return res 

def Fill(res):
    # 输入学号
    username_input = driver.find_element(By.CSS_SELECTOR, "#loginNameDiv input")
    username_input.clear()  # 清空输入框
    username_input.send_keys(username)
    # 输入密码
    password_input = driver.find_element(By.CSS_SELECTOR, "#loginPwdDiv input")
    password_input.clear()  # 清空输入框
    password_input.send_keys(password)
    # 等待验证码输入框可见
    wait = WebDriverWait(driver, 10)
    verify_code_input = wait.until(EC.visibility_of_element_located((By.ID, "verifyCode")))
    # 输入验证码
    verify_code_input.clear()  # 清空输入框
    verify_code_input.send_keys(res)

def check_and_fill_and_click():
    while driver.current_url != indexurl: 
        Identify()
        Fill(res)
        # 点击登录按钮
        driver.find_element(By.CSS_SELECTOR, ".longin-button").click()
        time.sleep(0.5)
        driver.get(indexurl)
        time.sleep(0.5)
        # 找到按钮并点击
        driver.find_element(By.CLASS_NAME, 'el-button.courseBtn.el-button--primary.is-round').click()
        time.sleep(0.1)

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
driver.get("https://jwxk.hrbeu.edu.cn/xsxk/profile/index.html")
check_and_fill_and_click()
# 创建 ActionChains 实例，并随机点击页面上的一个位置
ActionChains(driver).move_by_offset(100, 100).click().perform()
if "batchId" in driver.current_url:
    print("登录成功")

# 无限期暂停程序执行
while True:
    time.sleep(1)