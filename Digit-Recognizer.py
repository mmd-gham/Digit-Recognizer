from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser, filedialog, messagebox
import PIL.ImageGrab as ImageGrab
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from csv import writer



# x99=""
class Draw():
    def __init__(self, root):

        # Defining title and Size of the Tkinter Window GUI
        self.root = root
        self.root.state("zoomed")  # maximize
        self.root.title("Digit Recognizer")
        #         self.root.geometry("810x530")
        self.root.configure(background="white")
        self.root.resizable(False, False)
        #         self.root.resizable(0,0)

        # variables for pointer and Eraser
        self.pointer = "white"
        self.erase = "white"

        # Widgets for Tkinter Window

        # Defining a label
        self.label = Label(self.root, text= "Digit Recognition Application In Python", fg= "orange", bd = 10, width=50,
                           relief=RAISED)
        self.label.pack()

        # Defining a background color for the Canvas
        self.background = Canvas(self.root, bg='black', bd=5, relief=GROOVE, height=470, width=680)
        self.background.pack(pady=15)

        self.result1 = Label(self.root, text="")
        self.result1.pack(pady=5)

        # enter real digit
        self.ent_real = Entry(self.root, width=11, bg="pink")
        self.ent_real.pack(pady=5)

        # start project button
        self.start_btn = Button(self.root, text="START", bd=4, bg='gold', command=self.start, width=9, relief=RIDGE)
        self.start_btn.pack(pady=5)

        # Save Button for saving the image in local computer after prediction
        self.save_btn = Button(self.root, text="PREDICT", state="disabled", bd=4, bg='gold', command=self.predict,
                               width=9, relief=RIDGE)
        self.save_btn.pack(pady=5)

        # save correct answer
        self.answer_btn = Button(self.root, text="Save ans", state="disabled", bd=4, bg='gold', command=self.save_ans,
                                 width=9, relief=RIDGE)
        self.answer_btn.pack(pady=5)

        # Reset Button to clear the entire screen
        self.clear_screen = Button(self.root, text="Clear Screen", bd=4, bg='white',command=lambda:
                                   [self.background.delete('all'),self.save_btn.configure(state="active")],
                                   width=9, relief=RIDGE)
        self.clear_screen.pack(pady=5)

        # Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        self.background.create_oval(x1, y1, x2, y2, fill=self.pointer, outline=self.pointer, width=40)

    def select_color(self, col):
        pass

    def eraser(self):
        pass

    def canvas_color(self):
        pass

    def start(self):
        ################################## training #########################################
        #        digits=cv2.imread("digits.png",cv2.IMREAD_GRAYSCALE)
        #        rows=np.vsplit(digits,50)
        #        cells=[]
        #        cells2=[]
        #        for row in rows :
        #            row_cells=np.hsplit(row,100)
        #            for cell in row_cells:
        #                cells.append(cell)
        #                #all in one column
        #                cells2.append(cell.flatten())
        #
        #        #cells2 is a list and in openCV we need numpy array because it is faster than list
        #        cells2=np.array(cells2,dtype=np.float32)
        #        n=np.arange(10)
        #        targets=np.repeat(n,500)
        #
        ##        self.knn=KNeighborsClassifier(n_neighbors=6,metric='minkowski')
        ##        self.knn.fit(cells2,targets)
        #
        #        self.knn=cv2.ml.KNearest_create()
        #        self.knn.train(cells2,cv2.ml.ROW_SAMPLE,targets)

        ########################## train from csv ####################################
        self.result1.configure(text="Wait...", fg="red")
        self.start_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.answer_btn.configure(state="disabled")
        self.root.update()

        data = np.genfromtxt('mydigits.csv', delimiter=',', dtype="float32")
        targets = np.genfromtxt('mytargets.csv', delimiter=',', dtype="int32")

        self.knn = cv2.ml.KNearest_create()
        self.knn.train(data, cv2.ml.ROW_SAMPLE, targets)

        self.result1.configure(text="Ready", fg="green")
        self.start_btn.configure(state="disabled")
        self.save_btn.configure(state="active")
    #####################################################################################

    def predict(self):
        ############################## save image ################################
        try:
            # self.background update()
            #            file_ss =filedialog.asksaveasfilename(defaultextension='jpg')
            # print(file_ss)
            x = self.root.winfo_rootx() + self.background.winfo_x()
            # print(x, self.background.winfo_x())
            y = self.root.winfo_rooty() + self.background.winfo_y()
            # print(y)

            x1 = x + self.background.winfo_width()
            # print(x1)
            y1 = y + self.background.winfo_height()
            # print(y1)
            ImageGrab.grab().crop((x, y, x1, y1)).save("test.png")
        #   for this to work better make sure the resolution of of system is on 100%
        #            messagebox.showinfo('Screenshot Successfully Saved as' + str(file_ss))

        except:
            print("Error in saving the screenshot")

        ######################################### predict ##############################
        my_digit = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)
        my_digit = cv2.resize(my_digit, (20, 20))
        ####################
        self.my_test_flat = []
        self.my_test_flat.append(my_digit.flatten())
        self.my_test_flat = np.array(self.my_test_flat, dtype=np.float32)

        #        my_predict = self.knn.predict(my_test_flat)
        ret, result, neighbours, dist = self.knn.findNearest(self.my_test_flat, k=7)
        #        print(result)
        #        global x99
        self.test = my_digit.flatten()
        self.test = np.array(self.test, dtype=np.float32)

        self.result1.configure(text=result[0])
        self.neighbours = neighbours

        ########################## checking if the drawing is a digit or not ##########################

        max={}
        for digits in self.neighbours:
            for digit in digits:
                if digit in max:
                    max[digit]+= 1
                else:
                    max[digit] = 1
        self.maximum=0
        for digit in max:
            if max[digit]>self.maximum:
                self.maximum = max[digit]
        if (self.maximum < 5) :
            self.result1.configure(text="The drawing is not good. Please clear the screen and draw another number",
                                   fg="red")
            self.save_btn.configure(state="disabled")
            return
        if (self.maximum == 7):
            self.save()


        #####################
        #        cv2.imshow("digits",my_digit)
        #        cv2.waitKey(0)
        #        cv2.destroyAllWindows()
        #####################

        self.start_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.answer_btn.configure(state="active")

    def save_ans(self):
        self.answer = self.ent_real.get()
        if (self.answer == ""):
            self.result1.configure(text="Fill the box", fg="red")
            return
        elif (len(self.answer)>1):
            self.result1.configure(text="Enter only one figure", fg="red")
            return
        try:
            self.answer = int(self.answer)
        except:
            self.result1.configure(text="Enter a number", fg="red")
            return
        self.save()

    def save(self) :
        self.answer = self.ent_real.get()
        self.result1.configure(text="wait...", fg="red")
        self.start_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.answer_btn.configure(state="disabled")
        self.root.update()

        with open('mydigits.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(self.test)

        with open('mytargets.csv', 'a') as f:
            writer_object = writer(f)
            writer_object.writerow([self.answer])

        self.result1.configure(text="Saved", fg="green")
        self.ent_real.delete(0, END)
        self.start_btn.configure(state="disabled")
        self.answer_btn.configure(state="disabled")



###############################################################################################


if __name__ == "__main__":
    root = Tk()
    p = Draw(root)
    root.mainloop()