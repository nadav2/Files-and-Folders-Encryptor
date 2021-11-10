
import webbrowser, threading
from shutil import copyfile

from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from tkinter import filedialog
import tkinter as tk
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import *
from kivymd.app import MDApp
from pathlib import Path
from kivy.uix.label import Label
import base64
import os
from kivy import Config
from kivy.core.window import Window
from create_photos import checkbox_image
from encrypt import decrypt_file, encrypt_file
from distutils.dir_util import copy_tree


app_data_path = os.getenv('APPDATA')
path1 = f"{app_data_path}\Eshqol Encryptor"
path = f"{app_data_path}\Eshqol Encryptor"

if not os.path.isdir(path):
    os.mkdir(path)

try:
    open(rf"{path1}\checked.png")
except:
    checkbox_image()

try:
    open(rf"{path}\light.txt")
except:
    with open(rf"{path}\light.txt", 'w') as f:
        f.write("Light")
    f.close()

Window.size = (540, 630)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'resizable', False)
Config.write()

Main = """
<Close>
    Label:
        text: app.text_close
        size_hint_x: None
        font_size: 19
        halign: 'center'
        pos_hint: {"center_x": 0.5, "center_y": 0.67}

    MDRectangleFlatButton:
        text: "Yes"
        font_size: 14
        on_press: app.temp()
        pos_hint: {'center_x':0.72, 'center_y':0.2}

    MDRectangleFlatButton:
        text: "No"
        font_size: 14
        pos_hint: {'center_x':0.28, 'center_y':0.2}

<Warning>
    Label:
        text: 'Any file or data loss caused by\\nthe use of this software is the\\nsole responsibility of the user.'  
        size_hint_x: None
        font_size: 19
        halign: 'center'
        pos_hint: {"center_x": 0.5, "center_y": 0.7}

    MDRectangleFlatButton:
        text: "I agree"
        font_size: 16
        pos_hint: {'center_x':0.5, 'center_y':0.21}

<Info>
    Label:
        text: ' When you use a password generated\\n from a file you must use the exact file in\\n order to decrypt your encrypted file.\\n We highly recommend that you save\\n a copy of your password file in a safe place.'
        size_hint_x: None
        font_size: 18
        pos_hint: {"center_x": 0.5, "center_y": 0.63}

    MDRectangleFlatButton:
        text: "Okay"
        font_size: 16
        pos_hint: {'center_x':0.5, 'center_y':0.15}

Screen:  
    MDLabel:
        text: "Eshqol Encryptor"
        font_size: 26
        pos_hint: {"center_x": 0.5, "center_y": 0.9}
        halign: 'center'
        

    MDRectangleFlatButton:
        text: "File"
        font_size: 24
        pos_hint: {'center_x':0.35, 'center_y':0.77}
        on_press: app.file()
        
        
                
                
    MDRectangleFlatButton:
        id: myfolder
        text: "Folder"
        font_size: 24
        pos_hint: {'center_x':0.65, 'center_y':0.77}
        on_press: app.folder()


    MDTextField:
        id: password1
        hint_text: "Type a password or file path"
        icon_right: "eye-off"
        size_hint_x: None
        width: 300
        font_size: 16
        pos_hint: {"center_x": 0.5, "center_y": 0.63}
        password: True
        mode: "rectangle"
        color_mode: 'accent'  
        on_text: app.get_live_text(self.text)
        write_tab: False  

    MDIconButton:
        icon: "file-search-outline"
        user_font_size: "33sp"
        pos_hint: {"center_x": 0.15, "center_y": 0.628}
        on_press: app.file_password()


    MDIconButton:
        icon: "android"
        user_font_size: "36sp"
        pos_hint: {'center_x':0.723, 'center_y':0.635}
        on_press: app.show_pass()
        opacity: 0    

    MDIconButton:
        id: mode
        icon: "white-balance-sunny"
        user_font_size: "40sp"
        pos_hint: {'center_x':0.08, 'center_y':0.93}
        on_press: app.darkMode()
        opacity: 1 

    MDIconButton:
        icon: "alert-outline"
        user_font_size: "29sp"
        pos_hint: {'center_x':0.18, 'center_y':0.34}
        on_press: app.OpenWarning()

    MDRectangleFlatButton:
        id: enc
        text: "Encrypt"
        font_size: 24
        pos_hint: {'center_x':0.35, 'center_y':0.34}
        # on_press: app.change_label('e')
        on_press: app.encrypt_file()
        disabled: app.dis

    MDRectangleFlatButton:
        id: dec
        text: "Decrypt"
        font_size: 24
        pos_hint: {'center_x':0.65, 'center_y':0.34}
        # on_press: app.change_label('d')
        on_press: app.decrypt_file()
        disabled: app.dis

    MDLabel:
        id: Output
        text: "Choose a file or a folder"
        size_hint_x: None
        font_size: 22
        pos_hint: {"center_x": 0.5, "center_y": 0.23}
        halign: 'center'
        text_size: None, None


    MDLabel:
        id: security
        text: "          Encryption Algorithm: AES-256"
        font_size: 21
        halign: 'center'
        pos_hint: {"center_x": 0.45, "center_y": 0.525}


    MDIconButton:
        icon: "information-outline"
        user_font_size: "23sp"
        pos_hint: {"center_x": 0.07, "center_y": 0.63}
        on_press: app.OpenInfo()

    MDRectangleFlatButton:
        text: "Open this file"
        font_size: 18
        pos_hint: {'center_x':0.5, 'center_y':0.1}
        on_press: app.open_file()

    MDRectangleFlatButton:
        text: "Try our\\nother apps"
        font_size: 14
        halign: 'center'
        pos_hint: {'center_x':0.87, 'center_y':0.93}
        on_press: app.Eshqol()

    # MDRoundFlatButton:
    #     text: "choose a file instead"
    #     font_size: 16
    #     pos_hint: {'center_x':0.5, 'center_y':0.53}
    #     on_press: app.file_password()


    CheckBox:
        pos_hint: {"center_x": 0.87, "center_y": 0.35}
        active: False
        on_active: app.save_copy(self.active)
        background_checkbox_normal: app.checkBoxImage
        background_checkbox_down: app.checkBoxImage2
        size_hint_x: None
        size_hint_y: None
        size: sp(60), sp(60)

    MDLabel:
        text: "save a copy of\\n the original file"
        font_size: 14
        halign: 'center'
        pos_hint: {"center_x": 0.87, "center_y": 0.2935}

"""


class Close(FloatLayout): pass


class Info(FloatLayout): pass


class Warning(FloatLayout): pass


class EshqolEncryptor(MDApp):
    dis = BooleanProperty(False)
    path = ""
    state = ""
    level = 1
    ed = "e"
    text_close = StringProperty('Your encryption is still in process,\\n are you sure you want to quit?')
    checkBoxImage2 = StringProperty(rf"{path1}\checked.png")
    checkBoxImage = StringProperty(rf"{path1}\unchecked.png")
    save_copy_active = False
    path_password = ""

    def build(self):
        self.title = "Eshqol Encryptor"
        self.theme_cls.primary_palette = "Orange"
        self.use_kivy_settings = False
        self.settings_cls = ContentPanel
        self.icon = 'shield.png'
        self.label = Label()
        Window.bind(on_request_close=self.on_request_close, on_dropfile=self._on_file_drop)
        Window.bind(mouse_pos=lambda x, p: setattr(self.label, 'text', str(p)))
        return Builder.load_string(Main)

    def get_live_text(self, text):
        if text == "":
            self.root.ids.password1.hint_text = "Type a password or file path"
        elif os.path.isfile(text):
            self.root.ids.password1.hint_text = "Password generated from file"
            self.root.ids.password1.icon_right = "eye"
            self.root.ids.password1.password = False
        else:
            self.root.ids.password1.hint_text = "Text password"

    def max_size_check(self, text):
        file_size = os.stat(text).st_size / (1024 * 1024)
        gb_size = round(file_size*2/1000, 2)
        if file_size > 300:
            self.root.ids.Output.text = f"warning: your file size exeeding the\n maximume recommended for encryption if\n you want to continue check first that you \nhave at least {gb_size} gb of ram free"

    def _on_file_drop(self, window, file_path):
        try:
            mouse_pos = self.label.text
            mouse_pos_x_y = mouse_pos.replace("(", "").replace(")", "").replace(" ", "").split(",")
            mouse_pos_x = float(mouse_pos_x_y[0])
            mouse_pos_y = float(mouse_pos_x_y[1])
            drag_file_address = file_path.decode("utf-8")

            if 365 < mouse_pos_y < 455 and 84 < mouse_pos_x < 449:
                if os.path.isfile(drag_file_address):
                    self.root.ids.password1.text = drag_file_address
                    self.root.ids.password1.password = False
                    self.root.ids.password1.icon_right = "eye"

            else:
                self.path = drag_file_address
                p = Path(self.path)
                self.folder_path = p.parent
                char = r"h\h"
                char_slash = char[1]
                if os.path.isdir(self.path):
                    self.root.ids.Output.text = f"Folder: {self.path.split(char_slash)[-1]}"
                    self.state = "folder"
                else:
                    self.root.ids.Output.text = f"File: {self.path.split(char_slash)[-1]}"
                    self.state = "file"
        except:
            pass

    def on_start(self):
        with open(rf"{path}\light.txt", 'r') as f1:
            state = f1.read()

        if state == "Light":
            self.root.ids.mode.icon = "white-balance-sunny"
            self.theme_cls.theme_style = "Light"

        else:
            self.root.ids.mode.icon = "weather-night"
            self.theme_cls.theme_style = "Dark"

    def on_request_close(self, *args):
        if self.dis:
            if self.ed == "e":
                self.text_close = 'Your encryption is still in process,\n are you sure you want to quit?'
                self.close()
                return True
            else:
                self.text_close = 'Your decryption is still in process,\n are you sure you want to quit?'
                self.close()
                return True

    def temp(self):
        self.get_running_app().stop()

    def folder1(self):
        self.root.ids.myfolder.disabled = True

    def darkMode(self):
        if self.root.ids.mode.icon == "white-balance-sunny":
            self.root.ids.mode.icon = "weather-night"
            with open(rf"{path}\light.txt", 'w') as f:
                f.write("Dark")
            self.theme_cls.theme_style = "Dark"

        else:
            self.root.ids.mode.icon = "white-balance-sunny"
            with open(rf"{path}\light.txt", 'w') as f:
                f.write("Light")
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Red"
            self.theme_cls.primary_palette = "Orange"

    def file_thread(self):
        root = tk.Tk()
        root.withdraw()
        self.path = filedialog.askopenfilename()
        p = Path(self.path)
        self.folder_path = p.parent
        self.state = "file"
        self.root.ids.Output.text = f"File: {self.path.split('/')[-1]}"
        self.max_size_check(self.path)
        root.mainloop()


    def file(self):
        threading.Thread(target=self.file_thread, daemon=True).start()

    def file_password_thread(self):
        root = tk.Tk()
        root.withdraw()
        self.path_password = filedialog.askopenfilename()
        self.root.ids.password1.text = self.path_password
        self.root.ids.password1.password = False
        self.root.ids.password1.icon_right = "eye"
        root.mainloop()

    def file_password(self):
        threading.Thread(target=self.file_password_thread, daemon=True).start()

    def path_to_password(self, password_text):
        with open(password_text, "rb") as f:
            converted_string = base64.b64encode(f.read())
        return converted_string

    def folder_thread(self):
        root = tk.Tk()
        root.withdraw()
        self.path = filedialog.askdirectory()
        self.folder_path = self.path
        self.state = "folder"
        self.root.ids.Output.text = f"Folder: {self.path.split('/')[-1]}"
        root.mainloop()

    def folder(self):
        threading.Thread(target=self.folder_thread, daemon=True).start()

    def show_pass(self):
        if self.root.ids.password1.password == True:
            self.root.ids.password1.password = False
            password = self.root.ids.password1.text
            self.root.ids.password1.text = ""
            self.root.ids.password1.text = password
            self.root.ids.password1.icon_right = "eye"
        else:
            self.root.ids.password1.password = True
            password = self.root.ids.password1.text
            self.root.ids.password1.text = ""
            self.root.ids.password1.text = password
            self.root.ids.password1.icon_right = "eye-off"

    def change_label_thread(self, a):
        try:
            if a == "e":
                self.ed = "e"
                self.dis = True
                file_stats = os.stat(self.path).st_size / (1024 * 1024)
                if self.state == "file":
                    a = file_stats / 2800
                    a = a * 60
                    a = a * 2.5
                    a = round(a, 2)
                    if a < 0.1:
                        a = 0.10
                    if self.save_copy_active:
                        a = a * 1.2
                    self.root.ids.Output.text = f"""
        Encryption in process...
        Estimate time: {a} seconds"""
                else:
                    self.root.ids.Output.text = "Encryption in process..."

            elif a == "d":
                self.ed = "d"
                self.dis = True
                self.root.ids.Output.text = "Decryption in process..."
        except:
            pass

    def change_label(self, a):
        threading.Thread(target=lambda: self.change_label_thread(a)).start()

    def encrypt_file_for_threading(self):


        if self.path == self.root.ids.password1.text and os.path.isfile(self.root.ids.password1):
            self.root.ids.Output.text = "You can't generate a password\n from the same file you want to encrypt"
            self.dis = False
        else:
            if self.path != "":
                if self.root.ids.password1.text != "":
                    self.change_label('e')
                    password = self.root.ids.password1.text
                    try:
                        password = self.path_to_password(password)
                    except:
                        pass
                    try:
                        if self.save_copy_active:
                            self.copy_path(self.path)

                        if self.state == "file":
                            encrypt_file(self.path, password)
                            self.root.ids.Output.text = "Successfully encrypted!"
                            self.dis = False

                        elif self.state == "folder":
                            self.folder_encryption(self.path, password)
                            self.root.ids.Output.text = "Successfully encrypted!"
                            self.dis = False
                    except:
                        self.root.ids.Output.text = "An error occurred in the encryption process"
                        self.dis = False

                else:
                    self.root.ids.Output.text = "Choose a password"
                    self.dis = False
            else:
                self.root.ids.Output.text = "Choose a file or a folder"
                self.dis = False


    def copy_path(self, path):
        if os.path.isfile(path):
            directory = os.path.dirname(path)
            copyfile(path, f"{directory}\copy_of_original_{os.path.basename(path)}")

        elif (os.path.isdir(path)):
            copy_tree(path, path + "_copy_of_original")

    def encrypt_file(self):
        file_enc_thread = threading.Thread(target=lambda: self.encrypt_file_for_threading(), daemon=True)
        file_enc_thread.start()

    def folder_encryption(self, folder_path, password):
        for file in os.listdir(folder_path):
            new_path = f"{folder_path}/{file}"
            if os.path.isdir(new_path):
                self.folder_encryption(new_path, password)
            elif os.path.isfile(new_path):
                encrypt_file(new_path, password)

    def folder_decryption(self, folder_path, password):
        for file in os.listdir(folder_path):
            new_path = f"{folder_path}/{file}"
            if os.path.isdir(new_path):
                self.folder_decryption(new_path, password)
            elif os.path.isfile(new_path):
                x = decrypt_file(new_path, password)
                if x == False:
                    return False

    def decrypt_file_for_threading(self):
        if self.path != "":
            if self.root.ids.password1.text != "":
                password = self.root.ids.password1.text
                try:
                    password = self.path_to_password(password)
                except:
                    pass

                try:
                    if self.state == "file":
                        check = decrypt_file(self.path, password)
                        if check:
                            self.root.ids.Output.text = "Decrypted Successfully"
                            self.dis = False
                        else:
                            self.root.ids.Output.text = "Your password is incorrect"
                            self.dis = False


                    elif self.state == "folder":
                        check1 = self.folder_decryption(self.path, password)
                        if check1 == False:
                            self.root.ids.Output.text = "Your password is incorrect"
                            self.dis = False
                        else:
                            self.root.ids.Output.text = "Decrypted Successfully"
                            self.dis = False
                except:
                    self.root.ids.Output.text = "An error occurred in the decryption process"
                    self.dis = False

            else:
                self.root.ids.Output.text = "Choose a password"
                self.dis = False
        else:
            self.root.ids.Output.text = "Choose a file or a folder"
            self.dis = False

    def decrypt_file(self):
        self.change_label('d')
        file_dec_thread = threading.Thread(target=lambda: self.decrypt_file_for_threading(), daemon=True)
        file_dec_thread.start()

    def save_copy(self, active_checkbox):
        if active_checkbox:
            self.save_copy_active = True
        else:
            self.save_copy_active = False

    def OpenInfo(self):
        show = Info()
        but = (Button(text="Okay", size_hint=(None, None),
                      width=120, height=60, pos_hint={"center_x": 0.5, "center_y": 0.1}, opacity=0))
        show.add_widget(but)
        popupWindow = Popup(title="Information", content=show, size_hint=(None, None),
                            size=(390, 280), auto_dismiss=False)
        but.bind(on_press=popupWindow.dismiss)
        popupWindow.open()

    def open_file(self):
        try:
            if self.path != "":
                os.startfile(self.path)
            else:
                self.root.ids.Output.text = "We couldn't open this file"
        except:
            self.root.ids.Output.text = "We couldn't open this file"

    def Eshqol(self):
        webbrowser.open("https://www.microsoft.com/en-us/search/shop/Apps?q=Eshqol+Development")

    def OpenWarning(self):
        show = Warning()
        but = (Button(text="Okay", size_hint=(None, None),
                      width=100, height=50, pos_hint={"center_x": 0.5, "center_y": 0.21}, opacity=0))
        show.add_widget(but)
        popupWindow = Popup(title="Note about encryption", content=show, size_hint=(None, None),
                            size=(340, 250), auto_dismiss=False)
        but.bind(on_press=popupWindow.dismiss)
        popupWindow.open()

    def close(self):
        show = Close()
        but = (Button(text="Yes", size_hint=(None, None),
                      width=100, height=50, pos_hint={"center_x": 0.28, "center_y": 0.2}, opacity=0))
        show.add_widget(but)
        popupWindow = Popup(title="Are you sure you want to exit?", content=show, size_hint=(None, None),
                            size=(350, 220), auto_dismiss=False)
        but.bind(on_press=popupWindow.dismiss)
        popupWindow.open()



if __name__ == '__main__':
    EshqolEncryptor().run()