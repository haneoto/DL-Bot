import sqlite3
import os
import glob
import re

# XHS-Downloader下载目录
BASE_DIR = r'F:\Download'

def find_first_media_file(extension_list):
    latest_file = None
    latest_ctime = 0
    for ext in extension_list:
        files = glob.glob(os.path.join(BASE_DIR, f'*.{ext}'))
        for file in files:
            ctime = os.path.getctime(file)
            if ctime > latest_ctime:
                latest_ctime = ctime
                latest_file = file
    if latest_file:
        return os.path.splitext(os.path.basename(latest_file))[0]
    return None

def sanitize_filename(filename):
    return re.sub(r'_\d+(\.txt)$', r'\1', filename)

def sqlite_to_text(db_file, txt_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    content_lines = []

    remove_prefixes = ("采集时间", "收藏数量", "评论数量", "分享数量", "点赞数量")

    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        for row in rows:
            for col, val in zip(column_names, row):
                line = f"{col}: {val}"
                if not line.startswith(remove_prefixes):
                    line = line.replace("[话题]", "")
                    content_lines.append(line)
            content_lines.append("")

    conn.close()

    if not content_lines:
        return False

    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(content_lines))

    return True

def main():
    db_file = os.path.join(BASE_DIR, 'ExploreData.db')
    media_file_name = find_first_media_file([
        'mp4', 'mov', 'm4v', 'webp', 'jpg', 'jpeg', 'png', 'heic'
    ])

    if media_file_name:
        txt_file = os.path.join(BASE_DIR, f'{media_file_name}.txt')
    else:
        txt_file = os.path.join(BASE_DIR, 'ExploreData.txt')

    txt_file = sanitize_filename(txt_file)

    if os.path.exists(db_file):
        created_txt = sqlite_to_text(db_file, txt_file)
        os.remove(db_file)
        if created_txt:
            print(f"Converted {db_file} to {txt_file} and deleted the database file.")
        else:
            print(f"{db_file} is empty. No txt file was created. Database deleted.")
    else:
        print(f"{db_file} does not exist.")

if __name__ == "__main__":
    main()
