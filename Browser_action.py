browser_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

from selenium.webdriver import Edge, EdgeOptions, EdgeService, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 用于选择登录端口
from selenium.webdriver.edge.options import Options

# 造浏览器配置对象
Edge_op = Options()
# 隐藏 正在受到自动软件的控制 这几个字
# Edge_op.add_experimental_option("excludeSwitches", ["enable-automation"])
# Edge_op.add_experimental_option("useAutomationExtension", False)
# Edge_op.add_argument("--disable-blink-features")
# Edge_op.add_argument("--disable-blink-features=AutomationControlled")
# # 配置浏览器
Edge_op.add_experimental_option("debuggerAddress", "localhost:9666")
# 让浏览器带着这个配置运行
web = Edge(options=Edge_op)

# 修改 webdriver 值
web.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
)
# 测试环节
web.get("https://www.baidu.com")
# 通过百度页面，搜索烤鸭
web.find_element(by=By.XPATH, value='//*[@id="kw"]').send_keys("烤鸭", Keys.ENTER)
