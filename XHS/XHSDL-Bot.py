import subprocess
import pyperclip
import sys
import traceback
import time

# ---------- 配置区 ----------
downloader_path = r"D:\Tool\XHS-Downloader\V2.6\main.exe"
converter_script = r"D:\Tool\XHS-Downloader\Script\ExploreData2txt.py"
# ---------------------------

def main():
    try:
        # 从剪贴板获取 URL
        try:
            url = pyperclip.paste().strip()
        except Exception:
            url = ""

        if not url or not (url.startswith("http://") or url.startswith("https://")):
            print("剪贴板中未检测到有效的网页链接，请复制链接后再运行脚本。")
            input("\n按回车键退出。")
            return

        print(f"检测到链接：{url}")
        print("正在运行XHS-Downloader...\n")

        # 运行下载器并等待结束
        try:
            result = subprocess.run([downloader_path, "-u", url], check=False)
        except FileNotFoundError:
            print("找不到下载程序，请检查路径：", downloader_path)
            input("\n按回车键退出。")
            return

        if result.returncode != 0:
            print("下载程序执行失败或被中止。")
            input("\n按回车键退出。")
            return

        print("\n下载完成，正在执行数据格式转换脚本...\n")

        # 执行ExploreData.db转换脚本
        try:
            subprocess.run([sys.executable, converter_script], check=True)
        except subprocess.CalledProcessError:
            print("转换脚本执行出错。")
            input("\n按回车键退出。")
            return
        except FileNotFoundError:
            print("找不到转换脚本，请检查路径：", converter_script)
            input("\n按回车键退出。")
            return

        print("\n任务完成，即将退出。")
        time.sleep(1.5)

    except Exception:
        print("程序执行出现异常：")
        traceback.print_exc()
        input("\n按回车键退出。")

if __name__ == "__main__":
    main()
