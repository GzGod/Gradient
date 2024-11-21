import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

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

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# 从文件加载代理
PROXY_FILE = "proxies.txt"
ACTIVE_PROXY_FILE = "checked_proxies.txt"

def load_proxies(file_path):
    """从文件加载代理。"""
    with open(file_path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

def save_active_proxies(proxies):
    """将活动代理保存到文件。"""
    with open(ACTIVE_PROXY_FILE, "w") as f:
        f.writelines(f"{proxy}\n" for proxy in proxies)

def check_proxy(proxy):
    """检查代理是否可以连接到目标URL。"""
    target_url = "https://app.gradient.network/"  
    try:
        response = requests.get(
            target_url,
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        if response.status_code == 200:
            logger.info(f"代理 {proxy} 是活动的")
            return proxy
    except Exception as e:
        logger.warning(f"代理 {proxy} 失败: {e}")
    return None

def run_proxy_checker(proxies):
    """运行代理检查器以检查代理列表。"""
    logger.info("启动代理检查器...")
    活动代理 = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # 根据需要设置线程数
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(futures):
            result = future.result()
            if result:
                活动代理.append(result)
    logger.info(f"找到的活动代理: {len(活动代理)}")
    return 活动代理

def main():
    """运行代理检查器和执行机器人任务的主函数。"""
    # 加载代理
    代理 = load_proxies(PROXY_FILE)
    if not 代理:
        logger.error(f"在 {PROXY_FILE} 中未找到代理")
        return

    # 检查代理
    活动代理 = run_proxy_checker(代理)
    if not 活动代理:
        logger.error("未找到活动代理。退出...")
        return

    # 保存活动代理
    save_active_proxies(活动代理)
    logger.info(f"活动代理已保存到 {ACTIVE_PROXY_FILE}")

    # 使用活动代理启动主机器人
    logger.info("使用活动代理启动机器人执行...")

if __name__ == "__main__":
    main()
