import time
import winsound
from tkinter import *
from threading import Thread
time.sleep(3)


def sound():
    winsound.PlaySound('sirena.wav', winsound.SND_FILENAME)

def window():
    window = Tk()
    window.geometry("1700x700")
    window.title("Volleyball")
    l2 = Label(window, font='Arial 48', text="ЗАПИСЬ!!!, ЗАПИСЬ!!!, ЗАПИСЬ!!!")
    l2.pack()
    window.attributes('-topmost',True)
    window.mainloop()
th1 = Thread(target=sound)
th2 = Thread(target=window)
th1.start()
th2.start()

for i in range(100):
    time.sleep(2)
    print(i**2)