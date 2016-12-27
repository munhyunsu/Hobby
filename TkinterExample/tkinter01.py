#!/usr/bin/python3

# TODO(LuHa): 라이브러리 추가
import tkinter


# TODO(LuHa): 기본 GUI
class Application(tkinter.Frame):
    """기본 GUI
    """
    def __init__(self, master = None):
        """초기화
        """
        self._master = master
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """메인 창 생성
        """
        self.hi_there = tkinter.Button(self)
        self.hi_there['text'] = 'Hello World\n(Click me)'
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack(side = 'top')
        self.quit = tkinter.Button(self, text = 'QUIT', \
                fg = 'red', command = self._master.destroy)
        self.quit.pack(side = 'bottom')

    def say_hi(self):
        """함수
        """
        print('hi there, everyone!')



def main():
    root = tkinter.Tk()
    app = Application(master = root)
    app.mainloop()



if __name__ == '__main__':
    main()
