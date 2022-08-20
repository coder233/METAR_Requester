# 导入模块
import datetime
import os
import tkinter as tk
import tkinter.messagebox as tm
from sys import exit

import ttkbootstrap as ttk
import wget

# 隐藏Tkinter默认窗口
root = tk.Tk()
root.withdraw()

# 初始化变量
var_airport = tk.StringVar()
var_airport.set("")
var_METAR = tk.StringVar()
var_METAR.set("")
# 此处STATE变量为Bool值,Ture表示正在查询报文信息,反之则为False
STATE = False

# UI美化
style = ttk.Style(theme='cosmo')
TOP = style.master


# 设置主窗口参数
main_win = tk.Tk()
main_win.title("METAR")
main_win.geometry("680x90")
main_win.overrideredirect(True)
main_win.attributes("-topmost", 1)
main_win.attributes("-alpha", 0.77)
main_win.geometry('+58+905')


# 定义查询METAR报文功能
def request():
    global STATE
    STATE = True
    # 设置enter_METAR输入框状态为"可写"并清空输入框
    enter_METAR.configure(state="normal")
    enter_METAR.delete(0, 'end')
    # 设置but_request,but_quit按钮状态为"失效",防止用户连续点击导致崩溃
    but_request.configure(state="disabled")
    but_quit.configure(state="disabled")
    try:
        # 获取enter_airport输入框内容(需要查询METAR的机场ICAO代码)
        airport = enter_airport.get()
        if airport == "":
            but_request.configure(state="normal")
            but_quit.configure(state="normal")
            enter_METAR.configure(state="readonly")
            STATE = False
            tm.showinfo("提示", "您还未输入机场ICAO")
            return 0
        # 将airport转换为全大写形式
        airport = airport.upper()
        # 清空并重新写入大写形式的airport
        enter_airport.delete(0, 'end')
        enter_airport.insert('end', airport)
        # 在输入框中写入"查询中......"提示
        enter_METAR.delete(0, 'end')
        enter_METAR.insert('end', "查询中......")

        main_win.update()

        # 定义变量path(下载的METAR报文保存路径),url(METAR下载网址)
        path = airport + '.TXT'
        url_metar = 'http://tgftp.nws.noaa.gov/data/observations/metar/stations/' + path
        files = os.listdir()
        if path in files:
            os.remove(path)
        # 下载报文
        wget.download(url_metar, path)
        # 刷新窗口
        main_win.update()

        # 输入显示当前时间
        time_now = datetime.datetime.now()
        enter_time.configure(state="normal")
        enter_time.delete(0, 'end')
        enter_time.insert('end', (str(time_now))[0:20])
        enter_time.configure(state="disabled")

    except:
        # 若报文查询失败弹出查询失败提示框,清空enter_METAR输入框并设置enter_METAR输入框状态为"只读"
        enter_METAR.delete(0, 'end')
        enter_METAR.insert('end', "查询失败 ≧ ﹏ ≦")
        main_win.update()
        enter_METAR.configure(state="readonly")
        tm.showerror("错误Error", "查询失败！\n(这可能由于输入的机场ICAO代码不存在或网络连接错误，您可以在检查无误后重试)")
        enter_METAR.configure(state="normal")
        enter_METAR.delete(0, 'end')
        enter_METAR.configure(state="readonly")
    else:
        # 打开获取的METAR报文文件并逐行读取
        f = open(path)
        f.readline()

        # 若报文获取成功,则清空enter_METAR输入框打开获取的文件并读取
        for item in f:
            if airport in item:
                # 截取METAR报文并保存在变量item中
                enter_METAR.delete(0, 'end')
                enter_METAR.insert('end', item)
                global var_METAR
                var_METAR = item

        # 关闭文件,显示报文内容,设置enter_METAR输入框状态为"只读"
        f.close()
        enter_METAR.configure(state="readonly")

        files = os.listdir()
        if path in files:
            os.remove(path)

    but_request.configure(state="normal")
    but_quit.configure(state="normal")
    STATE = False

# 定义退出程序功能
def quit_main_win():
    # 弹出是否退出提示框,若选择"是",关闭窗口与进程,返回值0
    but_request.configure(state="disabled")
    but_quit.configure(state="disabled")
    if tm.askokcancel('退出程序', '退出METAR报文查询程序?'):
        main_win.quit()
        main_win.destroy()
        exit()
        return 0
    else:
        but_request.configure(state="normal")
        but_quit.configure(state="normal")


# 定义各GUI组件
text_title = tk.Label(main_win, text='实时 METAR 报文查询', fg="black", font=("微软雅黑", 12), compound='center')
but_request = tk.Button(main_win, text='立即查询报文', font=("微软雅黑", 10), command=request)
but_quit = tk.Button(main_win, text="退出程序",  font=("微软雅黑", 10), command=quit_main_win)
enter_airport = tk.Entry(main_win, textvariable=var_airport, state="normal", font=("微软雅黑", 10))
enter_METAR = tk.Entry(main_win, textvariable=var_METAR, state="readonly", justify="left", font=("微软雅黑", 8))
enter_time = tk.Entry(main_win, state="disabled", font=("等线", 8))
lab_time = tk.Label(main_win, text="最近报文查询时间:", font=("等线", 8))
lab_airport = tk.Label(main_win, text="机场ICAO代码:", font=("微软雅黑", 9))
lab_METAR = tk.Label(main_win, text="METAR:", font=("微软雅黑", 9))

# 设置GUI组件位置
text_title.place(x=10, y=4)
but_request.place(x=285, y=33, width=85, height=22)
but_quit.place(x=375, y=33, width=60, height=22)
enter_METAR.place(x=55, y=60, width=620, height=25)
enter_airport.place(x=90, y=33, width=70, height=22)
enter_time.place(x=165, y=45, width=115, height=10)
lab_time.place(x=165, y=31, width=90, height=13)
lab_airport.place(x=5, y=33, width=80, height=20)
lab_METAR.place(x=5, y=60, width=45, height=20)

# 窗口循环
if __name__ == '__main__':
    main_win.mainloop()
