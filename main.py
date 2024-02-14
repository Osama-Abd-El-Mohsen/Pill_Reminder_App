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
from kivymd.tools.hotreload.app import MDApp
from kivy import platform
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
# from kivymd.app import MDApp
from kivymd.utils.set_bars_colors import set_bars_colors


class MainApp(MDApp):
    DEBUG = True
####################### Helper Functions ############################
    def arabic_font(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        return bidi_text

    def switch_theme_style(self):
        self.theme_cls.primary_palette = (self.theme_cls.primary_palette)
        self.style_state = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.theme_cls.theme_style = (self.style_state )
        self.set_bars_colors()
    
####################### Helper Functions ############################

####################### Build App Function ############################
    def build_app(self):
        self.style_state="Dark"
        self.set_bars_colors()
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
        self.ids_List = []
        self.medical_name = None
        self.my_global_medical_list = []
        self.stored_data = JsonStore('data.json')
        try :
            self.style_state = self.stored_data.get('style')[
                    'List2']
        except : self.style_state="Dark"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.5
        self.theme_cls.theme_style = self.style_state
        self.theme_cls.primary_palette = "Aliceblue"
        self.KV = Builder.load_file("kivy.kv")
        return self.KV
####################### Build App Function ############################

####################### Events Function ############################
    def on_start(self):
        def callback(permission, results):
            if all([res for res in results]):
                Clock.schedule_once(self.set_dynamic_color)
        super().on_start()
        if platform == "android":
            from android.permissions import Permission, request_permissions

            permissions = [Permission.READ_EXTERNAL_STORAGE]
            request_permissions(permissions, callback)
            
        try:
            self.my_global_medical_list = self.stored_data.get('stored_medicals')[
                'List']
            self.id = (self.my_global_medical_list[-1]["Id"]+1)
            for (med) in self.my_global_medical_list:
                self.KV.ids.list.add_widget(
                    MDList(
                        MDCard(
                            MDTextField(
                                MDTextFieldHintText(
                                    text="medicament name",
                                    halign="left",
                                ),
                                theme_line_color="Custom",
                                line_color_focus=(0, 1, 0, 0),
                                line_color_normal=(0, 1, 0, 0),
                                text=med["Name"],
                                width="240dp",
                                id="cardLabel",
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
                            padding=(10, 10, 10, 10),
                            size_hint=(1, None),
                            ripple_behavior=False,
                            theme_shadow_softness="Custom",
                            shadow_softness=15,
                            theme_elevation_level="Custom",
                            elevation_level=2,
                            spacing="10dp",
                        )))
        except:
            self.id = 0

    def on_stop(self):
        self.stored_data.put(
            'stored_medicals', List=self.my_global_medical_list)
        self.stored_data.put(
            'style', List2=self.style_state)
        
    def set_bars_colors(self,):
        set_bars_colors(
            self.theme_cls.primaryColor,  
            self.theme_cls.primaryColor,  
            self.style_state
        )
        print("="*20)
        print(self.style_state)
        print("="*20)
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
####################### Info Dialog ############################


####################### medicine_info_dialog ############################
    def medicine_info_dialog(self):

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
                    id="medical_name",
                    mode="outlined",
                ),
                MDDivider(),
                id="con",
                orientation="vertical",

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
                    on_press=self.open_menu

                ),
                MDIconButton(
                    style="standard",
                    icon="clock",
                    id=f"{self.id}",
                    on_press=self.show_time_picker
                ),
                MDIconButton(
                    style="standard",
                    id=f"{self.id}",
                    icon="calendar",
                    on_press=self.show_date_picker
                ),
                MDButton(
                    MDButtonText(text="Add",
                                 font_style="Title", role='medium'),
                    style="tonal",
                    on_press=self.Dialog_OK
                ),
                spacing="10dp",

            ))

        self.dia2.open()

    def Dialog_OK(self, *arg):
        self.medical_name = None
        self.medical_name = self.dia2.get_ids()["medical_name"].text
        if self.time != None and self.medical_name != "" and self.date != None and self.color != None:
            print(f"Medical name: {self.medical_name}")
            print(f"Date: {self.date}")
            print(f"Time: {self.time}")

            self.dia2.dismiss()
            self.add_medicine()

    def add_medicine(self):
        my_med_dict = {}
        self.KV.ids.list.add_widget(
            MDList(
                MDCard(
                    MDTextField(
                        MDTextFieldHintText(
                            text="medicament name",
                            halign="left",
                        ),
                        theme_line_color="Custom",
                        line_color_focus=(0, 1, 0, 0),
                        line_color_normal=(0, 1, 0, 0),
                        text=self.dia2.get_ids()["medical_name"].text,
                        width="240dp",
                        id="cardLabel",
                        mode="outlined",
                        role="medium",
                        font_style="Headline",
                        halign="left",
                        bold=True,
                        padding=(10, 0, 0, 0),
                        required=True
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
                        id=f"{self.id}",
                        icon="delete",
                        style="standard",
                        theme_text_color="Custom",
                        text_color="FF5C77",
                        on_press=self.Delete_Medicine,
                    ),
                    id=f"CardNum{self.id}",
                    style="elevated",
                    padding=(10, 10, 10, 10),
                    size_hint=(1, None),
                    ripple_behavior=False,
                    theme_shadow_softness="Custom",
                    shadow_softness=15,
                    theme_elevation_level="Custom",
                    elevation_level=2,
                    spacing="10dp",
                ))
        )
        print(self.id)
        self.ids_List.append(self.id)
        if self.time != None and self.date != None and type(self.date) != str and type(self.time) != str:
            self.time = self.time.strftime('%H:%M:%S')
            self.date = self.date.strftime('%Y-%m-%d')

        my_med_dict["Id"] = self.id
        my_med_dict["Name"] = self.medical_name
        my_med_dict["Time"] = self.time
        my_med_dict["Date"] = self.date
        my_med_dict["Color"] = self.color

        self.my_global_medical_list.append(my_med_dict)

        print(self.my_global_medical_list)

        self.time = None
        self.date = None
        self.medical_name = None
        self.color = None
        self.id += 1

    def Delete_Medicine(self, instance=None):
        if instance:
            self.KV.ids.list.remove_widget(instance.parent.parent)
            for med in self.my_global_medical_list:
                if med["Id"] == int(instance.id):
                    print(med)
                    self.my_global_medical_list.remove(med)
                    break

            self.id -= 1

    def open_menu(self, instance=None):
        self.menu_items = [
            {"text": "White", "on_release": lambda x=f"ffffff": self.menu_callback(
                x, instance), "md_bg_color": "ffffff"},
            {"text": "Blue", "on_release": lambda x=f"A6E0FF": self.menu_callback(
                x, instance), "md_bg_color": "A6E0FF"},
            {"text": "Red", "on_release": lambda x=f"FF5C77": self.menu_callback(
                x, instance), "md_bg_color": "FF5C77"},
            {"text": "Pink", "on_release": lambda x=f"FFAFED": self.menu_callback(
                x, instance), "md_bg_color": "FFAFED"},
            {"text": "Green", "on_release": lambda x=f"BDE986": self.menu_callback(
                x, instance), "md_bg_color": "BDE986"},
            {"text": "Yellow", "on_release": lambda x=f"FFF3B8": self.menu_callback(
                x, instance), "md_bg_color": "FFF3B8"},
            {"text": "Orange", "on_release": lambda x=f"FFB300": self.menu_callback(
                x, instance), "md_bg_color": "FFB300"},
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
                print(med)
                if med["Id"] == int(self.time_picker.headline_text):
                    if med["Time"] == "None":
                        med["Time"] = "00:00:00"
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
                    self.date_dialog.update_calendar(new_date.year, new_date.month)
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
                break
        instance.dismiss()
        if self.date != None:
            instance.style = "filled"
####################### Date  Picker ############################


####################### Main ############################
if __name__ == "__main__":
    MainApp().run()
####################### Main ############################
