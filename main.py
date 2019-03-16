import sys
from math import *
from tkinter import *
from tkinter import messagebox
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("seaborn-darkgrid")
import csv
import os

if sys.version_info[0] < 3:
    from Tkinter import *
    from Tkinter.font import Font
else:
    from tkinter import *
    from tkinter.font import Font
    
print("Libraries has been imported.")
print("\n")
print("\t==================================================================")
print("\t|      Lead Programmer:\t\t\tEugene B. Oca            |")
print("\t|      Design specialist:\t\tEdith A. Castillo        |")
print("\t|      Documentation specialist:\tBeatrice A. Abesamis     |")
print("\t==================================================================\n")
root = Tk()
root.wm_title("Numerical Methods (Bisection Method)")
root.overrideredirect(1)

# COLOR THEME
main_bg = "#FFFFFF"
#main_bg = "#FFFF80"
# END COLOR THEME

# Window Properties
k = (root.winfo_screenwidth() / 2) - (1000 / 2)
root.config(height=649, width=1000, bg=main_bg)
root.geometry("1000x649+{}+50".format(int(k)))
o_font = Font(family="Segoe UI", size=11)

console = Text(root, width=70, height=22, font=o_font, bg=main_bg, relief=FLAT)
console.place(x=10, y=201)

lbl_bisection = Label(root, text="BISECTION METHOD", bg="#FFFF00", font="-weight bold")
lbl_bisection.place(x=10, y=10)

# Graph Properties
matplotlib.get_backend()
f = Figure(figsize=(5, 7.6), dpi=80)
a = f.add_subplot(211)
b = f.add_subplot(212)
f.subplots_adjust(hspace=0.45, right=0.95, left=0.18)
f_plot = Figure(figsize=(4,2), dpi=80)
orig = f_plot.add_subplot(111)
f_plot.subplots_adjust(hspace=0.45, right=0.95, left=0.45, bottom=0.3)

def reset_figure():
    
    a.set_title("F(XR)")
    a.set_ylabel("F(XR)")
    a.set_xlabel("Iteration")
    
    b.set_title("Approximate Roots")
    b.set_ylabel("Roots")
    b.set_xlabel("Iteration")

    orig.set_title("Graph of Function")
    orig.set_ylabel("Y")
    orig.set_xlabel("X")

reset_figure()
graph = FigureCanvasTkAgg(f, root)
graph.draw()
graph.get_tk_widget().place(x=200, y=120)
graph._tkcanvas.place(x=600, y=-20)
graph_f = FigureCanvasTkAgg(f_plot, root)
graph_f.draw()
graph_f.get_tk_widget().place(x=300, y=30)
graph._tkcanvas.place(x=600, y=-20)

# END Add Plot point

def update_plot(z, Xr_arr,Fx_arr, error_arr):
    a.clear()
    b.clear()
    a.plot(z, Fx_arr)
    b.plot(z, Xr_arr)
    reset_figure()
    graph.draw()
    graph_f.draw()
    
lbl_root = Label(root, text="Approximate Root: 2.99", font=o_font, bg=main_bg, fg=main_bg)
lbl_root.place(x=670,y=580)

# Analysis
def analyze():
    if txt_equation.get() == "" or txt_lowerLimit.get() == "" or txt_upperLimit.get() == "" or txt_error.get() == "":
        messagebox.showinfo("Information", "Please provide all required fields.")
    else:
        try:
            print("\n\nAnalyzing....\n\n")
            error = 100.00;
            Xp = 0.00; 
            x = 0.00;
            i = 0;
            low = eval(txt_lowerLimit.get())*1.00;
            high = eval(txt_upperLimit.get())*1.00;

            #Limits Restriction
            d = str(txt_equation.get()).replace("^", "**").replace("x", "h").replace("e","2.718281828")
            h = low
            lo = eval(d)
            h = high
            hi = eval(d)
            
            if (lo < 0 and hi < 0) or (lo > 0 and hi > 0) or lo == 0 or hi == 0:
                messagebox.showinfo("Information", "F(x) should be of different signs.")
                return
            #END Limits Restriction
            
            if abs(low) > 50:
                messagebox.showinfo("Information", "Your lower limit exceeds the value of 50, please choose a lower value.")
                return

            if abs(high) > 50:
                messagebox.showinfo("Information", "Your upper limit exceeds the value of 50, please choose a lower value.")
                return
            console.delete('1.0', END)
            print("Initial Conditions: Low =", low, " High =", high);
            print("Equation: f(x) =", txt_equation.get(), "\n")
            Xr_arr = []
            Fx_arr = []
            error_arr = []
            z = []

            try:
            	# Offset Graph Axis
                offset_graph = 2*abs(low-high);
                if(offset_graph > 1):
                    orig.clear()
                    ys = []
                    r = range(int(low-offset_graph), int(high+offset_graph), 1);
                    for x in r:
                        eq = str(txt_equation.get()).replace("^", "**").replace("e","2.718281828")
                        ys.append(eval(eq))
                    orig.plot(r, ys)
                else:
                    print("Graph of function is too small.")
                x = 0.00
            except:
                messagebox.showinfo("Information", "Graph of function error.")

            # Instantiate csv file
            file = open('plot.csv', 'w', newline='')
            fieldnames = ['I', 'XL', 'XU', 'XR', 'F(XR)', 'ERROR']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            # Analysis Loop
            while(error>eval(txt_error.get())):
                Xp = x;
                x = (low+high)/2;
                eq = str(txt_equation.get()).replace("^", "**")
                Fx = eval(eq);
                error = abs((x-Xp)/x);
                if(Fx>0):
                    print("{}\t{}\t{}\t{}\t{}\t{}".format(i, "%0.6f" % low, "%0.6f" % high, "%0.6f" % x, "%0.6f" % float(Fx), "%0.6f" % error));
                    console.insert(END, str(i) + "\t" + str("%0.6f" % low) + "\t  " + "%0.6f" % high + "\t  " + "%0.6f" % x + "\t\t" + "%0.6f" % float(Fx) + "\t\t" + "%0.6f" % error + "\n")
                    z.append(i)
                    Fx_arr.append(float(Fx))
                    Xr_arr.append(float(x))
                    error_arr.append(float(error))
                    writer.writerow({'I': i, 'XL': low, 'XU': high, 'XR': x, 'F(XR)': Fx, 'ERROR': error})
                    high = x;
                else:
                    print("{}\t{}\t{}\t{}\t{}\t{}".format(i, "%0.6f" % low, "%0.6f" % high, "%0.6f" % x, "%0.6f" % float(Fx), "%0.6f" % error));
                    console.insert(END, str(i) + "\t" + str("%0.6f" % low) + "\t  " + "%0.6f" % high + "\t  " + "%0.6f" % x + "\t\t" + "%0.6f" % float(Fx) + "\t\t" + "%0.6f" % error + "\n")
                    z.append(i)
                    Fx_arr.append(float(Fx))
                    Xr_arr.append(float(x))
                    error_arr.append(float(error))
                    writer.writerow({'I': i, 'XL': low, 'XU': high, 'XR': x, 'F(XR)': Fx, 'ERROR': error})
                    low = x;
                i = i+1;
            update_plot(z, Xr_arr,Fx_arr, error_arr)
            lbl_root.config(text = "Approximate Root:\t{0}".format(x), fg="#000000")
            messagebox.showinfo("Information", "Graph computing is done and saved.")
            print("\n\nAnalysis done.\n\n")
            file.close()
        except Exception as error:
            messagebox.showinfo("Information", "Limits or Equations might not be possible. Please try again. Error: "+str(error))
            
# END Analysis

# Main

def terminate():
    result = messagebox.askquestion("Exit", "Are You Sure?", icon='question')
    if result == 'yes':
        quit()
    else:
        return

# GUI Codes
menubar = Menu(root)
menubar.add_command(label="Quit", command=terminate)
root.config(menu=menubar)
offset_y = 40
offset_x = 12
lbl_equation = Label(text="Equation:", font=o_font, bg=main_bg)
lbl_equation.place(x=10, y=10+offset_y)

txt_equation = Entry(font=o_font, relief=GROOVE, bg="#5EAEFF")
txt_equation.place(x=85+offset_x, y=10+offset_y)

lbl_lowerLimit = Label(text="Lower Limit:", font=o_font, bg=main_bg)
lbl_lowerLimit.place(x=10, y=34+offset_y)

txt_lowerLimit = Entry(font=o_font, relief=GROOVE, bg="#5EAEFF")
txt_lowerLimit.place(x=85+offset_x, y=34+offset_y)

lbl_upperLimit = Label(text="Upper Limit:", font=o_font, bg=main_bg)
lbl_upperLimit.place(x=10, y=58+offset_y)

txt_upperLimit = Entry(font=o_font, relief=GROOVE, bg="#5EAEFF")
txt_upperLimit.place(x=85+offset_x, y=58+offset_y)

lbl_error = Label(text="Error:", font=o_font, bg=main_bg)
lbl_error.place(x=10, y=82+offset_y)

txt_error = Entry(font=o_font, relief=GROOVE, bg="#5EAEFF")
txt_error.place(x=85+offset_x, y=82+offset_y)

cmd_analyze = Button(text="Analyze", command=analyze, font=o_font, width=13, height=4, relief=FLAT, bg="#FCFF6A")
cmd_analyze.place(x=270, y=50)


neg_offset = -49
lbl_head = Label(root, text="i", bg=main_bg);
lbl_head.place(x=10, y=220+neg_offset);

lbl_head = Label(root, text="X", bg=main_bg);
lbl_head.place(x=100, y=220+neg_offset);
lbl_head = Label(root, text="L", bg=main_bg);
lbl_head.place(x=110, y=225+neg_offset);

lbl_head = Label(root, text="X", bg=main_bg);
lbl_head.place(x=165, y=220+neg_offset);
lbl_head = Label(root, text="U", bg=main_bg);
lbl_head.place(x=175, y=225+neg_offset);

lbl_head = Label(root, text="X", bg=main_bg);
lbl_head.place(x=235, y=220+neg_offset);
lbl_head = Label(root, text="R", bg=main_bg);
lbl_head.place(x=245, y=225+neg_offset);

lbl_head = Label(root, text="F( X     )", bg=main_bg);
lbl_head.place(x=345, y=220+neg_offset);
lbl_head = Label(root, text="R", bg=main_bg);
lbl_head.place(x=370, y=225+neg_offset);

lbl_head = Label(root, text="ERROR", bg=main_bg);
lbl_head.place(x=465, y=220+neg_offset);
# END Main

root.mainloop()
