from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
import cv2
import numpy as np

class Application(Frame):
    """A classic GUI program for writing classes"""
    def __init__(self, master=None):
        super().__init__(master)            # super()代表的是父类定义，而不是父类对象
        self.master = master
        self.pack()

        self.createWidget()

    def createWidget(self):

        # Components of row 1
        self.l1 = Label(self, text="Cross-sectional image of end A", pady=20)
        self.l1.grid(row=0, column=1)

        v1 = StringVar()
        v2 = StringVar()

        def read_file_name_1():
            f = askopenfilename(title="Select image file (English path)", initialdir="c:", filetype=[("JPG", "jpg"), ("PNG", ".png")])
            v1.set(f)
            self.w1.delete('1.0', 'end')

        def read_file_name_2():
            f = askopenfilename(title="Select image file (English path)", initialdir="c:", filetype=[("JPG", "jpg"), ("PNG", ".png")])
            v2.set(f)

        self.btn1 = Button(self, text="Select file", command=read_file_name_1)
        self.btn1.grid(row=0, column=2)

        self.t1 = Entry(self, textvariable=v1, width=20)
        self.t1.grid(row=0, column=0)

        # Components of row 2
        self.exist = IntVar()
        self.c2 = Checkbutton(self, text="Only one end of the section", variable=self.exist, onvalue=1, offvalue=0, pady=10)
        self.c2.grid(row=1, column=1)

        # Check whether to select the second section
        def judge_workable():
            if self.exist.get() == 1:
                self.btn2["state"] = DISABLED
                self.btn_con_b["state"] = DISABLED
            elif self.exist.get() == 0:
                self.btn2["state"] = ACTIVE
                self.btn_con_b["state"] = ACTIVE
            print(self.exist.get())

        self.btn3 = Button(self, text="Confirm", command=judge_workable)
        self.btn3.grid(row=1, column=2)

        # Components of row 3
        self.t2 = Entry(self,textvariable=v2 , width=20)
        self.t2.grid(row=2, column=0)

        self.l2 = Label(self, text="Cross-sectional image of end A", pady=20)
        self.l2.grid(row=2, column=1)

        self.btn2 = Button(self, text="Select file", command=read_file_name_2)
        self.btn2.grid(row=2, column=2)

        # Components of row 4,5
        thresh_a = StringVar()
        thresh_a.set(245)
        thresh_b = StringVar()
        thresh_b.set(245)

        self.entry1_a = Entry(self, textvariable=thresh_a)
        self.entry1_a.grid(row=3, column=0)

        def thresh_confirm_A():
            alpha = "The A-end cross-sectional area identification threshold has been identified as: " + str(thresh_a.get())
            messagebox.showinfo("Threshold Confirmation", alpha)

        self.btn_con_a = Button(self, command=thresh_confirm_A, text="Confirm")
        self.btn_con_a.grid(row=3, column=2)

        self.l3_a = Label(self, text="A-end cross-section recognition color threshold\n(default to 245)", pady=20)
        self.l3_a.grid(row=3, column=1)

        self.entry1_b = Entry(self, textvariable=thresh_b)
        self.entry1_b.grid(row=4, column=0)

        def thresh_confirm_B():
            alpha = "The B-end cross-sectional area identification threshold has been identified as: " + str(thresh_a.get())
            messagebox.showinfo("Threshold Confirmation", alpha)

        self.btn_con_b = Button(self, command=thresh_confirm_B, text="Confirm")
        self.btn_con_b.grid(row=4, column=2)

        self.l3_b = Label(self, text="B-end cross-section recognition color threshold\n(default to 245)", pady=20)
        self.l3_b.grid(row=4, column=1)


        # Text Box
        self.w1 = Text(self, width=60, height=10)
        self.w1.grid(row=7, column=0, columnspan=4)

        # Components of row 6
            # Cross-sectional area calculation codes
        def sec_area_calc():
            self.w1.delete('1.0', 'end')
            if self.exist.get() == 0:
                sec_A = str(v1.get())
                sec_B = str(v2.get())
                th_a = int(str(thresh_a.get()))
                th_b = int(str(thresh_b.get()))

                img = cv2.imread(sec_A)  # read image
                img2 = cv2.imread(sec_B)
                imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                imgray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                # Calculate A-section pixel points
                ret_a, thresh_a1 = cv2.threshold(imgray, th_a, 255, cv2.THRESH_BINARY_INV)
                section_area = cv2.countNonZero(thresh_a1)

                # Calculate B-section pixel points
                ret_a2, thresh_a2 = cv2.threshold(imgray2, th_b, 255, cv2.THRESH_BINARY_INV)
                section_area2 = cv2.countNonZero(thresh_a2)

                # Average cross-sectional area calculation
                section_area_av = (section_area + section_area2) / 2
                real_area = ((25.4 / 600) ** 2) * section_area_av

                # Image Recognition Monitoring
                cv2.namedWindow('sec_A', 0)
                cv2.resizeWindow('sec_A', 700, 700)
                cv2.namedWindow('sec_B', 0)
                cv2.resizeWindow('sec_B', 700, 700)

                cv2.imshow("sec_A", thresh_a1)
                cv2.imshow("sec_B", thresh_a2)
                cv2.waitKey(0)

                cv2.destroyAllWindows()

                text_1 = "A-end cross-sectional area: " + str(((25.4 / 600) ** 2) * section_area) + "\n\n" + "B-end cross-sectional area: " + str(((25.4 / 600) ** 2) * section_area2) + "\n\n"
                self.w1.insert(1.0, text_1)
                # self.w1.insert(2.0,"")
                # print(real_area)
            elif self.exist.get() == 1:
                sec_A = str(v1.get())
                th_a = int(str(thresh_a.get()))

                img = cv2.imread(sec_A)  # read image
                imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Calculate A-section pixel points
                ret_a, thresh_a1 = cv2.threshold(imgray, th_a, 255, cv2.THRESH_BINARY_INV)
                section_area = cv2.countNonZero(thresh_a1)

                # Image Recognition Monitoring
                cv2.namedWindow('sec_A', 0)
                cv2.resizeWindow('sec_A', 700, 700)

                cv2.imshow("sec_A", thresh_a1)
                cv2.waitKey(0)

                cv2.destroyAllWindows()

                # print(section_area)
                # print(section_area2)
                # print(section_area_av)
                text_1 = "A-end cross-sectional area: " + str(((25.4 / 600) ** 2) * section_area) + "\n\n"
                self.w1.insert(1.0, text_1)

        self.l4 = Label(self, text="Click to calculate the cross-sectional area", pady=10)
        self.l4.grid(row=5, column=1)

        self.btn3 = Button(self, command=sec_area_calc, text="Click here")
        self.btn3.grid(row=5, column=2)

        # Components of row 7
            # Identification of the vascular bundle codes
        def fib_rate_calc():
            # A-end cross section
            sec_A = str(v1.get())
            sec_B = str(v2.get())
            th_a = int(str(thresh_a.get()))
            th_b = int(str(thresh_b.get()))

            if self.exist.get() == 0:
                img = cv2.imread(sec_A)
                imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                ret, thresh_1 = cv2.threshold(imgray, th_a, 255, cv2.THRESH_BINARY_INV)

                contours, hierarchy = cv2.findContours(thresh_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                areas = list()
                for i, cnt in enumerate(contours):
                    areas.append((i, cv2.contourArea(cnt)))  # Area size
                a2 = sorted(areas, key=lambda d: d[1], reverse=True)  # Sorted by size, from largest to smallest
                max_c_area = a2[0][0]  # Select the maximum profile

                cnt = contours[max_c_area]
                rect = cv2.minAreaRect(cnt)  # Minimum external rectangle
                box = np.int0(cv2.boxPoints(rect))  # The four corner points of the rectangle are rounded
                cv2.drawContours(img, [box], 0, (255, 0, 0), 2)

                size = rect[1]
                size = tuple(map(int, size))
                center = rect[0]
                width = img.shape[1]
                height = img.shape[0]
                angle = rect[2]

                # Judgment formula for always keeping the rectangle flat
                if rect[1][0] <= rect[1][1]:
                    angle = 90 + angle
                    beta = rect[1][1]
                    alpha = rect[1][0]
                    size = (beta, alpha)
                    size = tuple(map(int, size))

                M = cv2.getRotationMatrix2D(center, angle, 1)
                img_rot = cv2.warpAffine(img, M, (width, height))
                img_crop = cv2.getRectSubPix(img_rot, size, center)  # Intercepting a rectangular box in a rotated image

                ROI = cv2.selectROI('1', img_crop, showCrosshair=1)  # Mouse interaction to select ROI
                x, y, w, h = ROI
                img_fiber_area = img_crop[y:y + h, x:x + w]

                areagray = cv2.cvtColor(img_fiber_area, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(areagray, (5, 5), 0)
                ret3, th2 = cv2.threshold(areagray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                img_area = areagray.size
                fiber_area = cv2.countNonZero(th2)
                a = str(fiber_area / img_area) + '\t'

                cv2.imshow('sec_A', th2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                # B-end cross section
                img2 = cv2.imread(sec_B)
                imgray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                ret, thresh_2 = cv2.threshold(imgray2, th_b, 255, cv2.THRESH_BINARY_INV)

                contours2, hierarchy = cv2.findContours(thresh_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                areas2 = list()
                for i, cnt2 in enumerate(contours2):
                    areas2.append((i, cv2.contourArea(cnt2)))  # Area size
                a2 = sorted(areas2, key=lambda d: d[1], reverse=True)  # Sorted by size, from largest to smallest
                max_c_area2 = a2[0][0]  # Select the maximum profile

                cnt2 = contours2[max_c_area2]
                rect2 = cv2.minAreaRect(cnt2)  # Minimum external rectangle
                box2 = np.int0(cv2.boxPoints(rect2))  # The four corner points of the rectangle are rounded
                cv2.drawContours(img2, [box2], 0, (255, 0, 0), 2)

                size2 = rect2[1]
                size2 = tuple(map(int, size2))
                center2 = rect2[0]
                width2 = img2.shape[1]
                height2 = img2.shape[0]
                angle2 = rect2[2]

                # Judgment formula for always keeping the rectangle flat
                if rect2[1][0] <= rect2[1][1]:
                    angle2 = 90 + angle2
                    beta2 = rect2[1][1]
                    alpha2 = rect2[1][0]
                    size2 = (beta2, alpha2)
                    size2 = tuple(map(int, size2))

                M2 = cv2.getRotationMatrix2D(center2, angle2, 1)
                img_rot2 = cv2.warpAffine(img2, M2, (width2, height2))
                img_crop2 = cv2.getRectSubPix(img_rot2, size2, center2)  # Intercepting a rectangular box in a rotated image

                ROI2 = cv2.selectROI('1', img_crop2, showCrosshair=1)  # Mouse interaction to select ROI
                x2, y2, w2, h2 = ROI2
                img_fiber_area2 = img_crop2[y2:y2 + h2, x2:x2 + w2]

                areagray2 = cv2.cvtColor(img_fiber_area2, cv2.COLOR_BGR2GRAY)
                ret32, th22 = cv2.threshold(areagray2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                img_area2 = areagray2.size
                fiber_area2 = cv2.countNonZero(th22)
                b = str(fiber_area2 / img_area2) + '\t'

                cv2.imshow('sec_B', th22)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                text_2 = "Percentage of vascular bundles in the A-end section: " + str(a) + "\n\n" + "Percentage of vascular bundles in the B-end section: " + str(b)
                self.w1.insert(5.0, text_2)

            elif self.exist.get() == 1:
                img = cv2.imread(sec_A)
                imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                ret, thresh_1 = cv2.threshold(imgray, th_a, 255, cv2.THRESH_BINARY_INV)

                contours, hierarchy = cv2.findContours(thresh_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                areas = list()
                for i, cnt in enumerate(contours):
                    areas.append((i, cv2.contourArea(cnt)))  # Area size
                a2 = sorted(areas, key=lambda d: d[1], reverse=True)  # Sorted by size, from largest to smallest
                max_c_area = a2[0][0]  # Select the maximum profile

                cnt = contours[max_c_area]
                rect = cv2.minAreaRect(cnt)  # Minimum external rectangle
                box = np.int0(cv2.boxPoints(rect))  # The four corner points of the rectangle are rounded
                cv2.drawContours(img, [box], 0, (255, 0, 0), 2)

                size = rect[1]
                size = tuple(map(int, size))
                center = rect[0]
                width = img.shape[1]
                height = img.shape[0]
                angle = rect[2]

                # Judgment formula for always keeping the rectangle flat
                if rect[1][0] <= rect[1][1]:
                    angle = 90 + angle
                    beta = rect[1][1]
                    alpha = rect[1][0]
                    size = (beta, alpha)
                    size = tuple(map(int, size))

                M = cv2.getRotationMatrix2D(center, angle, 1)
                img_rot = cv2.warpAffine(img, M, (width, height))
                img_crop = cv2.getRectSubPix(img_rot, size, center)  # Intercepting a rectangular box in a rotated image

                ROI = cv2.selectROI('1', img_crop, showCrosshair=1)  # Mouse interaction to select ROI
                x, y, w, h = ROI
                img_fiber_area = img_crop[y:y + h, x:x + w]

                areagray = cv2.cvtColor(img_fiber_area, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(areagray, (5, 5), 0)
                ret3, th2 = cv2.threshold(areagray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                img_area = areagray.size
                fiber_area = cv2.countNonZero(th2)
                a = str(fiber_area / img_area) + '\t'

                cv2.imshow('sec_A', th2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


                text_2 = "Percentage of vascular bundles in the A-end section: " + str(a) + "\n\n"
                self.w1.insert(5.0, text_2)

        self.l5 = Label(self, text="Click to calculate\npercentage of vascular bundles", pady=20)
        self.l5.grid(row=6, column=1)

        self.btn4 = Button(self, command=fib_rate_calc, text="Click here")
        self.btn4.grid(row=6, column=2)


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x650+200+60")
    root.title("Raw bamboo cross-sectional feature recognition software")
    app = Application(master=root)

    root.mainloop()