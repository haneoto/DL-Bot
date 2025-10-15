import subprocess
import time
import sys
import os

# ---------- 配置区 ----------
downloader_path = r"D:\Tool\DouK-Downloader\main.exe"
script_path = r"D:\Tool\DouK-Downloader\Script\DetailData2txt.py"
# ---------------------------

def main():
    try:
        print("启动 DouK-Downloader...")
        # 启动 main.exe，并等待其关闭
        proc = subprocess.Popen([downloader_path])
        proc.wait()  # 等待下载程序执行完成（用户关闭后继续）

        print("检测到 DouK-Downloader 已退出，开始执行 DetailData2txt.py...")
        subprocess.run(["python", script_path], check=True)

        print("任务完成，1.5 秒后退出。")
        time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n用户手动中断。")
    except Exception as e:
        print("发生错误：", e)
        input("按回车键退出。")
        sys.exit(1)

if __name__ == "__main__":
    main()
