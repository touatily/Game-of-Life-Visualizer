####################################################
#                                                  #
#   Projet:             Conway's Game of Life      #
#   Author:             M. Lyes Touati             #
#   Last Update:        18/08/2020                 #
#                                                  #
####################################################

import tkinter as tk
from tkinter import filedialog
import csv
import sim
import time
import threading as th
from tkinter import messagebox as mb
from tkinter.colorchooser import askcolor
import subprocess
import os
import platform as pm
from PIL import Image, ImageDraw

class window(tk.Tk):

    def __init__(self):
        super().__init__()

        self.inited = False
        self.simStarted = False

        self.colorGrid = "blue"
        self.colorCells = "black"
        self.shapeCells = "square"
        self.clipboard = None

        # window configuration
        ## solve incompatibility problem of wm_state("zoomed") with Linux
        try:
            self.wm_state("zoomed")
        except:
            pad=3
            self.geometry("{0}x{1}+0+0".format( self.winfo_screenwidth()-pad,
                                                self.winfo_screenheight()-pad))
        self.title("Conway's game for life visualizer")

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.resizable(False, False)

        self.plan = tk.Frame(self, bg="grey")
        self.plan.pack(fill="both", padx=20, pady=20, expand=True)

        self.plan.grid_columnconfigure(0, weight=1)

        # menu configuration
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.loadConfig, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", command=self.saveConfig, accelerator="Ctrl+S")
        filemenu.add_command(label="Save as PDF", command=self.savePDF, accelerator="Ctrl+P")
        filemenu.add_command(label="Save as PS", command=self.savePS, accelerator="Ctrl+T")
        filemenu.add_command(label="Save as JPEG", command=self.saveJPG, accelerator="Ctrl+J")
        filemenu.add_command(label="Save as GIF", command=self.saveGIF, accelerator="Ctrl+G")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Clean Grid", command = self.cleanGrid, accelerator="Ctrl+C")
        editmenu.add_command(label="Fill Grid", command = self.fillGrid, accelerator="Ctrl+F")
        menubar.add_cascade(label="Edit", menu=editmenu)

        optionmenu = tk.Menu(menubar, tearoff=0)
        optionmenu.add_command(label="Grid Color", command = self.chooseColorGrid, accelerator="F1")
        optionmenu.add_command(label="Cells Color", command = self.chooseColorCells, accelerator="F2")
        optionmenu.add_command(label="Background Color", command = self.chooseColorBG, accelerator="F3")

        shapemenu = tk.Menu(menubar, tearoff=0)
        shapemenu.add_command(label="Square", command = lambda : self.selectShape(1), accelerator="Alt+S")
        shapemenu.add_command(label="Triangle", command = lambda : self.selectShape(2), accelerator="Alt+T")
        shapemenu.add_command(label="Circle", command = lambda : self.selectShape(3), accelerator="Alt+C")
        optionmenu.add_cascade(label="Shape of Cells", menu=shapemenu)

        menubar.add_cascade(label="Options", menu=optionmenu)
        
        simmenu = tk.Menu(menubar, tearoff=0)
        simmenu.add_command(label="Start/Stop Simulation", command = self.start, accelerator="Enter")
        simmenu.add_command(label="Next generation", command = self.step, accelerator="Right Arrow")
        menubar.add_cascade(label="Simulation", menu=simmenu)

        menubar.add_command(label="About", command=self.about, accelerator="Ctrl+A")
        self.config(menu=menubar)

        # canvas configuration
        self.canvas = tk.Canvas(self.plan, bg = "white",
                                height=h-91, bd=2, highlightbackground="black")
        
        self.canvas.grid(row = 0, column = 0, sticky="NEWS", ipadx=0, ipady=0)

        
        self.canvas.bind('<Button-1>', self.click1_canvas)
        self.canvas.bind('<Control-1>', self.click2_canvas)
        self.canvas.bind('<B1-Motion>', self.click1_canvas)
        self.canvas.bind('<Control-B1-Motion>', self.click2_canvas)
        self.canvas.bind('<Motion>', self.mouseMotion)
        
        
        # control buttons
        self.plan2 = tk.Frame(self.plan)
        self.plan2.grid(row=0, column=1, sticky="SN")

        self.clean = tk.Button(self.plan2, text="Clean", command=self.cleanGrid)
        self.clean.pack(ipadx=15, padx=10, ipady=5, pady=5)
        
        self.startStop = tk.Button(self.plan2, text="Start", command=self.start)
        self.startStop.pack(ipadx=15, padx=10, ipady=5, pady=5)

        self.btnStep = tk.Button(self.plan2, text="Step", command=self.step)
        self.btnStep.pack(ipadx=15, padx=10, ipady=5, pady=5)

        self.load = tk.Button(self.plan2, text="Load", command=self.loadConfig)
        self.load.pack(ipadx=15, padx=10, ipady=5, pady=5)

        self.save = tk.Button(self.plan2, text="Save", command=self.saveConfig)
        self.save.pack(ipadx=15, padx=10, ipady=5, pady=5)


        self.lspeed = tk.Label(self.plan2, text="Speed")
        self.lspeed.pack(ipadx=15, padx=10)
        
        self.speed = tk.Scale(self.plan2, from_=100, to=1)
        self.speed.pack(ipadx=15, padx=10)

        self.bind('<Control-s>', self.saveConfig)
        self.bind('<Control-c>', self.cleanGrid)
        self.bind('<Control-f>', self.fillGrid)
        self.bind('<Control-o>', self.loadConfig)
        self.bind('<Control-q>', self.exit)
        self.bind('<Control-p>', self.savePDF)
        self.bind('<Control-t>', self.savePS)
        self.bind("<Control-j>", self.saveJPG)
        self.bind("<Control-g>", self.saveGIF)

        self.bind('<Key>', self.keyPressed)
        self.bind('<Return>', self.start)
        self.bind('<F1>', self.chooseColorGrid)
        self.bind('<F2>', self.chooseColorCells)
        self.bind('<F3>', self.chooseColorBG)

        self.bind('<Up>', self.increaseSpeed)
        self.bind('<Down>', self.decreaseSpeed)
        self.bind('<Right>', self.step)

        self.bind('<Alt-s>', lambda e: self.selectShape(1, e))
        self.bind('<Alt-t>', lambda e: self.selectShape(2, e))
        self.bind('<Alt-c>', lambda e: self.selectShape(3, e))

        ## label showing mouse coordinate
        self.tv = tk.StringVar()
        self.coordinate = tk.Label(self.plan2, textvariable=self.tv, anchor='e')
        self.coordinate.pack(side="bottom", fill="x", pady=25)


        # button 2 (Mouse Wheel) events
        self.canvas.bind("<Button-3>", self.click_2)
        self.canvas.bind("<B3-Motion>", self.motion_2)
        self.canvas.bind("<ButtonRelease-3>", self.release_2)

        self.x = None
        self.y = None
        self.rmenu = None


    def click_2(self, e=None):
        if not self.rmenu:
            self.x = e.x - e.x%10
            self.y = e.y - e.y%10

    def motion_2(self, e):
        if not self.rmenu:
            self.canvas.delete("select")
            x = max(0, e.x - e.x%10)
            x = min(x, self.canvas.winfo_width())
            y = max(0, e.y - e.y%10)
            y = min(y, self.canvas.winfo_height())
            self.canvas.create_rectangle(self.x, self.y, x, y, outline="grey", tag="select", width=3, dash=(8, 2))

    def release_2(self, e):
        if self.x !=e.x and self.y != e.y and not self.rmenu:
            self.rmenu = tk.Menu(None, tearoff=0, takefocus=0)
            self.rmenu.add_command(label="Fill Zone", command=lambda : self.fillZone(e), accelerator="F")
            self.rmenu.add_command(label="Clean Zone", command=lambda : self.cleanZone(e), accelerator="C")
            self.rmenu.add_separator()

            self.rmenu.add_command(label="Copy Zone", command=lambda : self.copyZone(e), accelerator="Shift-C")
            self.rmenu.add_command(label="Paste", command=lambda : self.pasteZone(e), accelerator="Shift-V")

            self.rmenu.add_separator()

            self.rmenu.add_command(label="Save Zone as PDF", command=lambda : self.saveZonePDF(e), accelerator="P")
            self.rmenu.add_command(label="Save Zone as PS", command=lambda : self.saveZonePS(e), accelerator="T")

            self.rmenu.add_separator()
            self.rmenu.add_command(label="Cancel", command=lambda : self.escape(e), accelerator="Escape")
            #self.rmenu.add_command(label="Copy", command=lambda :self.canvas.delete("select"))
            #self.rmenu.add_command(label="Cut", command=lambda :self.canvas.delete("select"))

            self.rmenu.bind("<Key>", lambda event: self.keyPressedAfterSelect(event, e))
            self.rmenu.bind("<Shift-KeyPress-V>", lambda event: self.pasteZone(e))
            self.rmenu.bind("<Shift-KeyPress-C>", lambda event: self.copyZone(e))

            if pm.system() == "Linux":
                self.rmenu.bind("<Escape>", self.escape)
                self.bind("<Escape>", self.escape)
            try:
                self.rmenu.tk_popup(e.x_root+2, e.y_root+2)
            finally:
                self.rmenu.grab_release()
                if pm.system() == "Windows":
                    self.canvas.delete("select")
                    self.rmenu = None


    def copyZone(self, e):
        x, y = e.x-e.x%10, e.y-e.y%10
        x = min(max(0, x), self.canvas.winfo_width())
        y = min(max(0, y), self.canvas.winfo_height())

        w, h = abs(self.x-x), abs(self.y-y)
        x, y = min(self.x, x), min(self.y, y)
        x = x // 10
        y = y // 10

        self.clipboard = [[self.gridContent[j+y][i+x] for j in range(h//10)] for i in range(w//10)]
        #print(self.clipboard)
        #print()
        self.escape(e)
        self.event_generate("<Escape>", when="tail")


    def pasteZone(self, e):
        if self.clipboard == None: 
            self.escape(e)
            return
        x, y = e.x-e.x%10, e.y-e.y%10
        x = min(max(0, x), self.canvas.winfo_width())
        y = min(max(0, y), self.canvas.winfo_height())

        xxx = x // 10
        yyy = y // 10
        for i in range(len(self.clipboard)):
            for j in range(len(self.clipboard[0])):
                self.gridContent[yyy+j][xxx+i] = self.clipboard[i][j]

                x = i*10 + xxx*10
                xx = x+10
                
                y = j*10 + yyy*10
                yy = y+10
                tagg = str(x) + "-" + str(y)
                #print(x, y)
                

                if self.clipboard[i][j]==1:
                    if self.shapeCells == "square":
                        self.canvas.create_rectangle(x+1, y+1, xx-1, yy-1, outline=self.colorCells,
												 fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "circle":
                        self.canvas.create_oval(x+1, y+1, xx-1, yy-1,
									outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "triangle":
                        self.canvas.create_polygon(x+5, y+1, xx-1, yy-1, x+1, yy-1, 
									outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                else:
                    self.canvas.delete(tagg)
									
        self.escape(e)
        self.event_generate("<Escape>", when="tail")

    def saveZonePDF(self, e):
        x, y = e.x-e.x%10, e.y-e.y%10
        x = min(max(0, x), self.canvas.winfo_width())
        y = min(max(0, y), self.canvas.winfo_height())

        w, h= abs(self.x-x), abs(self.y-y)
        x, y = min(self.x, x), min(self.y, y)
        self.escape(e)
        self.canvas.update()

        ftypes = [('PDF files', '.pdf')]
        fname = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".pdf",
                                             title="Save as PDF file", initialdir = "./PDFs/")
        if fname == "":
            return
        try:
            self.canvas.postscript(file="tmp.ps", colormode='color', rotate=True, pageheight=600, pagewidth=700,
                               x=x, y=y, width=w, height=h)


            if pm.system()=="Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                process = subprocess.Popen(["ps2pdf", "tmp.ps", fname], startupinfo=startupinfo)
            else:
                process = subprocess.Popen(["ps2pdf", "tmp.ps", fname])
            process.wait()
            os.remove("tmp.ps")
            
            mb.showinfo('Action completed', 'The PDF file has been generated successfully!')
        except Exception:
            mb.showerror("Error", "Somehting went wrong!")


    def saveZonePS(self, e):
        x, y = e.x-e.x%10, e.y-e.y%10
        x = min(max(0, x), self.canvas.winfo_width())
        y = min(max(0, y), self.canvas.winfo_height())

        w, h= abs(self.x-x), abs(self.y-y)
        x, y = min(self.x, x), min(self.y, y)
        self.escape(e)
        self.canvas.update()
        ftypes = [('PS files', '.ps')]
        fname = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".ps", title="Save as PS file",
                                initialdir = "./PSs/")
        if fname == "":
            return
        self.canvas.postscript(file=fname, colormode='color', rotate=True, pageheight=600, pagewidth=700,
                               x=x, y=y, width=w, height=h)
        mb.showinfo('Action completed', 'The PS file has been generated successfully!')

        


    def keyPressedAfterSelect(self, event, e):
        if event.char == "F" or event.char == "f":
            self.fillZone(e)
            self.event_generate("<Escape>", when="tail")
        elif event.char == "C" or event.char == "c":
            self.cleanZone(e)
            self.event_generate("<Escape>", when="tail")
        elif event.char == "P" or event.char == "p":
            self.saveZonePDF(e)
            self.event_generate("<Escape>", when="tail")
        elif event.char == "T" or event.char == "t":
            self.saveZonePS(e)
            self.event_generate("<Escape>", when="tail")

    def escape(self, e):
        self.canvas.delete("select")
        self.x=None
        self.y=None
        self.rmenu = None

    def cleanZone(self, e):
        x = max(0, e.x - e.x%10)
        x = min(x, self.canvas.winfo_width())
        y = max(0, e.y - e.y%10)
        y = min(y, self.canvas.winfo_height())

        x1, x2 = min(x, self.x), max(x, self.x)
        y1, y2 = min(y, self.y), max(y, self.y)
        for i in range(x1//10, x2//10):
            x = i*10
            xx = x+10
            for j in range(y1//10, y2//10):
                y = j*10
                yy = y+10               
                tagg = str(x) + "-" + str(y)
                self.canvas.delete(tagg)
                self.gridContent[j][i] = 0
        self.escape(e)


    def fillZone(self, e):
        x = max(0, e.x - e.x%10)
        x = min(x, self.canvas.winfo_width())
        y = max(0, e.y - e.y%10)
        y = min(y, self.canvas.winfo_height())

        x1, x2 = min(x, self.x), max(x, self.x)
        y1, y2 = min(y, self.y), max(y, self.y)

        for i in range(x1//10, x2//10):
            x = i*10
            xx = x+10
            for j in range(y1//10, y2//10):
                if self.gridContent[j][i] == 0:
                    self.gridContent[j][i] = 1
                    y = j*10
                    yy = y+10               
                    tagg = str(x) + "-" + str(y)
                    if self.shapeCells == "square":
                        self.canvas.create_rectangle(x+1, y+1, xx-1, yy-1, outline=self.colorCells,
                                                 fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "circle":
                        self.canvas.create_oval(x+1, y+1, xx-1, yy-1,
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "triangle":
                        self.canvas.create_polygon(x+5, y+1, xx-1, yy-1, x+1, yy-1, 
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)

        self.escape(e)



    def selectShape(self, shape=1, e=None):
        if shape==1: # Square
            if self.shapeCells == "square":
                 return
            self.shapeCells = "square"
            self.canvas.delete("cells")
            for i in range(len(self.gridContent)):
                for j in range(len(self.gridContent[0])):
                    if self.gridContent[i][j] == 1:
                        tagg = str(j*10) + "-" + str(i*10)
                        self.canvas.create_rectangle(j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1,
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)

        elif shape==2: # Triangle
            if self.shapeCells == "triangle":
                 return
            self.shapeCells = "triangle"
            self.canvas.delete("cells")
            for i in range(len(self.gridContent)):
                for j in range(len(self.gridContent[0])):
                    if self.gridContent[i][j] == 1:
                        tagg = str(j*10) + "-" + str(i*10)
                        self.canvas.create_polygon(j*10+1+4, i*10+1, (j+1)*10-1, (i+1)*10-1, j*10+1, (i+1)*10-1, 
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)


        elif shape==3: # Circle
            if self.shapeCells == "circle":
                 return
            self.shapeCells = "circle"

            self.canvas.delete("cells")
            for i in range(len(self.gridContent)):
                for j in range(len(self.gridContent[0])):
                    if self.gridContent[i][j] == 1:
                        tagg = str(j*10) + "-" + str(i*10)
                        self.canvas.create_oval(j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1,
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)


    def increaseSpeed(self, e=None):
        if self.speed.get() < 100:
            self.speed.set(self.speed.get()+1)

    def decreaseSpeed(self, e=None):
        if self.speed.get() > 1:
            self.speed.set(self.speed.get()-1)

    def init(self, e = None):
        if not self.inited:
            height = self.canvas.winfo_height()
            width = self.canvas.winfo_width()
            if height > 10: self.inited=True       
            for i in range(1, height//10):
                self.canvas.create_line(0, i*10, width, i*10, fill=self.colorGrid, tag="grid")
            for i in range(1, width//10):
                self.canvas.create_line(i*10, 0, i*10, height, fill=self.colorGrid, tag="grid")

            self.nbRows = height//10
            self.nbCols = width//10

            self.gridContent = [[0 for j in range(self.nbCols)] for i in range(self.nbRows)]


    def mouseMotion(self, event):
        x = event.x // 10
        y = event.y // 10
        if (x < self.nbCols and x >= 0 and y < self.nbRows and y >=0):
            self.tv.set("x = " + str(x) + ", y = " + str(y))

        
    def cleanGrid(self, e=None):
        self.canvas.delete("cells")
        self.gridContent = [[0 for j in range(self.nbCols)] for i in range(self.nbRows)]

    def fillGrid(self, e=None):
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        for i in range(0, width//10):
            x = i*10
            xx = x+10
            for j in range(0, height//10):
                if self.gridContent[j][i] == 0:
                    self.gridContent[j][i] = 1
                    y = j*10
                    yy = y+10
                    tagg = str(x) + "-" + str(y)


                    if self.shapeCells == "square":
                        self.canvas.create_rectangle(x+1, y+1, xx-1, yy-1, outline=self.colorCells,
                                                 fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "circle":
                        self.canvas.create_oval(x+1, y+1, xx-1, yy-1,
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "triangle":
                        self.canvas.create_polygon(x+5, y+1, xx-1, yy-1, x+1, yy-1, 
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)



    def savePDF(self, e=None):
        self.canvas.update()
        ftypes = [('PDF files', '.pdf')]
        fname = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".pdf",
                                             title="Save as PDF file", initialdir = "./PDFs/")

        if fname == "":
            return

        try:
            self.canvas.postscript(file="tmp.ps", colormode='color', rotate=True,
                                   pageheight=600, pagewidth=700)


            if pm.system()=="Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                process = subprocess.Popen(["ps2pdf", "tmp.ps", fname], startupinfo=startupinfo)
            else:
                process = subprocess.Popen(["ps2pdf", "tmp.ps", fname])
            process.wait()
            os.remove("tmp.ps")
            
            mb.showinfo('Action completed', 'The PDF file has been generated successfully!')
        except Exception:
            mb.showerror("Error", "Somehting went wrong!")

        
    def savePS(self, e=None):
        self.canvas.update()
        ftypes = [('PS files', '.ps')]
        fname = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".ps", title="Save as PS file",
                                initialdir = "./PSs/")
        if fname == "":
            return
        self.canvas.postscript(file=fname, colormode='color', rotate=True, pageheight=600, pagewidth=700)
        mb.showinfo('Action completed', 'The PS file has been generated successfully!')

    def saveJPG(self, e=None):
        ftypes = [('JPEG files', '.jpg')]
        fname = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".jpg", title="Save as JPEG image",
                                initialdir = "./JPEGs/")
        if fname == "":
            return
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        image1 = Image.new("RGB", (width, height), self.canvas["bg"])
        draw = ImageDraw.Draw(image1)

        ## Draw grid lines
        for i in range(1, height//10):
            draw.line([0, i*10, width, i*10], self.colorGrid)
        for i in range(1, width//10):
            draw.line([i*10, 0, i*10, height], self.colorGrid)

        for i in range(len(self.gridContent)):
            for j in range(len(self.gridContent[0])):
                if self.gridContent[i][j] == 1:
                    if self.shapeCells == "square":
                        draw.rectangle([j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1],
                            fill=self.colorCells, outline=self.colorCells)
                    elif self.shapeCells == "circle":
                        draw.ellipse([j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1],
                            fill=self.colorCells, outline=self.colorCells)
                    elif self.shapeCells == "triangle":
                        draw.polygon([j*10+1+4, i*10+1, (j+1)*10-1, (i+1)*10-1, j*10+1, (i+1)*10-1],
                            outline=self.colorCells, fill=self.colorCells)

        image1.save(fname)
        mb.showinfo('Action completed', 'The JPEG image has been generated successfully!')


    def saveGIF(self, e=None):
        ftypes = [('GIF files', '.gif')]
        fname = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".gif", title="Save as GIF image",
                                initialdir = "./GIFs/")
        if fname == "":
            return
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        image1 = Image.new("RGB", (width, height), self.canvas["bg"])
        draw = ImageDraw.Draw(image1)

        ## Draw grid lines
        for i in range(1, height//10):
            draw.line([0, i*10, width, i*10], self.colorGrid)
        for i in range(1, width//10):
            draw.line([i*10, 0, i*10, height], self.colorGrid)

        for i in range(len(self.gridContent)):
            for j in range(len(self.gridContent[0])):
                if self.gridContent[i][j] == 1:
                    if self.shapeCells == "square":
                        draw.rectangle([j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1],
                            fill=self.colorCells, outline=self.colorCells)
                    elif self.shapeCells == "circle":
                        draw.ellipse([j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1],
                            fill=self.colorCells, outline=self.colorCells)
                    elif self.shapeCells == "triangle":
                        draw.polygon([j*10+1+4, i*10+1, (j+1)*10-1, (i+1)*10-1, j*10+1, (i+1)*10-1],
                            outline=self.colorCells, fill=self.colorCells)

        image1.save(fname)
        mb.showinfo('Action completed', 'The GIF image has been generated successfully!')



    def saveConfig(self, e=None):
        fname = filedialog.asksaveasfilename(filetypes=[('CSV files', '.csv')], defaultextension=".csv",
                                             title="Save configuration as CSV file", initialdir = "./Saved config/")
        if fname =="" or not fname:
            return

        #print(fname)
        with open(fname, "w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerows(self.gridContent)
        mb.showinfo('Action completed', 'The configuration has been successfully saved!')

    def loadConfig(self, e=None):
        fname = filedialog.askopenfilename(filetypes=[('CSV files', '.csv')], defaultextension=".csv",
                                             title="Save configuration as CSV file", initialdir = "./Saved config/")
        if fname=="" or not fname:
            return
        with open(fname, "r") as f:
            reader = csv.reader(f, delimiter=",")
            l = list(reader)
            fileContent = [[int(ee) for ee in e] for e in l]
        self.gridContent =  [[0 for j in range(self.nbCols)] for i in range(self.nbRows)]

        self.canvas.delete("cells")
        for i in range(min(len(self.gridContent), len(fileContent))):
            for j in range(min(len(self.gridContent[0]), len(fileContent[0]))):
                if fileContent[i][j] == 1:
                    self.gridContent[i][j] = 1
                    tagg = str(j*10) + "-" + str(i*10)

                    if self.shapeCells == "square":
                        self.canvas.create_rectangle(j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1,
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "circle":
                        self.canvas.create_oval(j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1,
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "triangle":
                        self.canvas.create_polygon(j*10+1+4, i*10+1, (j+1)*10-1, (i+1)*10-1, j*10+1, (i+1)*10-1, 
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
            

    def click1_canvas(self, e):
        x = e.x - e.x%10
        y = e.y - e.y%10
        if (x//10 < self.nbCols and x//10 >= 0 and y//10 < self.nbRows and y//10 >=0):
            if self.gridContent[y//10][x//10] == 0:
                self.gridContent[y//10][x//10] = 1
                xx = x+10
                yy = y+10
                tagg = str(x) + "-" + str(y)

                if self.shapeCells == "square":
                    self.canvas.create_rectangle(x+1, y+1, xx-1, yy-1,
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                elif self.shapeCells == "circle":
                    self.canvas.create_oval(x+1, y+1, xx-1, yy-1,
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                elif self.shapeCells == "triangle":
                    self.canvas.create_polygon(x+1+4, y+1, xx-1, yy-1, xx-9, yy-1,
                                    outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)

            self.mouseMotion(e)
            

    def click2_canvas(self, e):
        x = e.x - e.x%10
        y = e.y - e.y%10
        if (x//10 < self.nbCols and x//10 >= 0 and y//10 < self.nbRows and y//10 >=0):
            tagg = str(x) + "-" + str(y)
            self.canvas.delete(tagg)
            self.mouseMotion(e)
            self.gridContent[y//10][x//10] = 0


    def start(self, e=None):
        with th.Lock():
            if not self.simStarted:
                self.simStarted = True
                self.startStop['text'] = "Stop"
                self.after(100 - self.speed.get() + 1, self.task)
            else:
                self.simStarted = False
                self.startStop['text'] = "Start"
        
        

    def stop(self):
        with th.Lock():
            if self.simStarted:
                self.simStarted = False
                self.startStop['text'] = "Start"


    def keyPressed(self, e=None):
        if e.char == "n" or e.char == "N":
            self.step()

    def step(self, e=None):
        self.gridContent = sim.nextGen(self.gridContent)
        self.canvas.delete("cells")
        for i in range(len(self.gridContent)):
            for j in range(len(self.gridContent[0])):
                if self.gridContent[i][j] == 1:
                    tagg = str(j*10) + "-" + str(i*10)

                    if self.shapeCells == "square":
                        self.canvas.create_rectangle(j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1,
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "circle":
                        self.canvas.create_oval(j*10+1, i*10+1, (j+1)*10-1, (i+1)*10-1,
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)
                    elif self.shapeCells == "triangle":
                        self.canvas.create_polygon(j*10+1+4, i*10+1, (j+1)*10-1, (i+1)*10-1, j*10+1, (i+1)*10-1, 
                                outline=self.colorCells, fill=self.colorCells, tag="cells " + tagg)

    def exit(self, e=None):
        self.stop()
        self.destroy()

    def task(self):
        with th.Lock():
            if self.simStarted:
                self.step()
                self.after(100 - self.speed.get() + 1, self.task)
        

    def about(self, e=None):
        mb.showinfo('No', 'Quit has been cancelled')

    def chooseColorGrid(self, e=None):
        res = askcolor(color=self.colorGrid, title = "Grid Color Chooser")
        if res[1] != None:
            self.colorGrid = res[1]
            l = self.canvas.find_withtag("grid")
            for e in l:
                self.canvas.itemconfig(e, fill=res[1]) # change color

    def chooseColorCells(self, e=None):
        res = askcolor(color=self.colorCells, title = "Cells Color Chooser")
        if res[1] != None:
            self.colorCells = res[1]
            l = self.canvas.find_withtag("cells")
            for e in l:
                self.canvas.itemconfig(e, fill=res[1], outline=res[1]) # change color

    def chooseColorBG(self, e=None):
        res = askcolor(color=self.canvas['bg'], title = "Cells Color Chooser")
        if res[1] != None:
            self.canvas.configure(bg=res[1])

p = window()
p.bind("<Visibility>", p.init)
p.mainloop()
