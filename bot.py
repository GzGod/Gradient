import os
import time
import logging
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from pathlib import Path
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

banner = """
               ╔═╗╔═╦╗─╔╦═══╦═══╦═══╦═══╗
               ╚╗╚╝╔╣║─║║╔══╣╔═╗║╔═╗║╔═╗║
               ─╚╗╔╝║║─║║╚══╣║─╚╣║─║║║─║║
               ─╔╝╚╗║║─║║╔══╣║╔═╣╚═╝║║─║║
               ╔╝╔╗╚╣╚═╝║╚══╣╚╩═║╔═╗║╚═╝║
               ╚═╝╚═╩═══╩═══╩═══╩╝─╚╩═══╝
               原作者gihub：airdropinsiders
               我的gihub：github.com/Gzgod
               我的推特：推特雪糕战神@Hy78516012
               TG群：https://t.me/+FZHZVA_gEOJhOWM1
               TG群（土狗交流）：https://t.me/+0X5At4YG0_k0ZThl
"""
print(banner)
time.sleep(1)

# 加载环境变量
load_dotenv()

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# 常量
EXTENSION_ID = "caacbgbklghmpodbdafajbgdnegacfmo"
CRX_URL = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=98.0.4758.102&acceptformat=crx2,crx3&x=id%3D{EXTENSION_ID}%26uc&nacl_arch=x86-64"
EXTENSION_FILENAME = "app.crx"
USER = os.getenv("APP_USER")
PASSWORD = os.getenv("APP_PASS")

# 验证凭据
if not USER or not PASSWORD:
    logger.error("请设置 APP_USER 和 APP_PASS 环境变量")
    exit(1)

# 从文件加载代理
with open("active_proxies.txt", "r") as f:
    proxies = [line.strip() for line in f if line.strip()]  # 移除空行

if not proxies:
    logger.warning("在 active_proxies.txt 中未找到代理。以直接模式运行。")
    proxies = [None]  # 添加直接模式（无代理）

# 初始化假用户代理生成器
ua = UserAgent()

# 下载Chrome扩展
def download_extension():
    """下载Chrome扩展。"""
    logger.info(f"从以下地址下载扩展: {CRX_URL}")
    ext_path = Path(EXTENSION_FILENAME)
    if ext_path.exists() and time.time() - ext_path.stat().st_mtime < 86400:
        logger.info("扩展已下载，跳过...")
        return
    response = requests.get(CRX_URL, headers={"User-Agent": ua.random})
    if response.status_code == 200:
        ext_path.write_bytes(response.content)
        logger.info("扩展下载成功")
    else:
        logger.error(f"下载扩展失败: {response.status_code}")
        exit(1)

# 为WebDriver设置Chrome选项，使用随机用户代理和代理
def setup_chrome_options(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 以无头模式运行
    chrome_options.add_argument(f"user-agent={ua.random}")  # 随机用户代理
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免在无头模式下崩溃

    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")
        logger.info(f"使用代理: {proxy}")
    else:
        logger.info("以直接模式运行（无代理）。")

    # 使用扩展（如果需要）
    ext_path = Path(EXTENSION_FILENAME).resolve()
    chrome_options.add_extension(str(ext_path))
    
    # 掩盖WebDriver（避免被检测）
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options

# 登录Web应用程序
def login_to_app(driver):
    """登录Web应用程序。"""
    driver.get("https://app.gradient.network/")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Enter Email"]'))
    )
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Enter Email"]').send_keys(USER)
    driver.find_element(By.CSS_SELECTOR, '[type="password"]').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button").click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/dashboard/setting"]'))
    )
    logger.info("登录成功")
# 打开Chrome扩展
def open_extension(driver):
    """打开Chrome扩展。"""
    driver.get(f"chrome-extension://{EXTENSION_ID}/popup.html")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Status")]'))
    )
    logger.info("扩展加载成功")

# 使用代理尝试连接
def attempt_connection(proxy):
    """尝试使用代理连接。"""
    chrome_options = setup_chrome_options(proxy)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        download_extension()
        login_to_app(driver)
        open_extension(driver)
        logger.info(f"使用代理连接成功: {proxy if proxy else '直接模式'}")
        return driver
    except Exception as e:
        logger.warning(f"代理失败: {proxy if proxy else '直接模式'} - 错误: {e}")
        driver.quit()
        return None

# 工作者函数，处理带延迟的代理测试
def worker(proxy):
    driver = attempt_connection(proxy)
    if driver:
        logger.info(f"代理 {proxy if proxy else '直接模式'} 正在工作。运行任务...")
        try:
            while True:
                time.sleep(random.uniform(20, 40))  # 动作之间的随机延迟，看起来更自然
                logger.info(f"在代理 {proxy if proxy else '直接模式'} 上运行任务...")
        except KeyboardInterrupt:
            logger.info("由于用户中断，停止工作者。")
        finally:
            driver.quit()
    else:
        logger.info(f"代理 {proxy if proxy else '直接模式'} 失败。移动到下一个。")

# 运行代理的主函数
def main():
    """运行代理的主函数。"""
    try:
        if len(proxies) == 1:
            logger.info(f"使用单模式: {'直接' if proxies[0] is None else proxies[0]}")
            worker(proxies[0])  # 直接运行，不使用线程
        else:
            logger.info(f"检测到多模式，运行在多线程模式。")
            max_workers = min(len(proxies), 5)  # 将线程限制为5以提高效率
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(worker, proxy) for proxy in proxies]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"工作者错误: {e}")
    except KeyboardInterrupt:
        logger.info("脚本被用户停止 (CTRL+C)。")

if __name__ == "__main__":
    main()
