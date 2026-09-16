from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import sqlite3

class AlyousefApp(App):
    def build(self):
        self.title = "تطبيق اليوسف للمحاسبة"
        
        conn = sqlite3.connect('alyousef.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS trans (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, inc REAL, exp REAL, dmg REAL)''')
        conn.commit()
        conn.close()

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(Label(text="🍏 تطبيق اليوسف للمحاسبة", font_size=24, size_hint_y=None, height=40))
        
        self.name_input = TextInput(hint_text="اسم العميل", multiline=False, size_hint_y=None, height=40)
        self.inc_input = TextInput(hint_text="الدخل (+)", multiline=False, size_hint_y=None, height=40)
        self.exp_input = TextInput(hint_text="الخرج (-)", multiline=False, size_hint_y=None, height=40)
        self.dmg_input = TextInput(hint_text="التالف (-)", multiline=False, size_hint_y=None, height=40)
        
        main_layout.add_widget(self.name_input)
        main_layout.add_widget(self.inc_input)
        main_layout.add_widget(self.exp_input)
        main_layout.add_widget(self.dmg_input)
        
        btn = Button(text="تسجيل العملية", background_color=(0.17, 0.24, 0.31, 1), size_hint_y=None, height=50)
        btn.bind(on_press=self.add_data)
        main_layout.add_widget(btn)
        
        scroll = ScrollView()
        self.grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        scroll.add_widget(self.grid)
        main_layout.add_widget(scroll)
        
        self.update_table()
        return main_layout

    def add_data(self, instance):
        name = self.name_input.text
        inc = float(self.inc_input.text or 0)
        exp = float(self.exp_input.text or 0)
        dmg = float(self.dmg_input.text or 0)
        
        if name:
            conn = sqlite3.connect('alyousef.db')
            conn.execute("INSERT INTO trans (name, inc, exp, dmg) VALUES (?,?,?,?)", (name, inc, exp, dmg))
            conn.commit()
            conn.close()
            self.update_table()
            self.name_input.text = ""
            self.inc_input.text = ""
            self.exp_input.text = ""
            self.dmg_input.text = ""

    def update_table(self):
        self.grid.clear_widgets()
        headers = ["العميل", "الدخل", "الخرج", "التالف", "المتبقي"]
        for h in headers:
            self.grid.add_widget(Label(text=h, size_hint_y=None, height=30))
            
        conn = sqlite3.connect('alyousef.db')
        cursor = conn.execute("SELECT name, inc, exp, dmg FROM trans ORDER BY id DESC")
        for row in cursor.fetchall():
            rem = row[1] - row[2] - row[3]
            self.grid.add_widget(Label(text=row[0], size_hint_y=None, height=30))
            self.grid.add_widget(Label(text=str(row[1]), size_hint_y=None, height=30))
            self.grid.add_widget(Label(text=str(row[2]), size_hint_y=None, height=30))
            self.grid.add_widget(Label(text=str(row[3]), size_hint_y=None, height=30))
            self.grid.add_widget(Label(text=str(rem), size_hint_y=None, height=30))
        conn.close()

if __name__ == '__main__':
    AlyousefApp().run()
  
