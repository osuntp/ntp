
from PyQt5 import QtWidgets
class Stylize: 
    standard_tab = "\
    QPushButton{ background-color: rgb(80, 122, 196); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:hover{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:pressed{ background-color: rgb(0, 58, 85); color: rgb(255, 255, 255); border: 2px solid black;}"

    current_tab =  "\
    QPushButton{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:hover{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:pressed{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 2px solid black;}"

    abort_tab = "\
    QPushButton{ background-color: rgb(170, 0, 0); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:hover{ background-color: rgb(249, 19, 19); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:pressed{ background-color: rgb(95, 0, 0); color: rgb(255, 255, 255); border: 2px solid black;} "

    standard_button = "\
    QPushButton{ background-color: rgb(39, 59, 94); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:hover{ background-color: rgb(80, 122, 196); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:pressed{ background-color: rgb(61, 93, 148); color: rgb(255, 255, 255); border: 2px solid black;}"

    start_button_inactive = "\
    QPushButton{ background-color: rgb(65, 65, 65); color: rgb(139, 139, 139); border: 2px solid black;} \
    QPushButton:hover{ background-color: rgb(65, 65, 65); color: rgb(139, 139, 139); border: 2px solid black;} \
    QPushButton:pressed{ background-color: rgb(65, 65, 65); color: rgb(139, 139, 139); border: 2px solid black;}"

    start_button_active = "\
    QPushButton{ background-color: rgb(0, 130, 0); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:hover{ background-color: rgb(0, 170, 0); color: rgb(255, 255, 255); border: 2px solid black;} \
    QPushButton:pressed{ background-color: rgb(0, 50, 0); color: rgb(255, 255, 255); border: 2px solid black;}"

    side_bar_status_green = "\
    QWidget{background-color: rgb(0, 170, 0); border: 2px solid black}"

    side_bar_status_red = "\
    QWidget{background-color: rgb(249, 19, 19); border: 2px solid black}"

    @classmethod
    def abort(cls, button):
        button.setStyleSheet(cls.abort_tab)

    @classmethod
    def all_tabs(cls, tabs):
        for tab in tabs:
            tab.setStyleSheet(cls.standard_tab)

    @classmethod
    def button(cls, buttons):
        for button in buttons:
            button.setStyleSheet(cls.standard_button)

    @classmethod
    def set_start_button_active(cls,button, isActive):
        if(isActive):
            button.setStyleSheet(cls.start_button_active)
        else:
            button.setStyleSheet(cls.start_button_inactive)

    @classmethod
    def set_current_tab(cls, new_tab, prev_tab):
        new_tab.setStyleSheet(cls.current_tab)
        prev_tab.setStyleSheet(cls.standard_tab)

    @classmethod
    def set_status_light_is_lit(cls, status_light: QtWidgets.QGraphicsView, isLit: bool):
        if(isLit):
            status_light.setStyleSheet(cls.side_bar_status_green)
        else:
            status_light.setStyleSheet(cls.side_bar_status_red)

    @classmethod
    def table(cls, table: QtWidgets.QTableWidget):
        pass

