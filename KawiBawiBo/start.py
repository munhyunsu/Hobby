#!/usr/bin/env python3

import os
import sys
import tkinter
import subprocess
import signal
import threading
import time
import copy

SRCPATH = './src/'

class GetParticipant(threading.Thread):
    def __init__(self, out):
        threading.Thread.__init__(self)
        self.out = out
        self.isrun = threading.Event()

    def run(self):
        out = self.out
        while not self.isrun.isSet():
            num_of_src = 0
            with os.scandir(SRCPATH) as it:
                for entry in it:
                    if not entry.name.startswith('.') and entry.is_file():
                        num_of_src = num_of_src + 1
            out.set('참가 인원수: ' + str(num_of_src))
            time.sleep(5)

    def set_isrun(self):
        self.isrun.set()
        #threading.Thread.join(self)


class GetRecent(threading.Thread):
    def __init__(self, out):
        threading.Thread.__init__(self)
        self.out = out
        self.isrun = threading.Event()
        self.submit = set()
        self.recent = list()
        with os.scandir(SRCPATH) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    self.submit.add(entry.name)
        for index in range(0, 10):
            self.recent.append('Unknown')

    def run(self):
        out = self.out
        new_submit = set()
        while not self.isrun.isSet():
            last_submit = copy.deepcopy(self.submit)
            self.submit.clear()
            with os.scandir(SRCPATH) as it:
                for entry in it:
                    if not entry.name.startswith('.') and entry.is_file():
                        if entry.name in last_submit:
                            pass
                        else:
                            self.recent.insert(0, entry.name)
                            self.recent.pop()
                        self.submit.add(entry.name)
            message = str()
            for node in self.recent:
                message = message + node + '\n'
            self.out.set(message)
            time.sleep(5)

    def set_isrun(self):
        self.isrun.set()
        #threading.Thread.join(self)


class KawiBawiBoFight(tkinter.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.isrun = threading.Event()
        master.title('KawiBawiBo Fight')
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
        l1_r = tkinter.LabelFrame(root, text = '최근 제출 10')
        l1_r.pack(side = 'right')
        l2_lt = tkinter.Frame(l1_l)
        l2_lt.pack(side = 'top')
        l2_lb = tkinter.Frame(l1_l)
        l2_lb.pack(side = 'bottom')
        # 버튼 생성
        participant = tkinter.StringVar()
        participant.set('참가 인원수: 000')
        participant_label = tkinter.Label(master = l2_lt,
                                          relief = 'solid',
                                          padx = 10, pady = 10,
                                          textvariable = participant)
        participant_label.pack(side = 'top')
        self.par_thread = GetParticipant(participant)
        self.par_thread.start()
        server_button = tkinter.Button(l2_lb)
        server_button['text'] = '서버 시작'
        server_button['command'] = self.start_server
        server_button.pack(side = 'left')
        self.server_button = server_button
        fight_button = tkinter.Button(l2_lb)
        fight_button['text'] = '경기 시작'
        fight_button['command'] = self.start_fight
        fight_button.pack(side = 'left')
        end_button = tkinter.Button(l2_lb)
        end_button['text'] = '종료'
        end_button['command'] = self.exit_fight
        end_button.pack(side = 'left')
        recent = tkinter.StringVar()
        recent.set('최근 제출 10')
        recent_message = tkinter.Message(master = l1_r,
                                         relief = 'flat',
                                         justify = 'center',
                                         textvariable = recent)
        recent_message.pack(side = 'bottom')
        self.rec_thread = GetRecent(recent)
        self.rec_thread.start()

    def start_server(self):
        self.sub_server = subprocess.Popen(['python3', 'kwb_server.py'])
        server_button = self.server_button
        server_button['text'] = '서버 종료'
        server_button['fg'] = 'red'
        server_button['command'] = self.end_server

    def end_server(self):
        try:
            self.sub_server.send_signal(signal.SIGINT)
        except:
            pass
        server_button = self.server_button
        server_button['text'] = '서버 시작'
        server_button['fg'] = 'black'
        server_button['command'] = self.start_server

    def exit_fight(self):
        root = self.master
        self.end_server()
        self.par_thread.set_isrun()
        self.rec_thread.set_isrun()
        root.destroy()

    def start_fight(self):
        os.system('gnome-terminal -e "python3 start_fight.py"')


def main(argv):
    os.makedirs(SRCPATH, exist_ok = True)
    root = tkinter.Tk()
    app = KawiBawiBoFight(master = root)
    app.mainloop()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
