import os
import shutil
import tkinter as tk
import tkinter.messagebox as tm
from sys import exit

import ttkbootstrap as ttk
import urllib3

root = tk.Tk()
root.withdraw()

# 设置变量
var_airport = tk.StringVar()
var_airport.set("")
var_METAR = tk.StringVar()
var_METAR.set("")
STATE = False

style = ttk.Style(theme='cosmo')
TOP = style.master

main_win = tk.Tk()
main_win.title("METAR")
main_win.geometry("680x90")


def request():
    global STATE
    STATE = False
    enter_METAR.configure(state="normal")
    enter_METAR.delete(0, 'end')
    try:
        airport = enter_airport.get()
        airport = airport.upper()
        enter_airport.delete(0, 'end')
        enter_airport.insert('end', airport)

        path = str(airport) + '.TXT'
        url = 'https://tgftp.nws.noaa.gov/data/observations/metar/decoded/' + path
        c = urllib3.PoolManager()
        with c.request('GET', url, preload_content=False) as res, open(path, 'wb') as out_file:
            shutil.copyfileobj(res, out_file)
        try:
            os.remove(path)
        finally:
            url = 'https://tgftp.nws.noaa.gov/data/observations/metar/decoded/' + path
            c = urllib3.PoolManager()
            with c.request('GET', url, preload_content=False) as res, open(path, 'wb') as out_file:
                shutil.copyfileobj(res, out_file)
    except:
        enter_METAR.configure(state="readonly")
        tm.showerror("错误Error", "查询失败！\n(这可能由网络连接不稳定所致，您也许可以尝试检查网络连接与输入ICAO代码无误后再次点击查询)")
    else:
        f1 = open(path)
        info = f1.read()
        f2 = open(path)
        f2.readline()
        if "404" not in info:
            for item in f2:
                if "ob" in item:
                    item = item[3:]
                    enter_METAR.insert('end', item)
                    global var_METAR
                    var_METAR = item
            f1.close()
            f2.close()
            enter_METAR.configure(state="readonly")
            tm.showinfo(str(airport) + ' METAR报文', info + '\nTip:此报文文本已保存在程序所在文件夹内')
            STATE = True
        else:
            enter_METAR.configure(state="readonly")
            tm.showerror("错误Error", "查询失败！\n未输入机场ICAO代码/机场ICAO代码错误")


def quit_main_win():
    if tm.askokcancel('退出程序', '退出METAR报文查询程序?'):
        global STATE
        STATE = False
        main_win.quit()
        main_win.destroy()
        exit()
        return 0


text_title = tk.Label(main_win, text='实时 METAR 报文查询', fg="black", font=("微软雅黑", 12), compound='center')
but_request = tk.Button(main_win, text='立即查询报文', font=("微软雅黑", 10), command=request)
but_quit = tk.Button(main_win, text="退出程序",  font=("微软雅黑", 10), command=quit_main_win)
lab_quit = tk.Label(main_win, text="(如果退不出就去任务管理器把我kill了)",  font=("微软雅黑", 9))
enter_airport = tk.Entry(main_win, textvariable=var_airport, state="normal",  font=("微软雅黑", 10))
enter_METAR = tk.Entry(main_win, textvariable=var_METAR, state="readonly", justify="left",  font=("微软雅黑", 9))
lab_airport = tk.Label(main_win, text="机场ICAO代码:",  font=("微软雅黑", 9))
lab_METAR = tk.Label(main_win, text="METAR:",  font=("微软雅黑", 9))

text_title.place(x=10, y=4)
lab_airport.place(x=5, y=33, width=80, height=20)
enter_airport.place(x=90, y=33, width=70, height=22)
but_request.place(x=170, y=33, width=85, height=22)
enter_METAR.place(x=55, y=60, width=620, height=25)
lab_METAR.place(x=5, y=60, width=45, height=20)
lab_quit.place(x=320, y=33, width=210, height=20)
but_quit.place(x=260, y=33, width=60, height=22)

main_win.protocol("WM_DELETE_WINDOW", quit_main_win)
main_win.overrideredirect(True)
main_win.attributes("-topmost", 1)
main_win.attributes("-alpha", 0.75)
main_win.geometry('+5+890')

if __name__ == '__main__':
    main_win.mainloop()
