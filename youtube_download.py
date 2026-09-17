import subprocess
import sys

def install_package(package):
    print(f"正在安裝 {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

# 首先卸載現有的yt-dlp以清除任何損壞的安裝
try:
    print("移除現有的yt-dlp安裝...")
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "yt-dlp"])
except:
    pass

# 正確安裝所需套件
required_libraries = ['yt-dlp']  # YouTube下載套件

for lib in required_libraries:
    install_package(lib)

print('安裝完成')
    
import os                       # 建立檔案
import tkinter as tk            # 介面設計
from tkinter import filedialog  # 文件選擇對話框
import yt_dlp                   # 抓取youtube影片

def rbvideo():
    global getvideo
    getvideo = videorb.get()

def clickDown():
    global getvideo
    labelMsg.config(text="")
    try:
        if(url.get() == ""):
            labelMsg.config(text="網址欄位必須輸入!")
            return
            
        if(path.get() == ""):
            pathdir = os.getcwd()
        else:
            pathdir = os.path.abspath(path.get().strip())

        if not os.path.exists(pathdir):
            os.makedirs(pathdir)

        print(f"Saving to: {pathdir}")

        ydl_opts = {
            'format': f'bestvideo[height<={getvideo[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(pathdir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url.get(), download=True)
                video_title = info['title']
                video_path = os.path.join(pathdir, f'{video_title}.mp4')
                labelMsg.config(text=f"Download Complete!\nFile saved as {video_path}")
        except yt_dlp.utils.DownloadError as e:
            labelMsg.config(text=f"Download error: {str(e)}")
        except Exception as e:
            labelMsg.config(text=f"Unexpected error: {str(e)}")

    except Exception as e:
        labelMsg.config(text=f"Error: {str(e)}")

def select_path():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path.set(selected_path)

win = tk.Tk()
win.title("download from youtube")
getvideo = "360p"         # 預設影片格式
videorb = tk.StringVar()  # 選項按鈕
url = tk.StringVar()      # 影片位址
path = tk.StringVar()     # 存檔位置

win_width = 390
win_height = 340
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
x = (screen_width - win_width) // 2
y = (screen_height - win_height) // 2
win.geometry(f"{win_width}x{win_height}+{x}+{y}")  # 設置視窗大小並置中

label1 = tk.Label(win, text="Youtube網址:")
label1.place(x=30, y=30)
entryUrl = tk.Entry(win, textvariable=url)
entryUrl.config(width=45)
entryUrl.place(x=30, y=60)

label2 = tk.Label(win, text="储存路徑(預設為當前資料夾):")
label2.place(x=30, y=90)
entryPath = tk.Entry(win, textvariable=path)
entryPath.config(width=40)
entryPath.place(x=30, y=120)

btnSelectPath = tk.Button(win, text="選擇路徑", command=select_path)
btnSelectPath.place(x=300, y=117)

label3 = tk.Label(win, text="影片格式")
label3.place(x=30, y=150)
rb1 = tk.Radiobutton(win, text="360p, mp4", variable=videorb, value='360p', command=rbvideo)
rb1.place(x=30, y=170)
rb1.select()
rb2 = tk.Radiobutton(win, text="720p, mp4", variable=videorb, value='720p', command=rbvideo)
rb2.place(x=30, y=190)

btnDown = tk.Button(win, text="下載影片", command=clickDown)
btnDown.place(x=300, y=300)
btnDown.lift()

labelMsg = tk.Label(win, text=">", fg='red', wraplength=350, justify='left', anchor='w')
labelMsg.place(x=30, y=230)

win.mainloop()