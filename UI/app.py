import tkinter as tk

from pages.first_page import FirstPage
from pages.camera_check_page import CheckCam
from pages.mock_interview_page import MockInterview
from pages.wait4game_page import WaitGame
from pages.introduct_game_page import IntroGames
from pages.intro_rsp_game_page import IntroRSPGame
from pages.rsp_game_page import RSPGame
from pages.intro_click_num_game_page import IntroClickGame
from pages.click_num_game_page import ClickGame
from pages.intro_compare_quantity_game_page import IntroCompareGame
from pages.compare_quantity_game_page import CompareGame
from pages.wait4result_page import WaitResult
from pages.result_page import Result



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Interview App")
        self.geometry("1920x1080")
        self.resizable(False,False)
        self.last = False
        #  결과 페이지가 바로 실행되더라도 안전하도록 기본 scores 초기화
        self.scores = {
            "rsp": {"correct": 0, "total": 0},
            "clicknum": {"correct": 0, "total": 0},
            "compare": {"correct": 0, "total": 0},
            "unfocus": {"time": 0.0},
            "tremor": {"time": 0.0}
        }

        self.frames = {}
        pages = (
            FirstPage,
            CheckCam,
            MockInterview,
            WaitGame,
            IntroGames,
            IntroRSPGame,
            RSPGame,
            IntroClickGame,
            ClickGame,
            IntroCompareGame,
            CompareGame,
            WaitResult,
            Result
        )

        for PageClass in pages:
            page_name = PageClass.__name__
            frame = PageClass(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("FirstPage")
    def show_frame(self, page_name: str):
        if page_name == "Result":
            self.last = True
        frame = self.frames.get(page_name)
        if frame is None:
#             # 디버그용 출력 — 필요 시 제거
            print(f"show_frame: '{page_name}' 프레임이 등록되어 있지 않습니다.")
            return
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
