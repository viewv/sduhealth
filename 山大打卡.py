import os
from pathlib import Path
from tkinter import *
from tkinter import messagebox

from sduhealth import main


class GuiSon():
    def __init__(self):
        self.top = Toplevel()
        self.top.title('填写用户名和密码')
        self.top.iconbitmap(Path(sys.argv[0]).parent.joinpath('sdu.ico'))
        self.width = 250
        self.height = 120
        self.screenwidth = self.top.winfo_screenwidth()
        self.screenheight = self.top.winfo_screenheight()
        self.top.geometry('%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2))
        self.top.resizable(0, 0)

        self.label1 = Label(self.top, text="学工号:", font=("微软雅黑", 12))
        self.label1.place(x=20, y=18, width=50, height=20)
        self.text1 = Entry(self.top, width=10, highlightcolor="blue", font=("微软雅黑", 10))
        self.text1.place(x=80, y=20, width=150, height=20)

        self.label2 = Label(self.top, text="密码:", font=("微软雅黑", 12))
        self.label2.place(x=27, y=48, width=50, height=20)
        self.text2 = Entry(self.top, width=10, font=("微软雅黑", 10))
        self.text2.place(x=80, y=48, width=150, height=20)

        self.btn = Button(self.top, text="保存", font=("微软雅黑", 15),
                          bg='black', fg='white', relief='ridge',
                          command=lambda: infoSave(self.text1.get(), self.text2.get(), self.top))
        self.btn.place(x=85, y=78, width=80, height=35)

    def getUserInfo(self):
        if os.path.exists('./userinfo.txt'):
            with open('./userinfo.txt', 'r') as f:
                user = f.readline()
                password = f.readline()
                self.text1.select_clear()
                self.text2.select_clear()
                self.text1.insert(0, user.strip())
                self.text2.insert(0, password.strip())

    def mainloop(self):
        self.top.mainloop()


class GUI():
    def __init__(self):
        self.window = Tk()
        self.window.title("山大打卡")

        self.width = 250
        self.height = 200
        self.screenwidth = self.window.winfo_screenwidth()
        self.screenheight = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2))
        self.window.resizable(0, 0)
        self.window.iconbitmap(Path(sys.argv[0]).parent.joinpath('sdu.ico'))
        self.text = ''

    def LabelInit(self):
        label1 = Label(self.window, text='使用方法:1.配置用户名和密码', font=("微软雅黑", 10))
        label1.place(x=30, y=151)
        label2 = Label(self.window, text="2.点击一键打卡", font=("微软雅黑", 10))
        label2.place(x=86, y=171)

    def buttonInit(self):
        btn1 = Button(self.window, text="配置用户名和密码", font=("微软雅黑", 11),
                      fg='white', bg='#6495ED', command=create)
        btn1.place(x=60, y=30, width=130, height=30)

        btn2 = Button(self.window, text="一键打卡", font=("微软雅黑", 20),
                      bg='black', fg='white', relief='ridge',
                      command=lambda: clicked(self.text, self.window))
        btn2.place(x=35, y=100, width=180, height=50)
        # btn.bind("<Button-1>", clicked(self.text))

    def mainloop(self):
        self.window.mainloop()


def clicked(text, window):
    info = main()
    messagebox.showinfo('提示', info)


def infoSave(user, password, top):
    f = open('./userinfo.txt', 'w')
    f.write(user + '\n')
    f.write(password)
    messagebox.showinfo('提示', '信息保存成功！')
    top.destroy()


def create():
    gui2 = GuiSon()
    gui2.getUserInfo()
    gui.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.LabelInit()
    gui.buttonInit()
    gui.mainloop()
