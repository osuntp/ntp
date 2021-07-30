from UI.UI import UI
from Log import Log
import random
from pandas import DataFrame
from UI.Stylize import Stylize

class Presenter:
    def __init__(self, ui: UI):
        self.ui = ui

        self.__setup_functionality()
    
    def __setup_functionality(self):
        
        # This isn't working in a for loop for some reason, might be because of the lambda expression? revisit
        self.ui.tabs[0].clicked.connect(lambda: self.tab_clicked(0))
        self.ui.tabs[1].clicked.connect(lambda: self.tab_clicked(1))
        self.ui.tabs[2].clicked.connect(lambda: self.tab_clicked(2))
        self.ui.tabs[3].clicked.connect(lambda: self.tab_clicked(3))
        self.ui.tabs[4].clicked.connect(lambda: self.tab_clicked(4))

        # Abort
        self.ui.abort_tab.clicked.connect(self.abort_clicked)

        # TEST: Delete later
        self.ui.TEST_diagnostics_button.clicked.connect(self.TEST_update_diagnostic_page)
        self.ui.TEST_hot_stand_to_green_button.clicked.connect(self.TEST_set_hot_stand_to_green)
        self.ui.TEST_hot_stand_to_red_button.clicked.connect(self.TEST_set_hot_stand_to_red)

    def tab_clicked(self, tab_index):
        Log.debug('A tab was clicked: This is a new test of the logging system. This system will be implemented in all classes going forward')

        if(self.ui.current_tab == self.ui.tabs[tab_index]):
            return

        self.ui.set_current_tab(tab_index)

    def abort_clicked(self):
        print('abort clicked')

    def TEST_update_diagnostic_page(self):
        self.ui.diagnostics.set_valve_voltage(random.randrange(0, 50000))
        self.ui.diagnostics.set_mass_flow(random.randrange(0, 50000))
        self.ui.diagnostics.set_heater_current(random.randrange(0, 50000))
        self.ui.diagnostics.set_heater_duty_cycle(random.randrange(0, 50000))
        self.ui.diagnostics.set_heater_power(random.randrange(0, 50000))

        if(random.choice([True, False])):
            status_text = "COOLING"
        else:
            status_text = "HEATING"

        self.ui.diagnostics.set_heater_state(status_text)

        self.ui.diagnostics.set_heater_set_point(random.randrange(0, 50000))

        x = [0,1,2,3,4,5]
        y = []

        for i in range(6):
            y.append(random.randrange(0,10))

        dataframe = DataFrame({'column1': x, 'column2': y},  columns=['column1', 'column2'])

        self.ui.diagnostics.update_plots(dataframe)

    def TEST_set_hot_stand_to_green(self):
        Stylize.set_status_light_is_lit(self.ui.hot_stand_status_light, True)

    def TEST_set_hot_stand_to_red(self):
        Stylize.set_status_light_is_lit(self.ui.hot_stand_status_light, False)
        
        
    
