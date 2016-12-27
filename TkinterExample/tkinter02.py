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
        self.set_property_window_size(master)
        super().__init__(master)
        self.pack()
        self.create_widgets()
    
    def set_property_window_size(self, root):
        """적절한 윈도우 사이즈로 설정
            400x300 이하일 경우 2/3 크기로 설정
            400x300 초과일 경우 400x300으로 설정
        """
        # 디스플레이 크기 확인
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 너비 설정
        if screen_width < 400:
            self._window_width = ((screen_width*2)//3)
        else:
            self._window_width = 400

        # 높이 설정
        if screen_height < 300:
            self._window_height = ((screen_height*2)//3)
        else:
            self._window_height = 300

        # 계산된 크기로 설정
        window_size = str(self._window_width) + 'x' + \
                str(self._window_height)
        root.geometry(window_size)


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
        print('hi there, everyone! ' + \
                'the default window size is {}x{}'.format(\
                self._window_width, self._window_height))



def main():
    root = tkinter.Tk()
    app = Application(master = root)
    app.mainloop()



if __name__ == '__main__':
    main()
