import yt_dlp
import webbrowser
import re
from tkinter import Tk, Entry, Button, Label, messagebox, Frame
import os
import subprocess
import shutil  

def validate_url(url):
    youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+')
    return youtube_regex.match(url) is not None

def play_video(resolution):
    url = url_entry.get()
    if not url:
        messagebox.showerror("خطأ", "يرجى إدخال رابط يوتيوب.")
        return

    if not validate_url(url):
        messagebox.showerror("خطأ", "الرابط المدخل غير صالح.")
        return

    try:
        ydl_opts = {}

        if resolution == "high":
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'}
        elif resolution == "low":
            ydl_opts = {'format': 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]'}
        elif resolution == "audio":
            ydl_opts = {'format': 'bestaudio[ext=m4a]'}
        else:
            messagebox.showerror("خطأ", "خيار الدقة غير صحيح.")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = None
            audio_url = None

            if resolution in ["high", "low"]:
                video_url = info.get('url')
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and not video_url:
                            video_url = f['url']
                        if f.get('acodec') != 'none' and not audio_url:
                            audio_url = f['url']
            elif resolution == "audio":
                audio_url = info.get('url')

            if resolution in ["high", "low"] and video_url and audio_url:
                if shutil.which("mpv"):
                    subprocess.run(["mpv", video_url, "--audio-file=" + audio_url])
                else:
                    webbrowser.open(video_url)
            elif resolution == "audio" and audio_url:
                webbrowser.open(audio_url)
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على تنسيقات مناسبة للفيديو أو الصوت.")

    except yt_dlp.utils.DownloadError as e:
        messagebox.showerror("خطأ في التحميل", f"حدث خطأ أثناء معالجة الفيديو:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع:\n{str(e)}")


window = Tk()
window.title("مشغل الوسائط المتعددة")

Label(window, text="أضف الرابط هنا").pack(pady=5)
url_entry = Entry(window, width=50)
url_entry.pack(pady=5)

button_frame = Frame(window)
button_frame.pack(pady=5)

high_res_button = Button(button_frame, text="دقة عالية", command=lambda: play_video("high"))
high_res_button.pack(side="left", padx=5)

low_res_button = Button(button_frame, text="دقة منخفضة", command=lambda: play_video("low"))
low_res_button.pack(side="left", padx=5)

audio_button = Button(window, text="صوت فقط", command=lambda: play_video("audio"))
audio_button.pack(pady=5)

exit_button = Button(window, text="خروج", command=window.quit)
exit_button.pack(pady=5)

window.mainloop()

