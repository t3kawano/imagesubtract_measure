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

import flet as ft

def main(page: ft.Page):
    #test(args)
    print("main")
    #page.title = "test"
    #page.padding = 10

    #text= ft.Text("test main")

    #layout = ft.Row(controls = [text],
    #               tight = True,
    #                )
    
    Imageprocess_fletgui(page)
    
    #page.add()
    #page.update()


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




class Imageprocess_fletgui(ft.UserControl):

    #default values    
    d_roi_arrange = ["12x8", "8x6", "6x4", "4x3", "2x2"]
    d_width_int = 100
    d_height_int = 100
    d_xpos_value_int = 23
    d_ypos_value_int = 43
    d_xinterval_value_int = 123
    d_yinterval_value_int = 123
    d_rotate_int = 0
    d_norm_method_list = ["post", "pre", "95%"]
    d_threshold_int = 4
    d_start_slice_int = 1
    d_end_slice_int = 0
    d_step_int = 1

    #def main(page: ft.Page):
    def __init__(self, page: ft.Page):
        self.page = page
        page.window_width = 200 
        page.window_height = 700
        page.window_title = "Image Subtract and Measure"

        #################################################
        #setup parts and functions
        open_button = ft.ElevatedButton("Open", on_click=self.open_button_handler)
        
        test_window_button = ft.ElevatedButton("Test", on_click=self.test_window_button_handler)

        auto_button = ft.ElevatedButton("Auto", on_click=self.auto_roi_button_handler)

        roi_arrange = Imageprocess_fletgui.d_roi_arrange
        dropdown_roi = ft.Dropdown(
            options=[ft.dropdown.Option(x) for x in roi_arrange],
            value="8x6", on_change=self.roi_changed,
            text_size="12", width=60, height=30,
            content_padding=ft.Padding(top=2, bottom=2, left=2, right=2)
        )

        #a text box with a label
        self.width_int = Imageprocess_fletgui.d_width_int
        width_label = ft.Text("width", size="10")
        self.roi_width_text = ft.TextField(value=str(self.width_int), text_size="12", width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=self.roi_width_text_changed)
        
        self.height_int = Imageprocess_fletgui.d_height_int
        height_label = ft.Text("height", size="10")
        self.roi_height_text = ft.TextField(value=str(self.height_int), text_size="12", width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=self.roi_height_text_changed)
        
        column_label = ft.Text("column", size="10")
        self.roi_column_text = ft.TextField(value="8", text_size="12", width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=self.roi_column_text_changed)
        
        row_label = ft.Text("row", size="10")
        self.roi_row_text = ft.TextField(value="6", text_size="12", width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=self.roi_row_text_changed)
        
        xpos_label = ft.Text("x posiion", size="10")
        self.xpos_value_int = Imageprocess_fletgui.d_xpos_value_int
        self.xpos_value = ft.Text(str(self.xpos_value_int),size="10")
        self.slider_xpos = ft.Slider(min=1, max=256, divisions=255, value=self.xpos_value_int,
                                width=190, height=30, 
                                label="{value}", on_change=self.slider_xpos_changed(e, "xpos"))#need rambda ?
        
        ypos_label = ft.Text("y position", size="10")
        ypos_value_int = 43
        async def slider_yposchanged(e):
            nonlocal ypos_value_int
            print("Y position changed: ", e.control.value)
            delta = ypos_value_int - int(e.control.value)
            print("abs(delta)" , abs(delta))
            if abs(delta) < 30:
                ypos_value_int=int(e.control.value)
            else:
                if delta > 0:
                    ypos_value_int=ypos_value_int-1
                else:
                    ypos_value_int=ypos_value_int+1
            slider_ypos.value=ypos_value_int
            ypos_value.value=str(ypos_value_int)
            await ypos_value.update_async()
            await slider_ypos.update_async()
        ypos_value = ft.Text(str(ypos_value_int),size="10")
        
        slider_ypos = ft.Slider(min=1, max=256, divisions=255, value=ypos_value_int,
                                width=190, height=30, 
                                label="{value}", on_change=slider_yposchanged)

        
        xinterval_label = ft.Text("x interval", size="10")
        xinterval_value_int = 123
        async def slider_xinterval_changed(e):
            nonlocal xinterval_value_int
            print("X interval changed:", e.control.value)
            delta = xinterval_value_int - int(e.control.value)
            print("abs(delta)" , abs(delta))
            if abs(delta) < 10:
                xinterval_value_int=int(e.control.value)
            else:
                if delta > 0:
                    xinterval_value_int=xinterval_value_int-1
                else:
                    xinterval_value_int=xinterval_value_int+1
            slider_xinterval.value=xinterval_value_int
            xinterval_value.value=str(xinterval_value_int)
            await xinterval_value.update_async()
            await slider_xinterval.update_async() 
            #page.update
        xinterval_value = ft.Text(str(xinterval_value_int),size="10")

        slider_xinterval = ft.Slider(min=1, max=512, divisions=511, value=xinterval_value_int,
                                width=190, height=30, 
                                label="{value}", on_change=slider_xinterval_changed)
        
        yinterval_label = ft.Text("y interval", size="10")
        yinterval_value_int = 123
        async def slider_yinterval_changed(e):
            nonlocal yinterval_value_int
            print("Y interval changed: ", e.control.value)
            delta = yinterval_value_int - int(e.control.value)
            print("abs(delta)" , abs(delta))
            if abs(delta) < 10:
                yinterval_value_int=int(e.control.value)
            else:
                if delta > 0:
                    yinterval_value_int=yinterval_value_int-1
                else:
                    yinterval_value_int=yinterval_value_int+1
            slider_yinterval.value=yinterval_value_int
            yinterval_value.value=str(yinterval_value_int)
            await yinterval_value.update_async()
            await slider_yinterval.update_async()
        yinterval_value = ft.Text(str(yinterval_value_int),size="10")
        slider_yinterval = ft.Slider(min=1, max=512, divisions=511, value=yinterval_value_int,
                                width=190, height=30, 
                                label="{value}", on_change=slider_yinterval_changed)

        rotate_int = 0
        rotate_label = ft.Text("rotate", size="10")
        async def roi_rotate_text_changed(e):
            nonlocal rotate_int
            print("ROI rotate changed:", e.control.value)
            #cant handle negative. need to fix
            rotate_int = self.sanitize_int(e.control.value, rotate_int)
            roi_rotate_text.value=str(rotate_int)
            await roi_rotate_text.update_async()
        roi_rotate_text = ft.TextField(value=str(rotate_int), text_size="12", 
                                    width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=roi_rotate_text_changed)

        def norm_method_changed(e):
            print("normalize method changed:", e.control.value)
        norm_method_list = ["post", "pre", "95%"]
        dropdown_norm_method = ft.Dropdown(
            options=[ft.dropdown.Option(x) for x in norm_method_list],
            value="post", on_change=norm_method_changed,
            text_size="12", width=60, height=30,
            content_padding=ft.Padding(top=2, bottom=2, left=2, right=2)
        )

        threshold_int = 4
        threshold_label = ft.Text("threshold", size="10")
        async def threshold_text_changed(e):
            nonlocal threshold_int
            print("threshold changed:", e.control.value)
            threshold_int = self.sanitize_int(e.control.value, threshold_int)
            threshold_text.value=str(threshold_int)
            await threshold_text.update_async()
        threshold_text = ft.TextField(value=str(threshold_int), text_size="12", 
                                    width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=threshold_text_changed)

        start_slice_int = 1
        start_slice_label = ft.Text("start", size="10")
        async def start_slice_text_changed(e):
            nonlocal start_slice_int
            print("start slice changed:", e.control.value)
            start_slice_int = self.sanitize_int(e.control.value, start_slice_int)
            start_slice_text.value=str(start_slice_int)
            await start_slice_text.update_async()
        start_slice_text = ft.TextField(value=str(start_slice_int), text_size="12", 
                                    width=40, height=30, 
                                content_padding=ft.Padding(top=2, bottom=2, left=2, right=2),
                                on_change=start_slice_text_changed)

        end_slice_int = 0
        end_slice_label = ft.Text("end", size =10)
        async def end_slice_text_changed(e):
            nonlocal end_slice_int
            print("end slice changed:", e.control.value)
            end_slice_int = self.sanitize_int(e.control.value, end_slice_int)
            end_slice_text.value=str(end_slice_int)
            await end_slice_text.update_async()
        end_slice_text = ft.TextField(value=str(end_slice_int), text_size="12",
                                    width = 40, height = 30,
                                    content_padding = ft.Padding(top=2, bottom=2, left=2, right=2),
                                    on_change = end_slice_text_changed)

        step_int = 1
        step_label = ft.Text("step", size =10)
        async def step_text_changed(e):
            nonlocal step_int
            print("step changed:", e.control.value)
            step_int = self.sanitize_int(e.control.value, step_int)
            step_text.value=str(step_int)
            await step_text.update_async()
        step_text = ft.TextField(value=str(step_int), text_size="12",
                                    width = 40, height = 30,
                                    content_padding = ft.Padding(top=2, bottom=2, left=2, right=2),
                                    on_change = step_text_changed)

        def start_button_handler(e):
            print("start button clicked")
        start_button = ft.ElevatedButton("Start", on_click=start_button_handler)

        def save_button_handler(e):
            print("save button clicked")
        save_button = ft.ElevatedButton("Save", on_click=save_button_handler)

        def temp_button_handler(e):
            print("temp button clicked")
        temp_button = ft.ElevatedButton("Temp", on_click=temp_button_handler)

        ################################################
        #layout
        row_top = ft.Row([open_button,test_window_button])

        row_roi_arrange = ft.Row([auto_button,dropdown_roi])

        row_roi_prop = ft.Row([ft.Column([width_label,height_label]),
                    ft.Column([self.roi_width_text,self.roi_height_text]),
                    ft.Column([column_label,row_label ]),
                    ft.Column([self.roi_column_text,self.roi_row_text])])
            
        row_roi_xpos = ft.Row([ft.Column([ft.Row([xpos_label,self.xpos_value]),
                                        self.slider_xpos])])

        row_roi_ypos = ft.Row([ft.Column([ft.Row([ypos_label,ypos_value]),
                                        slider_ypos])])

        row_roi_xinterval = ft.Row([ft.Column([ft.Row([xinterval_label,xinterval_value]),
                                            slider_xinterval])])
        
        row_roi_yinterval = ft.Row([ft.Column([ft.Row([yinterval_label,yinterval_value]),
                                            slider_yinterval])])

        row_roi_rotate = ft.Row([rotate_label,roi_rotate_text])

        row_method_param = ft.Row([dropdown_norm_method,threshold_label,threshold_text])

        row_slice_param = ft.Row([ft.Column([start_slice_label,start_slice_text]),
                    ft.Column([end_slice_label,end_slice_text]),
                    ft.Column([step_label,step_text ])])

        row_bottom_buttons = ft.Row([start_button,save_button,temp_button])

        # Create a column to hold the button
        column = ft.Column([row_top, row_roi_arrange, row_roi_prop, row_roi_xpos,
                            row_roi_ypos, row_roi_xinterval, row_roi_yinterval,
                            row_roi_rotate, row_method_param,row_slice_param,
                            row_bottom_buttons])

        page.add(column)

    #handler functions
    def open_button_handler(self, e):
        def on_folder_selected(path):
            if path is not None:  # Check if a folder was selected (user might cancel)
                print("Selected folder:", path.path)
            elif path is None:
                print("canceled")
        folder_picker = ft.FilePicker(on_result = on_folder_selected)
        self.page.overlay.append(folder_picker)
        self.page.update()
        folder_picker.get_directory_path()

    def test_window_button_handler(self, e):
        print("test button clicked")

    def auto_roi_button_handler(self, e):
        #do nothing for now
        print("auto roi button clicked")

    def roi_changed(self, e):
        print("ROI changed:", e.control.value)

    async def roi_width_text_changed(self, e):
        #nonlocal width_int#dont understand well, but need this. global not wrok
        print("ROI width changed:", e.control.value)
        self.width_int = self.sanitize_int(e.control.value, self.width_int)
        self.roi_width_text.value=str(self.width_int)
        await self.roi_width_text.update_async()

    async def roi_height_text_changed(self, e):
        print("ROI height changed:", e.control.value)
        self.height_int = self.sanitize_int(e.control.value, self.height_int)
        self.roi_height_text.value=str(self.height_int)
        await self.roi_height_text.update_async()

    def roi_column_text_changed(self,e):
        print("ROI column changed:", e.control.value)

    def roi_row_text_changed(self, e):
        print("ROI row changed:", e.control.value)        

    async def slider_xpos_changed(self, e, message: str):
        #nonlocal xpos_value_int
        print("X position changed:", e.control.value)
        delta = self.xpos_value_int - int(e.control.value)
        print("abs(delta)" , abs(delta))
        if abs(delta) < 30:
            self.xpos_value_int=int(e.control.value)
        else:
            if delta > 0:
                self.xpos_value_int=self.xpos_value_int-1
            else:
                self.xpos_value_int=self.xpos_value_int+1
        self.slider_xpos.value=self.xpos_value_int
        self.xpos_value.value=str(self.xpos_value_int)
        await self.xpos_value.update_async()
        await self.slider_xpos.update_async() 
        #page.update




    def sanitize_int(self, string, intval):
        if string.lstrip('-').isdigit():
            return int(string)
        else:
            return intval

    # Run the Flet app
    #ft.app(target=main)



     
############################################################
if __name__ == "__main__":    
    #test(sys.argv[1:])
    #main(sys.argv[1:])
    # Run the Flet app
    ft.app(target=main)
else:
    print("__name__ " + str(__name__))
            
        
        
        
        
        
