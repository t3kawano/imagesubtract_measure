
import os
import sys
import time
import datetime
import threading
import re
import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tkinter
import tkinter.ttk
import tkinter.filedialog
import cv2 
import PySimpleGUI as sg





############################################################
def main(args):
    #pass
    #if __name__ == "__main__":
    print("run on console")
    
    #test(args)
    
    gui = Imageprocessgui_psg()

    """
    root = tkinter.Tk()
    root.title(u"Image processing")
    root.geometry("600x400")
    
    app = Imageprocessgui(master = root)
    #to test
    #app.chooseadir(imagedir = "C:/path to easy access")
    #app.openadir()
    
    app.mainloop()
    """
    #sys.exit()
    #return app

def test(args):
    print("test function")
    root = tkinter.Tk()
    root.title(u"Image processing")
    root.geometry("600x400")
    #root.protocol("WM_DELETE_WINDOW", on_closing)
    
    app = Imageprocessgui(master = root)
    #app.chooseadir(imagedir = "C:/path to easy access")
    app.chooseadir(imagedir = "/path to easy access")  
    app.openadir()
    app.mainloop()
    #animagedir = "C:/path to easy access"
    animagedir = "/path to easy access"
    temp = cv2.imread(animagedir)

    pass

def on_closing():
    print("cv2.destroyAllWindows")
    cv2.destroyAllWindows()
    #print()
    #root.destroy()


###############################################################
#GUI class

class Imageprocessgui_psg:

    def __init__(self):


        # Top button. open
        frame_top = [[#sg.Button('Open',  
                        sg.FolderBrowse("choose dir", 
                        size = (5.5,1.5),
                        target = "-text_dir_chosen-"),#, key='-choose_dir-'), 
                        sg.Button('Processwindow',
                        key='-button_processwindow-')],
                        [sg.InputText(size=(30,7),
                        key = '-text_dir_chosen-', enable_events=True)]
                    ]

        # Roi section
        roi_arrange = ["12x8","8x6","6x4","4x3","2x2"]

        frame_roi = [
            [sg.Button('autoroi',
                key='-button_autoroi-'), 
            #OptionMenu can not evoke event. use Combo instead
            #sg.OptionMenu(roi_choices, size=(10,7),
            #    default_value="8x6", key = '-choice_roi-')],
            sg.Combo(roi_arrange, size=(10,7),
                default_value="8x6", key = '-combo_roi-', 
                enable_events=True, readonly=True)],
            [sg.Text("width "), 
            sg.InputText(size=(5,7), default_text="100", 
                key = '-text_roiwidth-',enable_events=True),
            sg.Text("column"), 
            sg.InputText(size=(5,7), default_text="8", 
                key = '-text_roicolumn-',enable_events=True)],
            [sg.Text("height"), 
            sg.InputText(size=(5,7), default_text="100", 
                key = '-text_roiheight-',enable_events=True),
            sg.Text("row   "), 
            sg.InputText(size=(5,7), default_text="6", 
                key = '-text_roirow-',enable_events=True)],
            [sg.Text("x pos     "), 
            #sg.InputText(size=(5,7), default_text="23"),
            sg.Slider(range=(1,255),
                            default_value =23,
                            resolution=1,
                            orientation='h',
                            size=(20, 15),
                            enable_events=True,
                            key='-slider_xpos-')],
            [sg.Text("y pos     "), 
            #sg.InputText(size=(5,7), default_text="48"),
            sg.Slider(range=(1,255),
                            default_value =48,
                            resolution=1,
                            orientation='h',
                            size=(20, 15),
                            enable_events=True,
                            key='-slider_ypos-')],
            [sg.Text("x interval"), 
            #sg.InputText(size=(5,7), default_text="23"),
            sg.Slider(range=(1,512),
                            default_value =123,
                            resolution=1,
                            orientation='h',
                            size=(20, 15),
                            enable_events=True,
                            key='-slider_xinterval-')],
            [sg.Text("y interval"), 
            #sg.InputText(size=(5,7), default_text="48"),
            sg.Slider(range=(1,512),
                            default_value =123,
                            resolution=1,
                            orientation='h',
                            size=(20, 15),
                            enable_events=True,
                            key='-slider_yinterval-')],
            [sg.Text("rotate"), 
            sg.InputText(size=(5,7), default_text="0", 
                key = '-text_rotate-',enable_events=True)]

            ]


        # calc parameters
        calc_type = ["post","95%","pre"]

        frame_calparam = [
            sg.Combo(calc_type, size=(10,7),
                default_value="post", key = '-combo_calctype-',
                enable_events=True,readonly=True),
            sg.Text("threshold"), 
            sg.InputText(size=(5,7), default_text="4", 
                key = '-text_threshold-',enable_events=True)
        ]

        # slice setting
        frame_slice = [
        ]

        # start and save
        frame_ss = [sg.Button('Start',size=(5.5,1.5), 
                        key='-button_start-'), 
                    sg.Button('Save',size=(5.5,1.5), 
                        key='-button_save-'), 
                    sg.Button('temp1',
                        key='-button_temp1-')]

        layout = [
            [frame_top],
            [frame_roi],
            [frame_calparam],
            [frame_slice],
            [frame_ss]    
            ]

        self.window = sg.Window("Imagesubtandmeasure ", layout)

        #loop start
        self.loop()

    #####################################################
    #'-button_open-': button_op_en_func,
    #'-button_processwindow-': button_processwindow_func,
    #'button_start': button_start_func,
    #'button_save': button_save_func,
    # process events
    
    #button
    #def choose_dir_func(self, event, values):
    #    pass

    def button_processwindow_func(self, event, values):
        pass

    def button_autoroi_func(self, event, values):
        pass

    def button_start_func(self, event, values):
        pass

    def button_save_func(self, event, values):
        pass

    def button_temp1_func(self, event, values):
        pass

    # combo box
    def combo_roi_func(self, event, values):
        pass

    def combo_calctype_func(self, event, values):
        pass

    #text 
    def text_dir_chosen_func(self, event, values):
        pass
    def text_roiwidth_func(self, event, values):
        pass

    def text_roicolumn_func(self, event, values):
        pass

    def text_roiheight_func(self, event, values):
        pass

    def text_roirow_func(self, event, values):
        pass

    def text_rotate_func(self, event, values):
        pass

    def text_threshold_func(self, event, values):
        pass

    # slider
    def slider_xpos_func(self, event, values):
        pass
    
    def slider_ypos_func(self, event, values):
        pass

    def slider_xinterval_func(self, event, values):
        pass

    def slider_yinterval_func(self, event, values):
        pass


    def close(self):
        self.window.close()
    #window.destroy()
    #window.update()

    #waiting user manipulation
    def loop(self):
        handler = {
            #'-choose_dir-': self.choose_dir_func,
            '-button_processwindow-': self.button_processwindow_func,
            '-button_autoroi-': self.button_autoroi_func,
            '-button_start-': self.button_start_func,
            '-button_save-': self.button_save_func,
            '-button_temp1-': self.button_temp1_func,

            '-combo_roi-': self.combo_roi_func,
            '-combo_calctype-': self.combo_calctype_func,

            '-text_dir_chosen-': self.text_dir_chosen_func,
            '-text_roiwidth-': self.text_roiwidth_func,
            '-text_roicolumn-': self.text_roicolumn_func,
            '-text_roiheight-': self.text_roiheight_func,
            '-text_roirow-': self.text_roirow_func,
            '-text_rotate-': self.text_rotate_func,
            '-text_threshold-': self.text_threshold_func,

            '-slider_xpos-': self.slider_xpos_func,
            '-slider_ypos-': self.slider_ypos_func,
            '-slider_xinterval-': self.slider_xinterval_func,
            '-slider_yinterval-': self.slider_yinterval_func,
        }

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "OK":
                self.close()
                break
            else:
                function = handler[event]
                print(event, values)
                function(event, values)




############################################################
if __name__ == "__main__":
    
    #test(sys.argv[1:])
    main(sys.argv[1:])
else:
    print("__name__" + str(__name__))









