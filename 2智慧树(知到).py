"""

智慧树（知到）页面自动登录
(默认为https://www.zhihuishu.com/,如有需求，请自行更改变量 ===> TargetURL)
"""
import ddddocr
import time
import Config
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 自定义内容
username = Config.username
password = Config.password1

TargetURL = "https://www.zhihuishu.com/"
ZhihuishuURL = "https://passport.zhihuishu.com/login" # 可以设置为你想登录之后跳转到的页面（默认为主登录页面，登录后跳转）

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
driver.get(ZhihuishuURL)

def InputInfor():
    # 输入手机号
    driver.find_element(By.ID, "lUsername").send_keys(username)
    # 输入密码
    driver.find_element(By.ID, "lPassword").send_keys(password)
    


def getimg():
    # 获取图片的src属性值
    background_img_src= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "yidun_bg-img"))).get_attribute("src")
    block_img_src = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "yidun_jigsaw"))).get_attribute("src")
    # 下载图片
    urllib.request.urlretrieve(background_img_src,'background.jpg')
    urllib.request.urlretrieve(block_img_src,'block.png')

def text_dis():
    slide = ddddocr.DdddOcr(det=False, ocr=False)
    with open('block.png', 'rb') as f:
        target_bytes = f.read()
    with open('background.jpg', 'rb') as f:
        background_bytes = f.read()
    res = slide.slide_match(target_bytes, background_bytes, simple_target=True)
    return res.get('target')[0]

def slide():
    distance = text_dis()
    # 拖动滑块
    slide = driver.find_element(By.CLASS_NAME, 'yidun_slider.yidun_slider--hover')
    action_chains = webdriver.ActionChains(driver)
    # 点击，准备拖拽
    action_chains.click_and_hold(slide)
    action_chains.pause(0.2)
    action_chains.move_by_offset(distance +10, 0)
    action_chains.pause(0.8)
    action_chains.move_by_offset(10, 0)
    action_chains.pause(0.8)
    action_chains.move_by_offset(-10, 0)
    action_chains.release()
    action_chains.perform()
    time.sleep(3)

def ZhihuishuLogin():
    InputInfor()
    # 找到登录按钮并点击
    driver.find_element(By.CLASS_NAME, 'wall-sub-btn').click()
    getimg()
    slide()
    if  "onlineweb.zhihuishu.com" in driver.current_url:
        print("登录成功")
   
ZhihuishuLogin()
if TargetURL == driver.current_url:
    print("登录成功")

# 无限期暂停程序执行
while True:
    time.sleep(1)