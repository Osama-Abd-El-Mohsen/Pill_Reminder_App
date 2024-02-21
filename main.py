from plyer import notification
from kivymd.app import MDApp
import time
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivymd.uix.list import *
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.menu import *
import arabic_reshaper
import bidi.algorithm
from kivymd.uix.textfield import *
from kivymd.uix.pickers import MDTimePickerDialVertical
from kivymd.uix.card import MDCard
import webbrowser
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivy.uix.widget import Widget
# from kivymd.tools.hotreload.app import MDApp
from kivy import platform
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import Config
# Config.set('kivy', 'keyboard_mode', 'systemanddock')
from kivy.core.audio import SoundLoader

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

class MainApp(MDApp):

    def check_medical_appointments(self, *args):
        print("iam in")
        now = datetime.now()
        current_time = now.replace(second=0).strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        for med in self.my_global_medical_list:
            if med["Time"] == current_time and med["Date"] == current_date :
                notification.notify(
                    title="Medication Reminder",
                    message=f"Don't forget to take your {med['Name']}!",
                    # app_icon=None, 
                    timeout=5, 
                    # toast=False,  
                )
                print("notification sent")
                sound = SoundLoader.load('alarm.wav')
                if sound:
                    print(f"Sound found at {sound.source}")
                    print(f"Sound length at {sound.length}")
                    sound.play()

####################### Helper Functions ############################

    def arabic_font(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        return bidi_text

    def switch_theme_style(self):
        self.style_state = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.theme_cls.switch_theme()
        self.theme_cls.update_theme_colors()
        self.save()

        self.set_bars_colors()

    def andoid_start_service(name,other_arg):  
        from android import mActivity  
        from jnius import autoclass  
        context = mActivity.getApplicationContext()  
        service_name = "org.bill.remindme" + ".Service" + "Pong"  
        service = autoclass(service_name)  
        service.start(mActivity, '')  # starts or re-initializes a service  
        return service

####################### Helper Functions ############################

####################### Build App Function ############################
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.stored_data = JsonStore('data.json')
        Clock.schedule_once(lambda *args: self.load())
        
    def load(self):
        self.icon_instance =""
        try:
            self.style_state = self.stored_data.get('style')[
                'List2']
        except:
            self.style_state = "Dark"

        now = datetime.now()
        self.tempH = str(now.hour)
        self.tempM = str(now.minute)
        self.tempD = str(now.day)
        self.tempY = str(now.year)
        self.tempMO = str(now.month)
        self.tempAm_Pm = "am" if now.hour < 12 else "pm"
        self.dia2 = ""
        self.time = None
        self.date = None
        self.color = None
        self.medical_name = None
        self.my_global_medical_list = []
        self.theme_cls.theme_style = self.style_state
        
        self.theme_cls.update_theme_colors()
        self.set_bars_colors()

        try:
            self.style_state = self.stored_data.get('style')[
                'List2']
            print("="*20)
            print("get data from json")
            print("="*20)
        except:
            self.style_state = "Dark"

        try:
            self.my_global_medical_list = self.stored_data.get('stored_medicals')[
                'List']
            print("="*20)
            print("Data Loaded")
            print("="*20)
            print(self.my_global_medical_list)
            print("="*20)
            self.id = (self.my_global_medical_list[-1]["Id"]+1)
            for (med) in self.my_global_medical_list:
                x = self.KV.ids.list.add_widget(
                    MDList(
                        MDCard(
                            MDTextField(
                                MDTextFieldHintText(
                                    id=str(med["Id"]),
                                    text="medicament name",
                                    halign="left",
                                ),
                                theme_line_color="Custom",
                                line_color_focus=(0, 1, 0, 0),
                                line_color_normal=(0, 1, 0, 0),
                                text=med["Name"],
                                width="240dp",
                                id=str(med["Id"]),
                                mode="outlined",
                                role="medium",
                                font_style="Headline",
                                halign="left",
                                padding=(10, 0, 0, 0),
                                required=True
                            ),
                            MDIconButton(
                                style="standard",
                                icon="clock",
                                id=str(med["Id"]),
                                on_press=self.show_time_picker
                            ),
                            MDIconButton(
                                style="standard",
                                icon="calendar",
                                id=str(med["Id"]),
                                on_press=self.show_date_picker
                            ),
                            MDIconButton(
                                style="standard",
                                icon="palette",
                                id=str(med["Id"]),
                                opacity=1.0,
                                disabled=False,
                                theme_text_color="Custom",
                                text_color=med["Color"],
                                on_press=self.open_menu
                            ),
                            MDIconButton(
                                id=str(med["Id"]),
                                icon="delete",
                                style="standard",
                                theme_text_color="Custom",
                                text_color="FF5C77",
                                on_press=self.Delete_Medicine,
                            ),
                            style="elevated",
                            id=str(med["Id"]),
                            size_hint=(.5, None),
                            ripple_behavior=False,
                            theme_shadow_softness="Custom",
                            shadow_softness=15,
                            theme_elevation_level="Custom",
                            elevation_level=2,
                            spacing="10dp",
                            size=(1, 250),
                            padding=(10, 10, 10, 10),
                        )))
                self.KV.ids.list.get_ids()[str(
                    med["Id"])].children[-1].bind(text=self.on_focus)
        except:
            self.id = 0

    def save(self):
        self.stored_data.put(
            'stored_medicals', List=self.my_global_medical_list)
        self.stored_data.put(
            'style', List2=self.style_state)

    def build(self):

        try:
            self.style_state = self.stored_data.get('style')[
                'List2']
        except:
            self.style_state = "Dark"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.5
        self.theme_cls.theme_style = self.style_state
        self.theme_cls.primary_palette = "Aliceblue"
        self.KV = Builder.load_file("kivy.kv")
        return self.KV
####################### Build App Function ############################
    def display_message(self, message):
        print("message")

    def on_focus(self, instance, text):
        x = instance.get_ids().keys()
        temp_id = instance.children[0].id
        for (x, med) in enumerate(self.my_global_medical_list):
            if med["Id"] == int(temp_id):
                self.my_global_medical_list[x]['Name'] = text
                print("="*20)
                print("Data Changed")
                print(med)
                self.save()
                print("="*20)
                break

        # print(instance.get_ids()[-4])
####################### Events Function ############################

    def on_start(self):
        Clock.schedule_interval(self.check_medical_appointments, 60)

        def callback(permission, results):
            if all([res for res in results]):
                Clock.schedule_once(self.set_dynamic_color)
        super().on_start()

        if platform == "android":
            from android.permissions import Permission, request_permissions
            permissions = [Permission.READ_EXTERNAL_STORAGE]
            request_permissions(permissions, callback)

            self.service = self.andoid_start_service('Pong')
            print(f'started android service. {self.service}')  

        elif platform in ('linux', 'linux2', 'macos', 'win'):  
                from runpy import run_path  
                from threading import Thread  
                self.service = Thread(  
                    target=run_path,  
                    args=['./service.py'],  
                    kwargs={'run_name': '__main__'},  
                    daemon=True  
                )  
                self.service.start()  
        
        else:  
            raise NotImplementedError(  
                "service start not implemented on this platform"  
            )

    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.backgroundColor,
            self.theme_cls.backgroundColor,
            "Light" if self.style_state == "Dark" else "Light"
        )

####################### Events Function ############################


####################### Info Dialog ############################

    def info_dialog(self):
        self.InfoDialog = MDDialog(
            MDDialogIcon(
                icon="information",
            ),
            MDDialogHeadlineText(
                text="About App",
            ),
            MDDialogSupportingText(
                text="this app devolped by Osama Abd El Mohsen".capitalize(),
            ),

            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="gmail",
                    ),
                    MDListItemSupportingText(
                        text="Osama.m.abdelmohsen@gmail.com",
                    ),
                    on_press=self.info_email_link,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="github",
                    ),
                    MDListItemSupportingText(
                        text="Osama-Abd-El-Mohsen",

                    ),
                    on_press=self.info_github_link,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDDivider(),
                orientation="vertical",
            ),

            MDDialogButtonContainer(
                Widget(),
                MDIconButton(
                        style="standard",
                        theme_text_color="Custom",
                        icon="bug",
                        on_press=self.bug_report_link
                    ),
                MDButton(
                    MDButtonText(text="Ok"),
                    style="text",
                    on_press=self.close_info_dialog
                ),

                spacing="8dp",
            ),
            id="infodialog"
        )
        self.InfoDialog.open()

    def close_info_dialog(self, *args):
        self.InfoDialog.dismiss()

    def info_github_link(self, *arg):
        webbrowser.open("http://www.github.com/Osama-Abd-El-Mohsen")

    def info_email_link(self, *arg):
        webbrowser.open("mailto:Osama.m.abdelmohsen@gmail.com")

    def bug_report_link(self, *arg):
        webbrowser.open("https://forms.gle/kcvaGvwxjow2mRS37")
####################### Info Dialog ############################


####################### medicine_info_dialog ############################

    def medicine_info_dialog(self):
        self.icon_instance = ""
        self.dia2 = MDDialog(
            MDDialogIcon(
                icon="plus",
            ),
            MDDialogHeadlineText(
                text="Remind Me With",
                font_style="Title",
                role='medium',
                bold=True
            ),

            MDDialogContentContainer(
                MDTextField(
                    MDTextFieldHintText(
                        text="medicament name",
                        halign="left",
                    ),
                    MDTextFieldHelperText(
                        text="Enter pill Name"),
                    theme_line_color="Custom",

                    id="medical_name",
                    mode="outlined",
                ),
                id="con",
                orientation="vertical",

            ),

            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Next",
                        font_style="Title", role='medium'),
                    style="tonal",
                    on_press=self.Next_1
                ),
                spacing="10dp",
            ))
        self.dia2.open()

    def Next_1(self, instance):
        self.menu_items = [
            {"text": "White", "on_release": lambda x=f"ffffff": menu_callback_add(
                x)},
            {"text": "Blue", "on_release": lambda x=f"A6E0FF": menu_callback_add(
                x)},
            {"text": "Red", "on_release": lambda x=f"FF5C77": menu_callback_add(
                x)},
            {"text": "Pink", "on_release": lambda x=f"FFAFED": menu_callback_add(
                x)},
            {"text": "Green", "on_release": lambda x=f"BDE986": menu_callback_add(
                x)},
            {"text": "Yellow", "on_release": lambda x=f"FFF3B8": menu_callback_add(
                x)},
            {"text": "Orange", "on_release": lambda x=f"FFB300": menu_callback_add(
                x)},
        ]

        self.menu = MDDropdownMenu(
            id="droplist",
            caller=instance,
            items=self.menu_items)

        def open_menu(icon_instance):
            self.icon_instance = icon_instance
            self.menu.open()

        def menu_callback_add(text_item):
            self.icon_instance.text_color = text_item
            self.color = text_item
            self.menu.dismiss()

        if instance.parent.get_ids()['medical_name'].text != "":
            self.dia2.dismiss()
            self.dia1 = MDDialog(
                MDDialogIcon(
                    icon="palette",
                ),
                MDDialogHeadlineText(
                    text="Chooce Bill Color",
                    font_style="Title",
                    role='medium',
                    bold=True
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDIconButton(
                        style="standard",
                        theme_text_color="Custom",
                        icon="palette",
                        id=f"{self.id}",
                        opacity=1.0,
                        disabled=False,
                        on_press=open_menu
                    ),
                    MDButton(
                        MDButtonText(
                            text="Next",
                            font_style="Title", role='medium'),
                        style="tonal",
                        on_press=self.Next_2
                    ),
                    spacing="10dp",
                ))
            self.dia1.open()

        else:
            instance.theme_bg_color = "Custom"
            instance.md_bg_color = "FF5C77"
            instance.parent.get_ids(
            )['medical_name'].children[0].text = "Pill  Name Is Empty "
            instance.parent.get_ids(
            )['medical_name'].line_color_normal = "FF5C77"

    def Next_2(self, instance):
        try:
            instance.dismiss()
        except:
            try:
                if self.icon_instance.text_color != "":
                    self.dia1.dismiss()
                    now = datetime.now()
                    self.time_picker = MDTimePickerDialVertical()
                    self.time_picker.hour = str(now.hour)
                    self.time_picker.minute = str(now.minute)

                    self.time_picker.bind(on_ok=self.Next_3)
                    self.time_picker.bind(on_cancel=self.cancel)
                    self.time_picker.open()
                else:
                    print(instance)
                    instance.theme_bg_color = "Custom"
                    instance.md_bg_color = "FF5C77"
            except:
                instance.theme_bg_color = "Custom"
                instance.md_bg_color = "FF5C77"

    def Next_3(self, instance):
        self.time = instance.time
        instance.dismiss()
        now = datetime.now()
        self.date_picker = MDModalDatePicker()
        self.date_picker.bind(on_ok=self.Dialog_OK)
        self.date_picker.bind(on_cancel=self.cancel)
        print(str(now.date()))
        new_date = datetime.strptime(str(now.date()), "%Y-%m-%d")
        self.date_picker.sel_day = new_date.day
        self.date_picker.sel_month = new_date.month
        self.date_picker.sel_year = new_date.year
        self.date_picker.update_calendar(
            new_date.year, new_date.month)

        self.date_picker.open()

    def cancel(self, instance):
        instance.dismiss()

    def Dialog_OK(self, instance):
        self.date = instance.get_date()[0]
        self.medical_name = None
        self.medical_name = self.dia2.get_ids()["medical_name"].text
        if self.time != None and self.medical_name != "" and self.date != None and self.color != None:
            instance.dismiss()
            self.add_medicine()

    def add_medicine(self):
        my_med_dict = {}
        now = datetime.now()
        self.tempH = str(now.hour)
        self.tempM = str(now.minute)
        self.tempD = str(now.day)
        self.tempY = str(now.year)
        self.tempMO = str(now.month)
        self.tempAm_Pm = "am" if now.hour < 12 else "pm"
        print(f"id for next card = {self.id}")
        self.KV.ids.list.add_widget(
            MDList(
                MDCard(
                    MDTextField(
                        MDTextFieldHintText(
                            id=str(self.id),
                            text="medicament name",
                            halign="left",
                        ),
                        theme_line_color="Custom",
                        line_color_focus=(0, 1, 0, 0),
                        line_color_normal=(0, 1, 0, 0),
                        text=self.dia2.get_ids()["medical_name"].text,
                        width="240dp",
                        mode="outlined",
                        role="medium",
                        font_style="Headline",
                        halign="left",
                        bold=True,
                        padding=(10, 0, 0, 0),
                        required=True,
                        id=f"{self.id}",

                    ),
                    MDIconButton(
                        style="standard",
                        icon="palette",
                        id=f"{self.id}",
                        opacity=1.0,
                        disabled=False,
                        theme_text_color="Custom",
                        text_color=self.color,
                        on_press=self.open_menu
                    ),
                    MDIconButton(
                        style="standard",
                        id=f"{self.id}",
                        icon="clock",
                        on_press=self.show_time_picker
                    ),
                    MDIconButton(
                        style="standard",
                        icon="calendar",
                        id=f"{self.id}",
                        on_press=self.show_date_picker
                    ),
                    MDIconButton(
                        id=f"{self.id}",
                        icon="delete",
                        style="standard",
                        theme_text_color="Custom",
                        text_color="FF5C77",
                        on_press=self.Delete_Medicine,
                    ),
                    id=f"CardNum{self.id}",
                    style="elevated",
                    size_hint=(.5, None),
                    ripple_behavior=False,
                    theme_shadow_softness="Custom",
                    shadow_softness=15,
                    theme_elevation_level="Custom",
                    elevation_level=2,
                    spacing="10dp",
                    size=(1, 350),
                    padding=(10, 10, 10, 10),

                ))
        )
        print("="*20)
        ax = f"CardNum{self.id}"
        print(ax)
        print(self.KV.ids.list.get_ids())
        print("="*20)
        print(self.KV.ids.list.get_ids()[ax].children[-1])
        self.KV.ids.list.get_ids()[ax].children[-1].bind(text=self.on_focus)

        print("="*20)
        print(self.id)

        if self.time != None and self.date != None and type(self.date) != str and type(self.time) != str:
            self.time = self.time.strftime('%H:%M:%S')
            self.date = self.date.strftime('%Y-%m-%d')

        my_med_dict["Id"] = self.id
        my_med_dict["Name"] = self.medical_name
        my_med_dict["Time"] = self.time
        my_med_dict["Date"] = self.date
        my_med_dict["Color"] = self.color

        self.my_global_medical_list.append(my_med_dict)
        notification.notify(
            title="Card Added ",
            message=" card added successfully",
            timeout=2
        )

        self.save()
        print("="*20)
        print("Saved data = ")
        print(self.my_global_medical_list)
        print("="*20)

        self.time = None
        self.date = None
        self.medical_name = None
        self.color = None
        self.id = self.my_global_medical_list[-1]["Id"] + 1

    def Delete_Medicine(self, instance=None):
        if instance:
            self.KV.ids.list.remove_widget(instance.parent.parent)
            for med in self.my_global_medical_list:
                if med["Id"] == int(instance.id):
                    print("="*20)
                    print("data Deleted")
                    print(med)
                    self.my_global_medical_list.remove(med)
                    self.save()
                    print("="*20)
                    break
            try:
                self.id = self.my_global_medical_list[-1]["Id"]+1
            except:
                self.id = 0
            print(f"deleted id and self.id =  {self.id}")

    def open_menu(self, instance=None):
        self.menu_items = [
            {"text": "White", "on_release": lambda x=f"ffffff": self.menu_callback(
                x, instance)},
            {"text": "Blue", "on_release": lambda x=f"A6E0FF": self.menu_callback(
                x, instance)},
            {"text": "Red", "on_release": lambda x=f"FF5C77": self.menu_callback(
                x, instance)},
            {"text": "Pink", "on_release": lambda x=f"FFAFED": self.menu_callback(
                x, instance)},
            {"text": "Green", "on_release": lambda x=f"BDE986": self.menu_callback(
                x, instance)},
            {"text": "Yellow", "on_release": lambda x=f"FFF3B8": self.menu_callback(
                x, instance)},
            {"text": "Orange", "on_release": lambda x=f"FFB300": self.menu_callback(
                x, instance)},
        ]
        if instance:
            self.menu = MDDropdownMenu(
                id="droplist",
                caller=instance,
                items=self.menu_items)
            self.menu.open()

    def menu_callback(self, text_item, instance):
        instance.text_color = text_item
        for med in self.my_global_medical_list:
            if med["Id"] == int(instance.id):
                med["Color"] = text_item
                self.save()
                break

        self.color = text_item
        self.menu.dismiss()
####################### medicine_info_dialog ############################


####################### Timer Picker ############################
    def show_time_picker(self, instance):
        self.time_picker = MDTimePickerDialVertical()
        self.time_picker.headline_text = instance.id
        self.time_picker.bind(on_ok=self.Time_on_ok)
        self.time_picker.bind(on_cancel=self.Time_on_cancel)

        if len(self.my_global_medical_list) != 0:
            for med in self.my_global_medical_list:
                if med["Id"] == int(self.time_picker.headline_text):
                    if med["Time"] == "None":
                        med["Time"] = "00:00:00"
                        print("time temp 00:00:00 saved")
                        self.save()
                    else:
                        med["Time"] = med["Time"]
                    new_hour = datetime.strptime(med["Time"], "%H:%M:%S")
                    self.time_picker.hour = str(new_hour.hour)
                    self.time_picker.minute = str(new_hour.minute)
                    break
                else:
                    self.time_picker.hour = self.tempH
                    self.time_picker.minute = self.tempM
        else:
            self.time_picker.hour = self.tempH
            self.time_picker.minute = self.tempM

        self.time_picker.open()

    def Time_on_cancel(self,  instance):
        instance.dismiss()

    def Time_on_ok(self, instance):
        self.tempH = instance.hour
        self.tempM = instance.minute
        self.time = instance.time

        if len(self.my_global_medical_list) != 0:
            for med in self.my_global_medical_list:
                if med["Id"] == int(instance.headline_text):
                    med["Time"] = str(instance.time)
                    self.save()
                    print("="*20)
                    print(f"time {str(instance.time)} saved")
                    print("="*20)
                    break
                else:
                    self.time = instance.time

        instance.dismiss()
####################### Timer Picker ############################


####################### Date  Picker ############################
    def show_date_picker(self, instance):
        self.date_dialog = MDModalDatePicker()
        self.date_dialog.headline_text = instance.id
        self.date_dialog.bind(on_ok=self.Date_on_ok)
        self.date_dialog.bind(on_cancel=self.Date_on_cancel)

        if len(self.my_global_medical_list) != 0:

            for med in self.my_global_medical_list:
                if med["Id"] == int(self.date_dialog.headline_text):
                    new_date = datetime.strptime(med["Date"], "%Y-%m-%d")
                    self.date_dialog.sel_day = new_date.day
                    self.date_dialog.sel_month = new_date.month
                    self.date_dialog.sel_year = new_date.year
                    self.date_dialog.update_calendar(
                        new_date.year, new_date.month)
                    break
                else:
                    self.date_dialog.sel_day = int(self.tempD)
                    self.date_dialog.sel_month = int(self.tempMO)
                    self.date_dialog.sel_year = int(self.tempY)
                    self.date_dialog.update_calendar(
                        int(self.tempY),  int(self.tempMO))
        else:
            self.date_dialog.sel_day = int(self.tempD)
            self.date_dialog.sel_month = int(self.tempMO)
            self.date_dialog.sel_year = int(self.tempY)
            self.date_dialog.update_calendar(
                int(self.tempY),  int(self.tempMO))

        self.date_dialog.open()

    def Date_on_cancel(self, instance):
        instance.dismiss()

    def Date_on_ok(self, instance):
        self.date = instance.get_date()[0]
        self.tempD = instance.get_date()[0].day
        self.tempMO = instance.get_date()[0].month
        self.tempY = instance.get_date()[0].year

        for med in self.my_global_medical_list:
            if med["Id"] == int(instance.headline_text):
                med["Date"] = str(instance.get_date()[0])
                self.save()
                print("="*20)
                print(f"time {str(instance.get_date()[0])} saved")
                print("="*20)
                break
        instance.dismiss()
        if self.date != None:
            instance.style = "filled"
####################### Date  Picker ############################


####################### Main ############################
if __name__ == "__main__":
    MainApp().run()
####################### Main ############################
