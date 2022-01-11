import matplotlib.pyplot as plt
from pandas import read_csv
from time import sleep, time
from PIL import Image, ImageTk
from cv2 import NORM_MINMAX, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, COLORMAP_JET, INTER_CUBIC, INTER_NEAREST, GaussianBlur, normalize, VideoCapture, applyColorMap, imread, imshow, merge, resize, split, waitKey
from numpy import array, cumsum, insert, mean, ndarray, reshape, sort, sqrt, where
from tkinter import Button, Checkbutton, BOTTOM, RIGHT, X, END, Entry, HORIZONTAL, IntVar, Label, LabelFrame, Listbox, Menu, Radiobutton, Scale, Scrollbar, StringVar, Tk, font, messagebox, ttk
from tkinter.filedialog import askopenfilename
import os
import glob
import threading as th
import sys


def print_ok(event):
    print('ok', event)


class App:
    def __init__(self):
        self.data = None
        self.cap = None
        self.quit_status = False
        self.play_status = False
        self.play_control = th.Thread(target=self.start_play)
        self.play_control.daemon = True
        self.keep_length = 0
        self.app = Tk()
        # self.app.resizable(width=False, height=False)
        self.app.title("Video marking tool")
        # self.app.iconbitmap("icon.ico")
        img_rgb = imread(os.path.join(os.getcwd(), 'logo.jpg'))
        img_rgb = resize(img_rgb, (320, 240), interpolation=INTER_NEAREST)

        imgs = LabelFrame(self.app, text="Videos")
        imgs.pack(side='top', expand=True, padx=10, pady=5)

        im1 = self.openCV_to_PhotoImage(img_rgb)
        left_view = Label(imgs, image=im1)
        left_view.pack(side='left', padx=10, pady=10)

        im2 = self.openCV_to_PhotoImage(img_rgb)
        right_view = Label(imgs, image=im2)
        right_view.pack(side='right', padx=10, pady=10)

        bar = Scale(self.app, from_=0, to=2000, tickinterval=200,
                    orient=HORIZONTAL, length=690)
        bar.pack()

        operation_frame = LabelFrame(self.app, text="Operation")
        operation_frame.pack(side='top', fill='both',
                             expand=True, padx=10, pady=5)

        open_btn = Button(
            operation_frame, text="Open [Ctrl+O]", command=self.select_path)
        open_btn.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        play_btn = Button(operation_frame, width=10,
                          text="Play [Space]", command=self.start_pause)
        play_btn.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        start_btn = Button(operation_frame, text="Start [<]")
        start_btn.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        end_btn = Button(operation_frame, text="End [>]")
        end_btn.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        complete_btn = Button(operation_frame, text="Complete [Enter]")
        complete_btn.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        label_frame = LabelFrame(self.app, text="Labels")
        label_frame.pack(side='top', fill='both', expand=True, padx=10, pady=5)

        v = StringVar()
        Radiobutton(label_frame, text='a走路', variable=v, value='walk').pack(padx=5, side='left')
        Radiobutton(label_frame, text='s站着', variable=v, value='stand').pack(padx=5, side='left')
        Radiobutton(label_frame, text='d起身', variable=v, value='standup').pack(padx=5, side='left')
        Radiobutton(label_frame, text='f坐着', variable=v, value='sit').pack(padx=5, side='left')
        Radiobutton(label_frame, text='g坐下', variable=v, value='sitdown').pack(padx=5, side='left')
        Radiobutton(label_frame, text='h摔倒', variable=v, value='falling').pack(padx=5, side='left')
        Radiobutton(label_frame, text='j摔倒后挣扎/不动', variable=v, value='falled').pack(padx=5, side='left')
        Radiobutton(label_frame, text='k躺下', variable=v, value='lying').pack(padx=5, side='left')
        Radiobutton(label_frame, text='l睡觉（活蛆）', variable=v, value='sleeping').pack(padx=5, side='left')
        Radiobutton(label_frame, text=';活动', variable=v, value='active').pack(padx=5, side='left')
        v.set('walk')

        label_list = Listbox(self.app, width=100)
        label_list.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        xscrollbar = Scrollbar(self.app, orient=HORIZONTAL, command=label_list.xview)
        xscrollbar.pack(side=BOTTOM, fill=X)
        label_list.config(xscrollcommand=xscrollbar.set)

        self.left_view = left_view
        self.right_view = right_view
        self.bar = bar
        self.open_btn = open_btn
        self.play_btn = play_btn
        self.label_list = label_list

        self.current_selected_file = None
        self.current_start_pos = 0
        self.current_end_pos = 0
        self.current_label = v

        self.app.bind('<Control-o>', self.select_path)
        self.app.bind('<space>', self.start_pause)

        self.app.bind('<,>', self.submit_label)#188
        self.app.bind('<.>', self.submit_label)#190
        self.app.bind('<Left>', self.submit_label)#37
        self.app.bind('<Right>', self.submit_label)#39
        self.app.bind('<Return>', self.submit_label)#13

        self.app.bind('<a>', self.submit_label)#65
        self.app.bind('<s>', self.submit_label)#83
        self.app.bind('<d>', self.submit_label)#68
        self.app.bind('<f>', self.submit_label)#70
        self.app.bind('<g>', self.submit_label)#71

        self.app.bind('<h>', self.submit_label)#72
        self.app.bind('<j>', self.submit_label)#74
        self.app.bind('<k>', self.submit_label)#75
        self.app.bind('<l>', self.submit_label)#76
        self.app.bind('<;>', self.submit_label)#186

        self.load_label_csv()
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()

    def get_fir_frame(self, pos):
        df = self.data[pos:pos+1]
        data = array(df).reshape((24, 32))
        frame = self.data_to_frame(data)
        frame = self.raw_img(frame)
        return self.openCV_to_PhotoImage(frame)

    def get_video_frame(self, pos):
        self.cap.set(CAP_PROP_POS_FRAMES, pos)
        _, img = self.cap.read()
        return self.openCV_to_PhotoImage(img)

    def update_win(self, pos=0):
        frame_num = int(
            pos * (self.cap.get(CAP_PROP_FRAME_COUNT)*0.97) / len(self.data)
        ) - 25

        img_left = self.get_fir_frame(self.bar.get())
        self.left_view.config(image=img_left)
        self.left_view.image = img_left

        img_right = self.get_video_frame(self.bar.get() + 4)
        self.right_view.config(image=img_right)
        self.right_view.image = img_right
        
        self.bar.set(pos)
        # self.label_list.select_set(END)
        self.label_list.see(END)
        self.app.update()

    def start_pause(self, event=None):
        if not self.play_status:
            self.play_btn['text'] = 'Pause [Space]'
            self.play_status = True
        else:
            self.play_btn['text'] = 'Play [Space]'
            self.play_status = False

    def start_play(self):
        while not self.quit_status:
            # print('in loop')
            try:
                if self.play_status:
                    self.update_win(self.bar.get()+1)
                else:
                    self.update_win(self.bar.get())
            except ValueError as e:
                self.play_btn['text'] = 'Play [Space]'
                self.play_status = False
            sleep(1/25)
        # quit()

    @ staticmethod
    def raw_img(frame):
        return resize(frame, (320, 240), interpolation=INTER_NEAREST)

    @ staticmethod
    def data_to_frame(data):
        out_data = None
        out_data = normalize(data, out_data, 0, 255, NORM_MINMAX)
        img_gray = (out_data).astype('uint8')
        heatmap_g = img_gray.astype('uint8')
        frame = applyColorMap(heatmap_g, COLORMAP_JET)
        return frame

    @ staticmethod
    def openCV_to_PhotoImage(src):
        b, g, r = split(src)
        img = merge((r, g, b))
        return ImageTk.PhotoImage(Image.fromarray(img))

    def select_path(self, event=None):
        path_ = askopenfilename()
        if path_:
            # auto save when select new csv file
            if os.path.basename(path_) != self.current_selected_file:
                self.save_labels()
            self.quit_status = True
            self.keep_length = 0

            father_path = os.path.dirname(os.path.dirname(path_))
            date = os.path.basename(path_).split('.')[0].split('_')[0:2]
            data_path = glob.glob(
                '{}/data/{}_{}_*.csv'.format(father_path, date[0], date[1]))[0]
            video_path = glob.glob(
                '{}/video/{}_{}_*.mp4'.format(father_path, date[0], date[1]))[0]
            self.data = read_csv(data_path, index_col=None).iloc[:, 2:]
            self.cap = VideoCapture(video_path)
            self.bar['to'] = len(self.data)
            self.bar['tickinterval'] = int(self.bar['to']/10)
            self.current_selected_file = os.path.basename(data_path)

            self.label_list.insert(END, self.current_selected_file)

            self.update_win(0)
            self.quit_status = False
            self.play_control.start()

        # self.start_pause()

    def submit_label(self, event=None):
        print(event)
        def update_last_line(keep_length=0, start=0, end=0, action=None):
            keep_string = ','.join(self.label_list.get(END).split(',')[0:keep_length+1])
            self.label_list.delete(END)
            if end == 0:
                pre = ',{}'.format(start)
            elif not action:
                pre = ',{},{}'.format(start, end)
            else:
                pre = ',{},{},{},'.format(start, end, action)
            self.label_list.insert(END, keep_string+pre)

        # self.app.bind('<a>', self.submit_label)#65
        # self.app.bind('<s>', self.submit_label)#83
        # self.app.bind('<d>', self.submit_label)#68
        # self.app.bind('<f>', self.submit_label)#70
        # self.app.bind('<g>', self.submit_label)#71
        # self.app.bind('<h>', self.submit_label)#72
        # self.app.bind('<j>', self.submit_label)#74
        # self.app.bind('<k>', self.submit_label)#75
        # self.app.bind('<l>', self.submit_label)#76
        # self.app.bind('<;>', self.submit_label)#186

        if event.keycode == 65:
            self.current_label.set('walk')
        if event.keycode == 83:
            self.current_label.set('stand')
        if event.keycode == 68:
            self.current_label.set('standup')
        if event.keycode == 70:
            self.current_label.set('sit')
        if event.keycode == 71:
            self.current_label.set('sitdown')
        if event.keycode == 72:
            self.current_label.set('falling')
        if event.keycode == 74:
            self.current_label.set('falled')
        if event.keycode == 75:
            self.current_label.set('lying')
        if event.keycode == 76:
            self.current_label.set('sleeping')
        if event.keycode == 186:
            self.current_label.set('active')
        
        self.app.update()

        
        if event.keycode == 188:
            self.bar.set(self.bar.get()-1)
        if event.keycode == 190:
            self.bar.set(self.bar.get()+1)

        if event.keycode == 37:
            self.current_start_pos = self.bar.get()
            update_last_line(self.keep_length, self.current_start_pos)

        if event.keycode == 39:
            self.current_end_pos = self.bar.get()
            update_last_line(self.keep_length, self.current_start_pos, self.current_end_pos)

        if event.keycode == 13:
            if self.current_start_pos < self.current_end_pos:
                update_last_line(self.keep_length, self.current_start_pos, self.current_end_pos, self.current_label.get())
                self.current_start_pos = 0
                self.current_end_pos = 0
                self.keep_length += 3
            else:
                messagebox.askokcancel("Error", "End postion must bigger than Start position.")

    def load_label_csv(self, path=os.path.join(os.getcwd(), 'labels.csv')):
        self.label_list.delete(0, END)
        with open(path, 'r') as f:
            for i in f.readlines():
                if i:
                    self.label_list.insert(END, i)
        # self.label_list.select_set(END)

    def save_labels(self):
        def get_last_line():
            try:
                with open(os.path.join(os.getcwd(), 'labels.csv'), 'r') as csvfile:
                    mLines = csvfile.readlines()
                return mLines[-1]
            except IndexError as e:
                return ''

        if self.label_list.get(END) != get_last_line():
            if len(self.label_list.get(END).split(',')) >= 4:
                with open(os.path.join(os.getcwd(), 'labels.csv'), 'a+') as f:
                    f.write(self.label_list.get(END)+'\n')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.save_labels()
            self.quit_status = True
            self.app.destroy()


if __name__ == "__main__":
    app = App()
