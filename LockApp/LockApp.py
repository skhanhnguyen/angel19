from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import (
    StringProperty,
    BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os

from kivy.core.window import Window

from connected import Connected

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# VALID_IDS = ('1234','abcd')

class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        if app.username in VALID_IDS:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'connected'
            app.numLockerUsed += 1
        else:
            self.manager.transition = SlideTransition()
            self.manager.current = 'loginfail'

        app.config.read(app.get_application_config())
        app.config.write()


    def resetForm(self):
        self.ids['login'].text = ""
        # self.ids['password'].text = ""


class Loginfail(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        if app.username in VALID_IDS:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'connected'
            # app.numLockerUsed += 1
        else:
            self.manager.transition = SlideTransition()
            self.manager.current = 'loginfail'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        # self.ids['password'].text = ""

class full(Screen):
    def collect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    numLockerUsed = NumericProperty(0)
    full = BooleanProperty(False)

    Window.clearcolor = (0.96862745, 0.65882353, 0.10980392, 1)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(Loginfail(name='loginfail'))
        manager.add_widget(full(name='full'))

        if self.full:
            manager.transition = SlideTransition()
            manager.current = 'full'


        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    print('accesing database...')
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('./angelhack19-1a419ced9dcf.json', scope)
    
    gc = gspread.authorize(credentials) 
    val = gc.open('angel19db').sheet1.get_all_values()
    df = pd.DataFrame(val[1:],columns=val[0])
    VALID_IDS = list(df['senderid'].values)

    LoginApp().run()