from tkinter import Tk, Canvas, Button, PhotoImage, font
import os
from pathlib import Path
from PIL import Image, ImageOps, ImageTk

ASSETS_PATH = os.path.abspath("./UI/assets")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)


 # 화면 실행
window = Tk()
window.title('MAIN') # window 창 이름 - 위에 타이틀 부분
window.geometry("1920x1080") # window 화면 크기
window.configure(bg = "#FFFFFF")
window.resizable(False, False) # x, y 변경 허용 여부

canvas = Canvas(
    window,
    height= 1080,
    width= 1920
)
canvas.place(x=0, y=0)

#background image 넣기
# img_background = Image.open(relative_to_assets("img_background.png"))
img_back = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
canvas.create_image(960,540, image = img_back)

# 배경 이미지 넣기
img_winpage = Image.open(relative_to_assets("img_win.png"))
img_win = ImageTk.PhotoImage(img_winpage)
canvas.create_image(960.0,550.0, image = img_win)

# 버튼 이미지
img_area_time = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_white.png")))
canvas.create_image(960, 500, image = img_area_time)


# 시작 버튼
btn_start = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_pupple.png")))
canvas.create_image(960, 830, image = btn_start)

# 타이틀 텍스트
canvas.create_text(
    # 시작좌표
    # 300,
    960,
    160,
    anchor="center",
    text="AI 면접 훈련도구",
    fill= '#FFFFFF',
    font=("Malgun Gothic", 30)
)
# 상단 텍스트
canvas.create_text(
            970,
            350.0,
            anchor="center",
            justify= "center",
            text="부족한 면접 경험을                      \n채워 나가보세요",
            fill="#0C0A0D",
            font=("Malgun Gothic", 30)
)
canvas.create_text(
            1150,
            317.0,
            anchor="center",
            justify= "center",
            text="AI와 함께",
            fill="#430065",
            font=("Malgun Gothic", 38)
)

# 하단 텍스트
canvas.create_text(
            960,
            650.0,
            anchor="center",
            justify= 'center',   # 문자 중앙 정렬
            text="AI가 내 면접을 분석하고 판단하여 도움을 줘요\n"
                 "영상 면접 환경과 실제 면접의 훈련을 할 수 있어요\n"
                 "마지막 피드백을 통해 고쳐야 할 점을 알 수 있어요",
            fill="#353C92",
            font=("AnekGurmukhi", 24)
)





window.mainloop() 