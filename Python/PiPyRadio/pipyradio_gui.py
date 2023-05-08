from tkinter import *
from tkinter import ttk
import threading
from time import strftime, localtime
import os

#---- class GUI ----------------------------------------------------------------

class GUI(threading.Thread):    
    def __init__(self):
        threading.Thread.__init__(self) # Tkinter canvas
        self.daemon = True # so it will be killed with the main thread!
        self.start()
        self.main_title = "" # No window title
        self.standard_font = ["Helvetica", 16, "bold"]
        self.textbox_font = ["Courier", 16, "bold"]
        self.station_names = []
        self.station_playing = ""
        self.flag_exit = False
        self.flag_shutdown = False
        self.flag_play = False
        self.flag_vol_down = False
        self.flag_vol_up = False
        self.flag_next = False
        self.flag_mute = False
        self.number_of_stations = 0
        self.station_page = 0
        self.padx = 3
        self.pady = 3
        self.button_ipady_height = 15 # button height
        self.button_height = 18
        self.button_width = 14
        self.button_width_small = 12
        self.image = "pipyradio_488.png"
        self.geometry = '800x480'
   
    def play(self,station):        
        self.flag_play = True        
        self.station_playing = station
        return
        
    def command(self,command):        
        if command == "Vol UP":
            self.flag_vol_up = True
        if command == "Vol DOWN":
            self.flag_vol_down = True
        if command == "MUTE":
            self.flag_mute = True
        if command == "NEXT":
            self.station_page += 1            
            print(self.number_of_stations)
            if (self.number_of_stations <= self.station_page*8):
                self.station_page = 0;
            self.update_station_buttons()                            
            self.flag_next = True
        if command == "QUIT":
            self.flag_exit = True
        if command == "SHUTDOWN":
            self.flag_shutdown = True
            
    def init_ttk_styles(self):
        self.s = ttk.Style()
        #frames
        self.s.configure("all.TFrame", background="lightgrey")
        self.s.configure("test.TFrame", background="grey")
        #widgets
        self.s.configure("default.TLabel", background="lightgrey",
                         font=self.standard_font)
        self.s.configure("time.TLabel", background="lightgrey",
                         font=self.standard_font)
        self.s.configure("important.TButton", background="lightgreen",
                         font=self.standard_font, height = 150, borderwidth=7)
        self.s.configure("default.TButton", background="lightgrey",
                         font=self.standard_font, borderwidth=7)
        self.s.configure("quit.TButton", background="lightgrey",
                         font=self.standard_font, borderwidth=3)
        self.s.map("important.TButton",background = [("active", 'lawngreen')])    

    def update_station_buttons(self):
        try:
            self.station_1.set(self.station_names[0+8*self.station_page])
        except:
            self.station_1.set("NA")
        try:
            self.station_2.set(self.station_names[1+8*self.station_page])
        except:
            self.station_2.set("NA")
        try:
            self.station_3.set(self.station_names[2+8*self.station_page])
        except:
            self.station_3.set("NA")
        try:
            self.station_4.set(self.station_names[3+8*self.station_page])
        except:
            self.station_4.set("NA")
        try:
            self.station_5.set(self.station_names[4+8*self.station_page])
        except:
            self.station_5.set("NA")
        try:
            self.station_6.set(self.station_names[5+8*self.station_page])
        except:
            self.station_6.set("NA")
        try:
            self.station_7.set(self.station_names[6+8*self.station_page])
        except:
            self.station_7.set("NA")
        try:
            self.station_8.set(self.station_names[7+8*self.station_page])
        except:
            self.station_8.set("NA")
        
    def update_time(self):        
        ftime = strftime("%d.%m.%y %H:%M:%S", localtime())        
        self.label_time['text'] = ftime
        self.label_time.after(1000, self.update_time)        

    def run(self):        
        self.mainWin = Tk()
        self.init_ttk_styles()        
        self.mainWin.protocol("WM_DELETE_WINDOW", self.command("Quit"))
        self.mainWin.title(self.main_title)
        self.mainWin.columnconfigure(0, weight=1)
        self.mainWin.rowconfigure(0, weight=1)
        self.mainWin.config(cursor = 'none') # Gone that cursor arrow, not needed!!
        self.mainWin.geometry(self.geometry) # This is our Gui format        
        self.mainWin.overrideredirect(Y) # Gone that blue top ribbon, we want a fixed GUI 
        self.station_1 = StringVar()
        self.station_2 = StringVar()
        self.station_3 = StringVar()
        self.station_4 = StringVar()
        self.station_5 = StringVar()
        self.station_6 = StringVar()
        self.station_7 = StringVar()
        self.station_8 = StringVar()
        self.station_1.set(self.station_names[0])
        self.station_2.set(self.station_names[1])
        self.station_3.set(self.station_names[2])
        self.station_4.set(self.station_names[3])
        self.station_5.set(self.station_names[4])
        self.station_6.set(self.station_names[5])
        self.station_7.set(self.station_names[6])
        self.station_8.set(self.station_names[7])
        
        # frame Main +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.frame_Main = ttk.Frame(self.mainWin, borderwidth=5, relief='ridge',
                                   padding="5 5 5 5", style = "all.TFrame")
        self.frame_Main.grid(column=0, row=0, sticky="WNES")
        for column in range(0,1): # 1 columns
            self.frame_Main.columnconfigure(column, weight=1)
        for row in range(0,4):    # 4 rows
            self.frame_Main.rowconfigure(row, weight=1)
            
        # frame Header: Image with time and fontsize spinbox +++++++++++++++++++
        self.frame_Header = ttk.Frame(self.frame_Main, borderwidth=3, relief='groove',
                                      padding="5 5 5 5", style="all.TFrame")
        self.frame_Header.grid(column=0, row=0, sticky="NWE")
        for column in range(0,3): # 3 columns
            self.frame_Header.columnconfigure(column, weight=1)
        for row in range(0,2):    # 2 rows
            self.frame_Header.rowconfigure(row, weight=1)        
        self.imageL1 = PhotoImage(file=self.image)
        self.label_png = ttk.Label(self.frame_Header, text="",
                                   image=self.imageL1,                                   
                                   style="default.TLabel")
        self.label_png.grid(ipady=3, column=0, row=1, columnspan=3, sticky="N")
        self.label_time = ttk.Label(self.frame_Header, text="",
                                    justify='right',
                                    style="time.TLabel")
        self.label_time.grid(ipady=7, column=2, row=0, sticky="NE")
        # frame Info ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.frame_Info = ttk.Frame(self.frame_Main,  borderwidth=3,
                                      padding="5 5 5 5", relief='groove',
                                      style="all.TFrame")
        self.frame_Info.grid(column=0, row=1, sticky="SWE")
        for column in range(0,1): # 1 columns
            self.frame_Info.columnconfigure(column, weight=1)
        for row in range(0,1):    # 1 rows
            self.frame_Info.rowconfigure(row, weight=1)        
        self.label_song = ttk.Label(self.frame_Info, text="",
                                    justify='right',
                                    style="default.TLabel")
        self.label_song.grid(ipady=5, column=0, row=0, sticky="W")
        
        # frame Buttons ++++++++++++++++++++++++++++++++++++++++++++
        self.frame_Buttons = ttk.Frame(self.frame_Main, style = "all.TFrame")
        self.frame_Buttons.grid(column=0, row=2, sticky=(W))
        column_nrs = 4
        row_nrs = 3
        for column in range(0,column_nrs):
            self.frame_Buttons.columnconfigure(column, weight=1)        
        for row in range(0,row_nrs):
            self.frame_Buttons.rowconfigure(row, weight=1)        
        self.button_station_1 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_1,
                                      command = lambda: self.play(self.station_1.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_1.grid(ipady=self.button_ipady_height, column=0, row=0)
        self.button_station_2 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_2,
                                      command = lambda: self.play(self.station_2.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_2.grid(ipady=self.button_ipady_height, column=1, row=0)
        self.button_station_3 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_3,
                                      command = lambda: self.play(self.station_3.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_3.grid(ipady=self.button_ipady_height, column=2, row=0)
        self.button_station_4 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_4,
                                      command = lambda: self.play(self.station_4.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_4.grid(ipady=self.button_ipady_height, column=0, row=1)
        self.button_station_5 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_5,
                                      command = lambda: self.play(self.station_5.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_5.grid(ipady=self.button_ipady_height, column=1, row=1)
        self.button_station_6 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_6,
                                      command = lambda: self.play(self.station_6.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_6.grid(ipady=self.button_ipady_height, column=2, row=1)
        self.button_station_7 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_7,
                                      command = lambda: self.play(self.station_7.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_7.grid(ipady=self.button_ipady_height, column=0, row=2)
        self.button_station_8 = ttk.Button(self.frame_Buttons,
                                      textvariable = self.station_8,
                                      command = lambda: self.play(self.station_8.get()),
                                      width = self.button_width,
                                      style="important.TButton")
        self.button_station_8.grid(ipady=self.button_ipady_height, column=1, row=2)
        self.button_next = ttk.Button(self.frame_Buttons,
                                 text = "NEXT",
                                 command = lambda: self.command("NEXT"),
                                 width = self.button_width,
                                 style="important.TButton")
        self.button_next.grid(ipady=self.button_ipady_height, column=2, row=2)
        self.button_vol_up = ttk.Button(self.frame_Buttons,
                                   text = "Vol UP",
                                   command = lambda: self.command("Vol UP"),
                                   width = self.button_width,
                                   style="default.TButton")
        self.button_vol_up.grid(ipady=self.button_ipady_height, column=3, row=0)
        self.button_vol_down = ttk.Button(self.frame_Buttons,
                                     text = "Vol DOWN",
                                     command = lambda: self.command("Vol DOWN"),
                                     width = self.button_width,
                                     style="default.TButton")
        self.button_vol_down.grid(ipady=self.button_ipady_height, column=3, row=1)
        self.button_mute = ttk.Button(self.frame_Buttons,
                                     text = "Radio MUTE",
                                     command = lambda: self.command("MUTE"),
                                     width = self.button_width,
                                     style="default.TButton")
        self.button_mute.grid(ipady=self.button_ipady_height, column=3, row=2)
        
        # frame Footer ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.frame_Footer = ttk.Frame(self.frame_Main,  borderwidth=3,
                                      padding="2 2 2 2", relief='groove',
                                      style="all.TFrame")
        self.frame_Footer.grid(column=0, row=3, sticky="WES")
        for column in range(0,4): # 4 columns
            self.frame_Footer.columnconfigure(column, weight=1)
        for row in range(0,1):    # 1 rows
            self.frame_Footer.rowconfigure(row, weight=1)        
        self.butt_quit = ttk.Button(self.frame_Footer, text='Quit',
                                    command = lambda: self.command("QUIT"),
                                    width = self.button_width,
                                    style="quit.TButton")
        self.butt_quit.grid(ipady=6, column=0, row=0, sticky="W")
        self.butt_shutdown = ttk.Button(self.frame_Footer, text='Shutdown',
                                    command = lambda: self.command("SHUTDOWN"),
                                    width = self.button_width,
                                    style="quit.TButton")
        self.butt_shutdown.grid(ipady=5, column=3, row=0, sticky="E")
        
        self.update_time()        
        # Padding
        for child in self.frame_Main.winfo_children():
            child.grid_configure(padx=self.padx, pady=self.pady)
        for child in self.frame_Header.winfo_children():
            child.grid_configure(padx=self.padx, pady=self.pady)
        for child in self.frame_Info.winfo_children():
            child.grid_configure(padx=self.padx, pady=self.pady)            
        for child in self.frame_Buttons.winfo_children():
            child.grid_configure(padx=self.padx, pady=self.pady)
        for child in self.frame_Footer.winfo_children():
            child.grid_configure(padx=self.padx, pady=self.pady)
        
        #self.mainWin.update_idletasks()
        self.mainWin.mainloop()
