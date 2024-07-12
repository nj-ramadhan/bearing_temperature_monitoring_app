from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.signal import find_peaks
import numpy as np
import os
import snap7
import numpy as np
import locale

locale.setlocale(locale.LC_TIME, "id_ID")
plt.style.use('bmh')

colors = {
    "Red": {
        "A200": "#EE2222",
        "A500": "#EE2222",
        "A700": "#EE2222",
    },
    "Blue": {
        "200": "#196BA5",
        "500": "#196BA5",
        "700": "#196BA5",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#FFFFFF",
        "CardsDialogs": "#EEEEEE",
        "FlatButtonDown": "#CCCCCC",
    },
    "Dark": {
        "StatusBar": "101010",
        "AppBar": "#E0E0E0",
        "Background": "#111111",
        "CardsDialogs": "#000000",
        "FlatButtonDown": "#333333",
    },
}

field_pos_small_right_to_left = [
    [0.242,0.790],[0.242,0.990], #lokomotif
    [0.262,0.790],[0.262,0.990],
    [0.338,0.790],[0.338,0.990],
    [0.358,0.790],[0.358,0.990],

    [0.440,0.790],[0.440,0.990], #gerbong 1
    [0.460,0.790],[0.460,0.990],
    [0.534,0.790],[0.534,0.990],
    [0.554,0.790],[0.554,0.990],

    [0.650,0.790],[0.650,0.990], #gerbong 2
    [0.670,0.790],[0.670,0.990],
    [0.744,0.790],[0.744,0.990],
    [0.764,0.790],[0.764,0.990],

    [0.229,0.530],[0.229,0.730], #gerbong 3
    [0.251,0.530],[0.251,0.730],
    [0.324,0.530],[0.324,0.730],
    [0.346,0.530],[0.346,0.730],

    [0.439,0.530],[0.439,0.730], #gerbong 4
    [0.461,0.530],[0.461,0.730],
    [0.534,0.530],[0.534,0.730],
    [0.556,0.530],[0.556,0.730],

    [0.650,0.530],[0.650,0.730], #gerbong 5
    [0.670,0.530],[0.670,0.730],
    [0.744,0.530],[0.744,0.730],
    [0.764,0.530],[0.764,0.730],

    [0.229,0.270],[0.229,0.470], #gerbong 6
    [0.251,0.270],[0.251,0.470],
    [0.324,0.270],[0.324,0.470],
    [0.346,0.270],[0.346,0.470],

    [0.439,0.270],[0.439,0.470], #gerbong 7
    [0.461,0.270],[0.461,0.470],
    [0.534,0.270],[0.534,0.470],
    [0.556,0.270],[0.556,0.470],

    [0.650,0.270],[0.650,0.470], #gerbong 8
    [0.670,0.270],[0.670,0.470],
    [0.744,0.270],[0.744,0.470],
    [0.764,0.270],[0.764,0.470],

    [0.229,0.010],[0.229,0.205], #gerbong 9
    [0.251,0.010],[0.251,0.205],
    [0.324,0.010],[0.324,0.205],
    [0.346,0.010],[0.346,0.205],

    [0.439,0.010],[0.439,0.205], #gerbong 10
    [0.461,0.010],[0.461,0.205],
    [0.534,0.010],[0.534,0.205],
    [0.556,0.010],[0.556,0.206],

    [0.650,0.010],[0.650,0.205], #gerbong 11
    [0.670,0.010],[0.670,0.205],
    [0.744,0.010],[0.744,0.205],
    [0.764,0.010],[0.764,0.205],
]

field_pos_large_right_to_left = [
    [0.242,0.790],[0.242,0.990], #lokomotif
    [0.262,0.790],[0.262,0.990],
    [0.290,0.790],[0.290,0.990],
    [0.310,0.790],[0.310,0.990],
    [0.338,0.790],[0.338,0.990],
    [0.358,0.790],[0.358,0.990],

    [0.440,0.790],[0.440,0.990], #gerbong 1
    [0.460,0.790],[0.460,0.990],
    [0.534,0.790],[0.534,0.990],
    [0.554,0.790],[0.554,0.990],

    [0.650,0.790],[0.650,0.990], #gerbong 2
    [0.670,0.790],[0.670,0.990],
    [0.744,0.790],[0.744,0.990],
    [0.764,0.790],[0.764,0.990],

    [0.229,0.530],[0.229,0.730], #gerbong 3
    [0.251,0.530],[0.251,0.730],
    [0.324,0.530],[0.324,0.730],
    [0.346,0.530],[0.346,0.730],

    [0.439,0.530],[0.439,0.730], #gerbong 4
    [0.461,0.530],[0.461,0.730],
    [0.534,0.530],[0.534,0.730],
    [0.556,0.530],[0.556,0.730],

    [0.650,0.530],[0.650,0.730], #gerbong 5
    [0.670,0.530],[0.670,0.730],
    [0.744,0.530],[0.744,0.730],
    [0.764,0.530],[0.764,0.730],

    [0.229,0.270],[0.229,0.470], #gerbong 6
    [0.251,0.270],[0.251,0.470],
    [0.324,0.270],[0.324,0.470],
    [0.346,0.270],[0.346,0.470],

    [0.439,0.270],[0.439,0.470], #gerbong 7
    [0.461,0.270],[0.461,0.470],
    [0.534,0.270],[0.534,0.470],
    [0.556,0.270],[0.556,0.470],

    [0.650,0.270],[0.650,0.470], #gerbong 8
    [0.670,0.270],[0.670,0.470],
    [0.744,0.270],[0.744,0.470],
    [0.764,0.270],[0.764,0.470],

    [0.229,0.010],[0.229,0.205], #gerbong 9
    [0.251,0.010],[0.251,0.205],
    [0.324,0.010],[0.324,0.205],
    [0.346,0.010],[0.346,0.205],

    [0.439,0.010],[0.439,0.205], #gerbong 10
    [0.461,0.010],[0.461,0.205],
    [0.534,0.010],[0.534,0.205],
    [0.556,0.010],[0.556,0.206],

    [0.650,0.010],[0.650,0.205], #gerbong 11
    [0.670,0.010],[0.670,0.205],
    [0.744,0.010],[0.744,0.205],
    [0.764,0.010],[0.764,0.205],
]

field_pos_small_left_to_right = [
    [0.750,0.990],[0.750,0.790], #lokomotif
    [0.730,0.990],[0.730,0.790],
    [0.650,0.990],[0.650,0.790],
    [0.630,0.990],[0.630,0.790],

    [0.552,0.990],[0.552,0.790], #gerbong 1
    [0.530,0.990],[0.530,0.790],
    [0.455,0.990],[0.455,0.790],
    [0.433,0.990],[0.433,0.790],

    [0.340,0.990],[0.340,0.790], #gerbong 2
    [0.318,0.990],[0.318,0.790],
    [0.245,0.990],[0.245,0.790],
    [0.223,0.990],[0.223,0.790],

    [0.762,0.730],[0.762,0.530], #gerbong 3
    [0.740,0.730],[0.740,0.530],
    [0.667,0.730],[0.667,0.530],
    [0.645,0.730],[0.645,0.530],

    [0.552,0.730],[0.552,0.530], #gerbong 4
    [0.530,0.730],[0.530,0.530],
    [0.455,0.730],[0.455,0.530],
    [0.433,0.730],[0.433,0.530],

    [0.340,0.730],[0.340,0.530], #gerbong 5
    [0.318,0.730],[0.318,0.530],
    [0.245,0.730],[0.245,0.530],
    [0.223,0.730],[0.223,0.530],

    [0.762,0.470],[0.762,0.270], #gerbong 6
    [0.740,0.470],[0.740,0.270],
    [0.667,0.470],[0.667,0.270],
    [0.645,0.470],[0.645,0.270],

    [0.552,0.470],[0.552,0.270], #gerbong 7
    [0.530,0.470],[0.530,0.270],
    [0.455,0.470],[0.455,0.270],
    [0.433,0.470],[0.433,0.270],

    [0.340,0.470],[0.340,0.270], #gerbong 8
    [0.318,0.470],[0.318,0.270],
    [0.245,0.470],[0.245,0.270],
    [0.223,0.470],[0.223,0.270],

    [0.762,0.205],[0.762,0.010], #gerbong 9
    [0.740,0.205],[0.740,0.010],
    [0.667,0.205],[0.667,0.010],
    [0.645,0.205],[0.645,0.010],

    [0.552,0.205],[0.552,0.010], #gerbong 10
    [0.530,0.205],[0.530,0.010],
    [0.455,0.205],[0.455,0.010],
    [0.433,0.205],[0.433,0.010],

    [0.340,0.205],[0.340,0.010], #gerbong 11
    [0.318,0.205],[0.318,0.010],
    [0.245,0.205],[0.245,0.010],
    [0.223,0.205],[0.223,0.010],
]

field_pos_large_left_to_right = [
    [0.750,0.990],[0.750,0.790], #lokomotif
    [0.730,0.990],[0.730,0.790],
    [0.700,0.990],[0.700,0.790],
    [0.680,0.990],[0.680,0.790],
    [0.650,0.990],[0.650,0.790],
    [0.630,0.990],[0.630,0.790],

    [0.552,0.990],[0.552,0.790], #gerbong 1
    [0.530,0.990],[0.530,0.790],
    [0.455,0.990],[0.455,0.790],
    [0.433,0.990],[0.433,0.790],

    [0.340,0.990],[0.340,0.790], #gerbong 2
    [0.318,0.990],[0.318,0.790],
    [0.245,0.990],[0.245,0.790],
    [0.223,0.990],[0.223,0.790],

    [0.762,0.730],[0.762,0.530], #gerbong 3
    [0.740,0.730],[0.740,0.530],
    [0.667,0.730],[0.667,0.530],
    [0.645,0.730],[0.645,0.530],

    [0.552,0.730],[0.552,0.530], #gerbong 4
    [0.530,0.730],[0.530,0.530],
    [0.455,0.730],[0.455,0.530],
    [0.433,0.730],[0.433,0.530],

    [0.340,0.730],[0.340,0.530], #gerbong 5
    [0.318,0.730],[0.318,0.530],
    [0.245,0.730],[0.245,0.530],
    [0.223,0.730],[0.223,0.530],

    [0.762,0.470],[0.762,0.270], #gerbong 6
    [0.740,0.470],[0.740,0.270],
    [0.667,0.470],[0.667,0.270],
    [0.645,0.470],[0.645,0.270],

    [0.552,0.470],[0.552,0.270], #gerbong 7
    [0.530,0.470],[0.530,0.270],
    [0.455,0.470],[0.455,0.270],
    [0.433,0.470],[0.433,0.270],

    [0.340,0.470],[0.340,0.270], #gerbong 8
    [0.318,0.470],[0.318,0.270],
    [0.245,0.470],[0.245,0.270],
    [0.223,0.470],[0.223,0.270],

    [0.762,0.205],[0.762,0.010], #gerbong 9
    [0.740,0.205],[0.740,0.010],
    [0.667,0.205],[0.667,0.010],
    [0.645,0.205],[0.645,0.010],

    [0.552,0.205],[0.552,0.010], #gerbong 10
    [0.530,0.205],[0.530,0.010],
    [0.455,0.205],[0.455,0.010],
    [0.433,0.205],[0.433,0.010],

    [0.340,0.205],[0.340,0.010], #gerbong 11
    [0.318,0.205],[0.318,0.010],
    [0.245,0.205],[0.245,0.010],
    [0.223,0.205],[0.223,0.010],
]

DEBUG = False

TEMP_OFFSET = 2.5412
TEMP_GAIN = 5.0 * 1000.0 #channge from A to mA with gain

BEARING_TEMP_DATA = 100
NUMBER_OF_BEARINGS = 100

BEARING_TEMP_MIN = 42.5

# Define constants for PLC connection and database read
PLC_IP = '192.168.0.2'
RACK = 0
SLOT = 1
DB_NUMBER = 3

DB_OFFSET_COUNTER = 0
DB_OFFSET_TRAIN_NAME = 2
DB_OFFSET_TRAIN_TYPE = 260
DB_OFFSET_TRAIN_SPEED = 534

DB_OFFSET_SENSOR = 532
DB_OFFSET_DIR = 538

DB_OFFSET_TEMPERATURE_L = 562
DB_OFFSET_TEMPERATURE_R = 962

DB_OFFSET_TEMPERATURE_BEARING = [1362, 1762, 2162, 2562, 2962, 3362, 3762, 4162, 4562, 4962,
                                 5362, 5762, 6162, 6562, 6962, 7362, 7762, 8162, 8562, 8962,
                                 9362, 9762, 10162, 10562, 10962, 11362, 11762, 12162, 12562, 12962,
                                 13362, 13762, 14162, 14562, 14962, 15362, 15762, 16162, 16562, 16962,
                                 17362, 1762, 18162, 18562, 18962, 19362, 19762, 20162, 20562, 20962, 
                                 ]

BYTES_TO_READ_S = 8
BYTES_TO_READ_M = 64
BYTES_TO_READ_L = 400

DELAY_BEFORE_READING_PLC = 7
INTERVAL_DURATION_DATA = 0.05  # seconds
INTERVAL_DURATION_UPDATE_TABLE = 0.5
INTERVAL_DURATION_UPDATE_DISPLAY = 1.0
REQUEST_TIME_OUT = 5.0

arr_bearing_temps_left_to_right = np.zeros(100)
arr_bearing_temps_right_to_left = np.zeros(100)

db_bearing_temps = np.zeros([100, 100]) # database set of bearing temperature raw value, array 100 x 100
arr_bearing_temps = np.zeros(100) # data array of bearing temperature raw value in a wheel, array 1 x 100
arr_calc_bearing_temps = np.zeros(100) # data array of calculated bearing temperature, array 1 x 100
calc_bearing_temps = 0.0 # data value of calculated bearing temperature

dir_left_to_right = False
dir_right_to_left = False
prev_dir_left_to_right = False
prev_dir_right_to_left = False

read_sensor_left_to_right = False
read_sensor_right_to_left = False

counting_wheel = 0
counting_wheel_max = 0

train_name = ""
carriage_type = ""
train_speed = 0.0

train_type = 0 # feeder / small = 0, argo / large = 1 

flag_autosave_data = False
flag_autosave_graph = False
graph_state = 0

class ScreenSplash(MDScreen):
    screen_manager = ObjectProperty(None)
    screen_standby = ObjectProperty(None)
    app_window = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(ScreenSplash, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_progress_bar, 0.05)

    def update_progress_bar(self, *args):
        if (self.ids.progress_bar.value + 1) < 100:
            raw_value = self.ids.progress_bar_label.text.split("[")[-1]
            value = raw_value[:-2]
            value = eval(value.strip())
            new_value = value + 1
            self.ids.progress_bar.value = new_value
            self.ids.progress_bar_label.text = "Loading.. [{:} %]".format(new_value)
        else:
            self.ids.progress_bar.value = 100
            self.ids.progress_bar_label.text = "Loading.. [{:} %]".format(100)
            self.screen_manager.current = "screen_dashboard"
            return False

class ScreenData(MDScreen):
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenData, self).__init__(**kwargs)
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path, sort_by='date')
        Clock.schedule_once(self.delayed_init, DELAY_BEFORE_READING_PLC)

    def delayed_init(self, dt):
        self.data_tables = MDDataTable(
            use_pagination=True,
            pagination_menu_pos="auto",
            rows_num=5,
            column_data=[("Bearing ", dp(20))]+[(f"T{i}", dp(10)) for i in range(1,101)]
        )

        self.ids.layout_tables.add_widget(self.data_tables)

        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()
        
        self.ax.set_xlabel("Data No.", fontsize=10)
        self.ax.set_ylabel("Temp. [C]", fontsize=10)

        self.ids.layout_graph.add_widget(FigureCanvasKivyAgg(self.fig))
        try:
            self.connect_to_plc()
            Clock.schedule_interval(self.read_plc, INTERVAL_DURATION_DATA)
            toast("PLC is sucessfully connected")
        except:
            Clock.schedule_interval(self.auto_reconnect, REQUEST_TIME_OUT)
            toast("PLC is disconnected")

    def auto_reconnect(self, dt):
        try:
            self.connect_to_plc()
            Clock.schedule_interval(self.read_plc, INTERVAL_DURATION_DATA)
            Clock.unschedule(self.auto_reconnect)
            toast("PLC is sucessfully connected")
        except:
            toast("PLC is disconnected, try reconnecting..")

    def reset_data(self):
        global db_bearing_temps
        global arr_calc_bearing_temps

        numbers = np.arange(1,101)       
        db_bearing_temps = np.zeros([100, 100])
        arr_calc_bearing_temps = np.zeros(100)
        # numbered_db = np.round(np.vstack((numbers,db_bearing_temps.T)), 1)
        numbered_db = np.vstack((numbers,np.round(db_bearing_temps.T, 1)))
        print(numbered_db)
        self.data_tables.row_data = numbered_db.T.tolist()

    def open_data(self):
        global db_bearing_temps
        global arr_bearing_temps
        global arr_bearing_temps_left_to_right, arr_bearing_temps_right_to_left
        self.file_manager.show(os.path.expanduser(os.getcwd() + "\data"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        try:
            self.exit_manager(path)
        except:
            toast("error select file path")

    def exit_manager(self, *args):
        global db_bearing_temps
        global arr_bearing_temps
        try: 
            toast("opening data")
            data_set = np.loadtxt(*args, delimiter=";", encoding=None)
            # print(data_set)
            db_bearing_temps = data_set.T
            arr_bearing_temps = db_bearing_temps[counting_wheel]
            print(db_bearing_temps)

            self.update_table()
            self.update_graph()

            self.manager_open = False
            self.file_manager.close()
                   
        except Exception as e:
            print("An exception occurred:", e)
            toast('error open file')
            self.manager_open = False
            self.file_manager.close()

    def connect_to_plc(self):
        global plc

        plc = snap7.client.Client()
        plc.connect(PLC_IP, RACK, SLOT)
        return plc

    def read_plc(self, dt):
        global plc
        global arr_bearing_temps, arr_bearing_temps_left_to_right, arr_bearing_temps_right_to_left
        global dir_left_to_right, dir_right_to_left
        global prev_dir_left_to_right, prev_dir_right_to_left
        global read_sensor_left_to_right, read_sensor_right_to_left
        global counting_wheel_max
        global train_name, carriage_type, train_speed, train_type

        try:
            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_TRAIN_NAME,BYTES_TO_READ_M)
            train_name = snap7.util.get_string(DB_bytearray, 0)

            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_TRAIN_TYPE,BYTES_TO_READ_M)
            carriage_type = snap7.util.get_string(DB_bytearray, 0)

            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_TRAIN_SPEED,BYTES_TO_READ_S)
            train_speed = snap7.util.get_real(DB_bytearray, 0)

            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_DIR,BYTES_TO_READ_S)
            dir_right_to_left = snap7.util.get_bool(DB_bytearray, 0, 0)
            dir_left_to_right = snap7.util.get_bool(DB_bytearray, 0, 1)

            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_SENSOR,BYTES_TO_READ_S)
            read_sensor_right_to_left = snap7.util.get_bool(DB_bytearray, 0, 0)
            read_sensor_left_to_right = snap7.util.get_bool(DB_bytearray, 0, 1)
           
            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_COUNTER,BYTES_TO_READ_S)
            counting_wheel_max = snap7.util.get_int(DB_bytearray, 0)

            train_type = 1 if counting_wheel_max > 16 else 0

            if ((dir_right_to_left or dir_left_to_right) and not prev_dir_right_to_left and not prev_dir_left_to_right):
                Clock.schedule_interval(self.auto_load, INTERVAL_DURATION_UPDATE_TABLE)

            if ((prev_dir_right_to_left or prev_dir_left_to_right) and not dir_left_to_right and not dir_right_to_left):
                try:
                    self.save_data()
                    self.reset_data()
                    Clock.unschedule(self.auto_load)

                except Exception as e:
                    print("An exception occurred:", e)
                    toast("error save data")
            
            DB_bytearray = plc.db_read(DB_NUMBER,DB_OFFSET_TEMPERATURE_BEARING[counting_wheel],BYTES_TO_READ_L)

            for i in range(0, 49):
                arr_bearing_temps[i] = snap7.util.get_real(DB_bytearray, i * 4)
            # if (dir_left_to_right):
            if (dir_left_to_right == True):
                arr_bearing_temps_left_to_right = arr_bearing_temps

            # if (dir_right_to_left):
            if (dir_right_to_left == True):                
                arr_bearing_temps_right_to_left = arr_bearing_temps
                       
            prev_dir_right_to_left = dir_right_to_left
            prev_dir_left_to_right = dir_left_to_right
            
        except RuntimeError as e:
            print(f"Error reading PLC data: {e}")
            Clock.schedule_interval(self.auto_reconnect, REQUEST_TIME_OUT)
            toast("PLC is disconnected")

    def finding_bearings(self, counting_wheel):
        global db_bearing_temps
        global arr_bearing_temps
        global calc_bearing_temps
        global arr_calc_bearing_temps  

        arr_bearing_temps = db_bearing_temps[counting_wheel][db_bearing_temps[counting_wheel] != np.array(None)]
        arr_bearing_trimmed = np.trim_zeros(arr_bearing_temps)
        peaks, _ = find_peaks(arr_bearing_temps, height = BEARING_TEMP_MIN)

        try:
            if arr_bearing_trimmed.size != 0:
                middle_value = np.take(arr_bearing_trimmed, arr_bearing_trimmed.size // 2)
                
            # print(middle_value)
            if arr_bearing_temps[peaks].size == 0:
                    calc_bearing_temps = np.max(arr_bearing_trimmed)
            else:
                # if wheel temperature is higher than bearing temperature
                if middle_value <= arr_bearing_trimmed[0]:
                    calc_bearing_temps = middle_value
                
                # if wheel temperature is lower than bearing temperature
                else:
                    calc_bearing_temps = np.max(arr_bearing_temps[peaks])

            self.ids.label_bearing_temp.text = str(np.round(calc_bearing_temps,2))
            toast(f"Temperatur Bearing No.{counting_wheel + 1} Hasil Kalkulasi adalah {np.round(calc_bearing_temps,2)}")

        except Exception as e:
            print("An exception occurred:", e)
            
    def auto_load(self, dt):
        global counting_wheel

        self.update_table()
        self.ids.text_bearing_num.text = str(counting_wheel + 1)
        self.update_bearing_num()

    def update_table(self):           
        global db_bearing_temps
        global arr_bearing_temps
        global calc_bearing_temps
        global arr_calc_bearing_temps        
        global arr_bearing_temps_left_to_right, arr_bearing_temps_right_to_left
        global dir_left_to_right, dir_right_to_left
        global read_sensor_left_to_right, read_sensor_right_to_left
        global counting_wheel, counting_wheel_max

        numbers = np.arange(1,101)
        db_bearing_temps[counting_wheel] = arr_bearing_temps
        db_bearing_temps_trimmed = np.trim_zeros(db_bearing_temps.T[0])
        # print(db_bearing_temps_trimmed)
        # print(db_bearing_temps_trimmed)
        counting_wheel_max = db_bearing_temps_trimmed.size

        if (dir_right_to_left == True):
            arr_calc_bearing_temps[(counting_wheel - 1)*2] = calc_bearing_temps

        if (dir_left_to_right == True):
            arr_calc_bearing_temps[((counting_wheel - 1)*2)+1] = calc_bearing_temps

        if (dir_left_to_right == True or dir_right_to_left == True):
            if (counting_wheel < counting_wheel_max):
                self.finding_bearings(counting_wheel)
                counting_wheel += 1
        
        print(arr_calc_bearing_temps)


        # if((dir_left_to_right and read_sensor_left_to_right) or (dir_right_to_left and read_sensor_right_to_left)): 
        numbered_db = np.vstack((numbers,np.round(db_bearing_temps.T, 1)))

        try:
            self.data_tables.row_data = numbered_db.T.tolist()
        
        except Exception as e:
            print("An exception occurred:", e)

    def update_graph(self, bearing_num = 0):           
        global db_bearing_temps
        global arr_bearing_temps
        global calc_bearing_temps
        global arr_calc_bearing_temps

        try:
            self.fig, self.ax = plt.subplots()
            self.fig.tight_layout()

            self.finding_bearings(bearing_num)
            arr_bearing_trimmed = np.trim_zeros(arr_bearing_temps)
                     
            self.ax.set_xlabel("n", fontsize=10)
            self.ax.set_ylabel("Temp. [C]", fontsize=10)
            self.ax.set_ylim(0, 100)
            self.ax.set_xlim(0, arr_bearing_trimmed.size)
            self.ax.plot(arr_bearing_trimmed)
            self.ax.plot(np.zeros_like(arr_bearing_trimmed) + BEARING_TEMP_MIN, "--", color="gray")

            self.ids.layout_graph.clear_widgets()
            self.ids.layout_graph.add_widget(FigureCanvasKivyAgg(self.fig))
        
        except Exception as e:
            print("An exception occurred:", e)
            err_msg = str(e)
            toast(err_msg)
    
    def update_bearing_num(self):
        self.update_graph(int(self.ids.text_bearing_num.text) - 1)
        
    def sort_on_num(self, data):
        try:
            return zip(
                *sorted(
                    enumerate(data),
                    key=lambda l: l[0][0]
                )
            )
        except:
            toast("Error sorting data")

    def save_data(self):
        global db_bearing_temps
        global arr_bearing_temps

        ScreenDashboard = self.screen_manager.get_screen('screen_dashboard')

        try:
            # name initialization
            name_file_now = datetime.now().strftime("\data\%d_%m_%Y_%H_%M_%S.csv")
            name_file_dashboard = datetime.now().strftime("%d_%m_%Y_%H_%M_%S.csv")
            cwd = os.getcwd()
            cwd_dashboard = 'C:\\Users\\khout\\OneDrive\\Desktop\\HISTORY_DATA\\'
            disk = cwd + name_file_now
            disk_dashboard = cwd_dashboard + name_file_dashboard

            header_text = "Roda 1"
            for i in range(2,101):
                header_text = header_text + ';' + "Roda " + str(i) 
            
            # save history data to default folder 
            with open(disk,"wb") as f:
                np.savetxt(f, db_bearing_temps.T, fmt="%.2f",delimiter=";",header=header_text)
            
            # save history data to dashboard folder
            with open(disk_dashboard,"wb") as f:
                np.savetxt(f, db_bearing_temps.T, fmt="%.2f",delimiter=";",header=header_text)

            # name initialization
            name_file_now = datetime.now().strftime("\data\calc_result_%d_%m_%Y_%H_%M_%S.csv")
            name_file_dashboard = datetime.now().strftime("calc_result_%d_%m_%Y_%H_%M_%S.csv")
            disk = cwd + name_file_now
            disk_dashboard = cwd_dashboard + name_file_dashboard

            calculated_data = np.vstack((arr_calc_bearing_temps, np.empty([2,100])))
            print(calculated_data)
            
            # save calculated data to default folder  
            with open(disk,"wb") as f:
                np.savetxt(f, calculated_data, fmt="%.2f",delimiter=";",header=header_text)

            # save calculated data to dashboard folder          
            with open(disk_dashboard,"wb") as f:
                np.savetxt(f, calculated_data, fmt="%.2f",delimiter=";",header=header_text)

            # save screenshot
            ScreenDashboard.save_screen()

            print("sucessfully save data")
            toast("sucessfully save data")

        except Exception as e:
            print("error saving data")
            toast(f"error saving data {e}")

    def screen_dashboard(self):
        self.screen_manager.current = 'screen_dashboard'

    def screen_data(self):
        self.screen_manager.current = 'screen_data'

    def exec_shutdown(self): 
        toast("Shutting down system")
        os.system("shutdown /s /t 1") #for windows os
        # os.system("shutdown -h now") #for linux os

class ScreenDashboard(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenDashboard, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, DELAY_BEFORE_READING_PLC)
        
    def delayed_init(self, dt):
        self.standby()
        Clock.schedule_interval(self.auto_load, INTERVAL_DURATION_UPDATE_DISPLAY)

    def auto_load(self, dt):
        global dir_left_to_right, dir_right_to_left
        global train_name, carriage_type, train_speed
        global counting_wheel, counting_wheel_max
        
        screenData = self.screen_manager.get_screen('screen_data')

        self.ids.lb_realtime_clock.text = str(datetime.now().strftime("%A, %d %B %Y %H:%M:%S"))
        screenData.ids.lb_realtime_clock.text = str(datetime.now().strftime("%A, %d %B %Y %H:%M:%S"))

        self.ids.lb_train_name.text = "Kereta: " + train_name
        screenData.ids.lb_train_name.text = "Kereta: " + train_name

        self.ids.lb_train_type.text = "Jenis Sarana: " + carriage_type
        screenData.ids.lb_train_type.text = "Jenis Sarana: " + carriage_type

        self.ids.lb_train_wheel.text = "Jumlah Roda: " + str(counting_wheel_max)
        screenData.ids.lb_train_wheel.text = "Jumlah Roda: " + str(counting_wheel_max)

        self.ids.lb_train_speed.text = "Kecepatan: " + f"{train_speed:10.2f}"
        screenData.ids.lb_train_speed.text = "Kecepatan: " + f"{train_speed:10.2f}"

        if (dir_left_to_right == True):
            self.move_left_to_right()
            
        if (dir_right_to_left == True):
            self.move_right_to_left()

        if (dir_right_to_left == False and dir_left_to_right == False):
            self.standby()

    def move_right_to_left(self):
        global field_pos_right_to_left
        global arr_calc_bearing_temps
        global train_type, train_name
        global counting_wheel_max

        screenData = self.screen_manager.get_screen('screen_data')

        if train_type == 1:
            self.ids.background_image.source = 'asset/train_large_right_to_left.jpg'
            train_name = "Argo"
        else:
            self.ids.background_image.source = 'asset/train_small_right_to_left.jpg'
            train_name = "Feeder"

        self.ids.lb_train_dir.text = "dari arah kanan ke kiri"
        screenData.ids.lb_train_dir.text = "dari arah kanan ke kiri"

        try:
            self.ids.layout_text_temps.clear_widgets()
            for i in range(0,counting_wheel_max):
                field = MDLabel(id=f'T_{i+1}', 
                                #text=f'{i}', -> Untuk Menampilkan Posisi Data
                                text= f'{np.round(arr_calc_bearing_temps[i],1)}', #-> Untuk Menampilkan data suhu bearing
                                theme_text_color= 'Primary' if (arr_calc_bearing_temps[i] <= BEARING_TEMP_MIN) else 'Error' ,
                                font_style= 'Caption',
                                pos_hint= {'center_x': (field_pos_large_right_to_left[i][0]) if train_type == 1 else (field_pos_small_right_to_left[i][0]),
                                           'center_y': (field_pos_large_right_to_left[i][1]) if train_type == 1 else (field_pos_small_right_to_left[i][1])}
                )
                self.ids.layout_text_temps.add_widget(field)

        except Exception as e:
            print("An exception occurred:", e)
            toast('error open screen')      

    def move_left_to_right(self):
        global field_pos_left_to_right
        global arr_calc_bearing_temps
        global train_type, train_name

        screenData = self.screen_manager.get_screen('screen_data')

        if train_type == 1:
            self.ids.background_image.source = 'asset/train_large_left_to_right.jpg'
            train_name = "Argo"
        else:
            self.ids.background_image.source = 'asset/train_small_left_to_right.jpg'
            train_name = "Feeder"

        self.ids.lb_train_dir.text = "dari arah kiri ke kanan"
        screenData.ids.lb_train_dir.text = "dari arah kiri ke kanan"

        try:
            self.ids.layout_text_temps.clear_widgets()
            for i in range(0,counting_wheel_max):
                field = MDLabel(id=f'T_{i+1}', 
                                #text=f'{i}', -> Untuk Menampilkan Posisi Data
                                text= f'{np.round(arr_calc_bearing_temps[i],1)}', #-> Untuk Menampilkan data suhu bearing
                                theme_text_color= 'Primary' if (arr_calc_bearing_temps[i] <= BEARING_TEMP_MIN) else 'Error' ,
                                font_style= 'Caption',
                                pos_hint= {'center_x': (field_pos_large_right_to_left[i][0]) if train_type == 1 else (field_pos_small_right_to_left[i][0]),
                                           'center_y': (field_pos_large_right_to_left[i][1]) if train_type == 1 else (field_pos_small_right_to_left[i][1])}
                )
                self.ids.layout_text_temps.add_widget(field)

        except Exception as e:
            print("An exception occurred:", e)
            toast('error open screen')   

    def standby(self):
        screenData = self.screen_manager.get_screen('screen_data')
        self.ids.background_image.source = 'asset/train_standby.png'
        self.ids.layout_text_temps.clear_widgets()

        self.ids.lb_train_name.text = "Standby"
        screenData.ids.lb_train_name.text = "Standby"

        self.ids.lb_train_type.text = "Tidak ada kereta melintas"
        screenData.ids.lb_train_type.text = "Tidak ada kereta melintas"

        self.ids.lb_train_wheel.text = ""
        screenData.ids.lb_train_wheel.text = ""

        self.ids.lb_train_speed.text = ""
        screenData.ids.lb_train_speed.text = ""

        self.ids.lb_train_dir.text = ""
        screenData.ids.lb_train_dir.text = ""

    def save_screen(self):
        try:
            # save screen shot to default folder
            name_file_now = datetime.now().strftime("\screenshot\%d_%m_%Y_%H_%M_%S.png")
            name_file_dashboard = datetime.now().strftime("%d_%m_%Y_%H_%M_%S.png")
            cwd = os.getcwd()
            cwd_dashboard = 'C:\\Users\\khout\\OneDrive\\Desktop\\HISTORY_DATA\\'
            disk = cwd + name_file_now
            disk_dashboard = cwd_dashboard + name_file_dashboard

            self.ids.layout_dashboard.export_to_png(disk)
            self.ids.layout_dashboard.export_to_png(disk_dashboard)

            print("sucessfully save screenshot")
            toast("sucessfully save screenshot")

        except:
            print("error saving screenshot")
            toast("error saving screenshot")

    def screen_dashboard(self):
        self.screen_manager.current = 'screen_dashboard'

    def screen_data(self):
        self.screen_manager.current = 'screen_data'

    def exec_shutdown(self): 
        toast("Shutting down system")
        os.system("shutdown /s /t 1") #for windows os
        # os.system("shutdown -h now") #for linux os

class RootScreen(ScreenManager):
    pass

class BearingTemperatureMonitoringApp(MDApp):
    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"
        self.icon = "asset\logo_kai.png" #for windows os
        Window.fullscreen = 'auto'
        Window.borderless = True
        Window.allow_screensaver = True

        Builder.load_file('main.kv')
        return RootScreen()

if __name__ == "__main__":
    BearingTemperatureMonitoringApp().run()
