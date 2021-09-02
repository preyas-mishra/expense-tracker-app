from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty,NumericProperty
import sqlite3
import datetime


conn = sqlite3.connect("expense.sqlite3")
cur = conn.cursor()
date = datetime.date.today()

class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        cur.execute('''SELECT * FROM USERDATA''')
        records = cur.fetchall()
        for row in records:
            if self.username.text == row[0] and self.password.text == row[2]:
                sm.current = "HomePage"
            else:
                print("User not exists")


class HomeWindow(Screen):
    super(LoginWindow)
    firstdesc = ObjectProperty(None)
    seconddesc = ObjectProperty(None)
    thirddesc = ObjectProperty(None)
    firstamount = ObjectProperty()
    secondamount = ObjectProperty(None)
    thirdamount = ObjectProperty(None)

    def spinner_clicked(self, value):
        print("Language selected is " + value)

    def submit(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS EXPENSEDATA(DESCRIPTION TEXT, AMOUNT REAL, Date_of_Entry TEXT)''')
        if self.firstdesc.text != "" and self.firstamount.text != "":
            cur.execute('''INSERT INTO EXPENSEDATA(Description,Amount,Date_of_entry) VALUES(?, ?, datetime('now','localtime'))''', (self.firstdesc.text, self.firstamount.text, ))

        if self.seconddesc.text != "" and self.secondamount.text != "":
            cur.execute('''INSERT INTO EXPENSEDATA(Description,Amount,Date_of_entry) VALUES(?, ?, datetime('now','localtime'))''', (self.seconddesc.text, self.secondamount.text, ))

        if self.thirddesc.text != "" and self.thirdamount.text != "":
            cur.execute('''INSERT INTO EXPENSEDATA(Description,Amount,Date_of_entry) VALUES(?, ?, datetime('now','localtime'))''', (self.thirddesc.text, self.thirdamount.text, ))
        print(type(self.secondamount.text))
        conn.commit()
        print("Query executed successfully")
        self.reset()

    def reset(self):
        self.firstdesc.text = ""
        self.firstamount.text = ""
        self.seconddesc.text = ""
        self.secondamount.text = ""
        self.thirddesc.text = ""
        self.thirdamount.text = ""

    def addmore(self):
        self.submit()
        self.reset()


class NewAccount(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    cur.execute('''CREATE TABLE IF NOT EXISTS USERDATA(username TEXT, email TEXT, password TEXT)''')

    def reset(self):
        self.username.text = ""
        self.email.text = ""
        self.password.text = ""

    def login(self):
        self.reset()
        sm.current = "login"

    def submit(self):
        if self.username.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                cur.execute('''INSERT INTO USERDATA(username, email, password) values(?, ?, ?)''', (self.username.text, self.email.text, self.password.text))
                conn.commit()
                sm.current = "HomePage"


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("mygui.kv")
sm = WindowManager()
screens = [LoginWindow(name="login"), NewAccount(name="NewAccountPage"), HomeWindow(name="HomePage")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class ExpenseTracker(App):
    def build(self):
        return sm


if __name__ == "__main__":
    ExpenseTracker().run()
