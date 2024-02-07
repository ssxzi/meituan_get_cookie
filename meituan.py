from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetToken:

    def open_url(self):
        # 设置为手机模式
        self.mobile_emulation = {"deviceName": "iPhone 6"}
        self.options = webdriver.EdgeOptions()
        self.options.add_experimental_option("mobileEmulation", self.mobile_emulation)
        self.driver = webdriver.Edge(options=self.options)

        # 调整窗口大小
        self.driver.maximize_window()
        self.driver.set_window_position((self.driver.get_window_size().get('width') - 375.2) / 2,
                                        (self.driver.get_window_size().get('height') - 687.83) / 2)
        self.driver.set_window_size(375.2, 687.83)

        # 打开网页
        self.driver.get("https://i.meituan.com")
        self.element = self.driver.find_element(By.CLASS_NAME, 'c-normal')
        self.element.click()
        WebDriverWait(self.driver, 600).until(EC.presence_of_element_located((By.CLASS_NAME, 'my-mt-logout')))
        self.get_cookie()
        # 关闭浏览器
        self.driver.quit()

    def get_cookie(self):
        # 获取Token和UUID
        self.cookies = self.driver.get_cookies()
        for cookie in self.cookies:
            if cookie['name'] == 'token':
                self.token = cookie['value']
            if cookie['name'] == 'uuid':
                self.uuid = cookie['value']
        self.cookie = self.token + '#' + self.uuid
        self.ui.text.setPlainText(self.cookie)

    def cope_cookie(self):
        # 复制到粘贴板
        self.text = self.ui.text.toPlainText()
        self.clipboard = QApplication.clipboard()
        self.clipboard.setText(self.text)

    def __init__(self):
        # 设置窗口图形界面
        self.ui = QUiLoader().load('src/meituan.ui')
        self.ui.button_url.clicked.connect(self.open_url)
        self.ui.button_cope.clicked.connect(self.cope_cookie)


app = QApplication()
# 设置窗口ico
app.setWindowIcon(QIcon('src/meituan.ico'))
gettoken = GetToken()
gettoken.ui.show()
app.exec_()
