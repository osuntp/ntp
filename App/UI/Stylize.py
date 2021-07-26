
from PyQt5 import QtWidgets
class Stylize: 
    standard_tab = "\
    QPushButton{ background-color: rgb(80, 122, 196); color: rgb(255, 255, 255); border: 0px;} \
    QPushButton:hover{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 0px;} \
    QPushButton:pressed{ background-color: rgb(0, 58, 85); color: rgb(255, 255, 255); border: 0px;}"

    current_tab =  "\
    QPushButton{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 0px;} \
    QPushButton:hover{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 0px;} \
    QPushButton:pressed{ background-color: rgb(101, 159, 211); color: rgb(255, 255, 255); border: 0px;}"

    abort_tab = "\
    QPushButton{ background-color: rgb(249, 19, 19); color: rgb(255, 255, 255); border: 0px;} \
    QPushButton:hover{ background-color: rgb(170, 0, 0); color: rgb(255, 255, 255); border: 0px;} \
    QPushButton:pressed{ background-color: rgb(95, 0, 0); color: rgb(255, 255, 255); border: 0px;} "

    side_bar_status_green = "\
    QGraphicsView{background-color: rgb(0, 170, 0);}"

    side_bar_status_red = "\
    QGraphicsView{background-color: rgb(249, 19, 19);}"

    @classmethod
    def abort(cls, button):
        button.setStyleSheet(cls.abort_tab)

    @classmethod
    def all_tabs(cls, tabs, starting_tab):
        for tab in tabs:
            tab.setStyleSheet(cls.standard_tab)
        
        starting_tab.setStyleSheet(cls.current_tab)

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

