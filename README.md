# Gradient-Auto-Bot

这个Python脚本使用Selenium自动化网页交互，同时轮换使用代理列表以避免检测并保持高度匿名。它使用一个Chrome扩展程序，如果需要会自动下载，并尝试使用不同的代理连接到一个Web应用程序，直到成功连接。一旦建立连接，它会继续在后台运行任务，并在操作之间随机延迟。

## 注册Gradient

- 通过电子邮件注册: [*Gradient*](https://app.gradient.network/signup?code=YWT3BK)

## 加入我们

[*撸毛频道*](https://t.me/+FZHZVA_gEOJhOWM1)
[*土狗频道*](https://t.me/+0X5At4YG0_k0ZThl)
               ╔═╗╔═╦╗─╔╦═══╦═══╦═══╦═══╗
               ╚╗╚╝╔╣║─║║╔══╣╔═╗║╔═╗║╔═╗║
               ─╚╗╔╝║║─║║╚══╣║─╚╣║─║║║─║║
               ─╔╝╚╗║║─║║╔══╣║╔═╣╚═╝║║─║║
               ╔╝╔╗╚╣╚═╝║╚══╣╚╩═║╔═╗║╚═╝║
               ╚═╝╚═╩═══╩═══╩═══╩╝─╚╩═══╝

## 功能

- 从 `active_proxies.txt` 文件中轮换多个代理。
- 使用一个Chrome扩展程序（自动下载）以增强功能。
- 随机化User-Agent头以避免检测。
- 使用 `ThreadPoolExecutor` 并行运行任务以实现并发代理使用。
- 处理登录到Web应用程序并与UI交互。
- 操作之间随机延迟以模拟人类行为。

## 要求

在运行脚本之前，请确保你已安装以下内容：

- Python 3.8或更高版本
- Selenium
- WebDriver Manager
- Fake User-Agent库
- 把账号密码放入.env文件：

  ```ini
  APP_USER=your_email@example.com
  APP_PASS=your_password
  ```

## 在Linux上安装ChromeDriver

1. **检查Chrome版本**：
   打开Chrome，进入 `chrome://settings/help`，并记下版本号。

2. **安装ChromeDriver**：
   使用以下命令下载并安装ChromeDriver：
   ```bash
   sudo apt update
   sudo apt install -y wget unzip
   wget https://chromedriver.storage.googleapis.com/<your_chrome_version>/chromedriver_linux64.zip
   unzip chromedriver_linux64.zip
   sudo mv chromedriver /usr/local/bin/
   chmod +x /usr/local/bin/chromedriver
   ```
3. **验证安装驱动程序**：
   ```bash
   chromedriver --version
   ```

## 运行

1. 克隆仓库
  ```
  git clone https://github.com/Gzgod/Gradient.git && cd Gradient
  ```
2. 安装依赖
  ```
  pip install -r requirements.txt
  ```
3. 运行代理检查
   确保你的proxies.txt里已经有代理了
  ```
  python3 checker.py
  ```
4.代理检查后会自动将活动代理导入active_proxies.txt
  ```
  python3 bot.py
  ```
## 注意事项

- 代理列表：确保 `active_proxies.txt` 包含有效的工作代理列表。如果所有代理都失败，脚本将移动到下一个代理。
- 扩展程序：脚本会自动处理Chrome扩展程序的下载以增强功能。
