from time import sleep
from datetime import datetime
from kivy.storage.jsonstore import JsonStore
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from notification import MyAndroidNotification
from jnius import autoclass

notificator = MyAndroidNotification()


stored_data = ""
my_global_medical_list = []


def check_medical_appointments(*args):
    state = False
    stored_data = JsonStore('data.json')
    my_global_medical_list = stored_data.get('stored_medicals')['List']
    now = datetime.now()
    current_time = now.replace(second=0).strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    current_day = datetime.now().strftime("%A")
    first_three_letters_day = current_day[:3]

    print("iam in")

    for med in my_global_medical_list:
        if med["Time"] == current_time and med["Date"] == current_date and med["Repeated_List"] == []:
            print("One Time Reminder")
            notificator.notify(
                app_name="Pill Reminder",
                title="Don't forget to take your Medicine",
                message=f"{med['Name']}!",
                app_icon=f"Assets/icon/{med['Color']}.ico",
                ticker="ticker test",
                toast=False
            )
            state = True

        elif med["Time"] == current_time and first_three_letters_day in med["Repeated_List"]:
            print(
                f"Repeated Reminder on {first_three_letters_day}, Repeated_List = {med['Repeated_List']} ")
            notificator.notify(
                app_name="Pill Reminder",
                title="Don't forget to take your Medicine",
                message=f"{med['Name']}!",
                app_icon=f"Assets/icon/{med['Color']}.ico",
                ticker="ticker test",
                toast=False
            )
            state = True

        elif med["Time"] == current_time and med["Repeated_List"] == ["Day"]:
            print(f"Every Day Repeated Reminder ")
            notificator.notify(
                app_name="Pill Reminder",
                title="Don't forget to take your Medicine",
                message=f"{med['Name']}!",
                app_icon=f"Assets/icon/{med['Color']}.ico",
                ticker="ticker test",
                toast=False
            )
            state = True

        if state == True:
            MediaPlayer = autoclass('android.media.MediaPlayer')
            AudioManager = autoclass('android.media.AudioManager')
            mPlayer = MediaPlayer()
            mPlayer.setDataSource('alarm.wav')
            mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
            mPlayer.prepare()
            mPlayer.start()


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    # Clock.schedule_interval(check_medical_appointments, 60)
    while True:
        now = datetime.now()
        print("running , now sec = ", now.second)
        if now.second == 0:
            check_medical_appointments()
        sleep(1)
