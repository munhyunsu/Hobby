#!/usr/bin/env python3


import sys
import tkinter
import subprocess
import signal

class Application(tkinter.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """GUI 제작
        """
        # 내부 변수 불러오기
        root = self.master
        # 프레임 분할
        l1_l = tkinter.Frame(root)
        l1_l.pack(side = 'left')
        l1_r = tkinter.Frame(root)
        l1_r.pack(side = 'right')
        l2_lt = tkinter.Frame(l1_l)
        l2_lt.pack(side = 'top')
        l2_lb = tkinter.Frame(l1_l)
        l2_lb.pack(side = 'bottom')
        # 버튼 생성
        #participant_button = tkinter.Button(l2_lt)
        #participant_button['text'] = '참가인원수: 000'
        #participant_button.pack(side = 'top')
        participant = tkinter.StringVar()
        participant.set('참가 인원수: 000')
        participant_label = tkinter.Label(master = l2_lt,
                                            relief = 'solid',
                                            textvariable = participant)
        participant_label.pack(side = 'top')
        server_button = tkinter.Button(l2_lb)
        server_button['text'] = '서버 시작'
        server_button['command'] = self.start_server
        server_button.pack(side = 'left')
        self.server_button = server_button
        fight_button = tkinter.Button(l2_lb)
        fight_button['text'] = '경기 시작'
        fight_button.pack(side = 'left')
        end_button = tkinter.Button(l2_lb)
        end_button['text'] = '종료'
        end_button['command'] = root.destroy
        end_button.pack(side = 'left')
        recent_button = tkinter.Button(l1_r)
        recent_button['text'] = '최근 제출 10'
        recent_button.pack(side = 'bottom')

    def start_server(self):
        self.sub_server = subprocess.Popen(['python3', 'kwb_server.py'])
        server_button = self.server_button
        server_button['text'] = '서버 종료'
        server_button['command'] = self.end_server

    def end_server(self):
        self.sub_server.send_signal(signal.SIGINT)
        server_button = self.server_button
        server_button['text'] = '서버 시작'
        server_button['command'] = self.start_server

def main(argv):
    root = tkinter.Tk()
    app = Application(master = root)
    app.mainloop()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
