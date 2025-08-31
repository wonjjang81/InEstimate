import sys, os
import warnings
warnings.filterwarnings("ignore")
import logging.handlers
import traceback
import time

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import *
import pandas as pd
from PyQt5.QtGui import QPixmap


UI_DIR = f"C:/sample_python/InEstimate/UI/"

Ui_MainWindow, QtBaseClass_MainWindow = uic.loadUiType(UI_DIR+"Main_v01.ui")
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Estimate")

        # 변수
        self.reset_ver()

        # Data
        self.get_excel_data()

        # Init
        self.reset()


    # ==========================
    # Reset
    # ==========================
    def reset(self):
        # --------------------
        # Combobox
        # --------------------
        gubuns = ['아파트', '빌라', '상가']
        self.comboBox_gubun.addItems(gubuns)

        # 조명
        light_gubun = list(dict.fromkeys(self.dict_materials['조명']['구분'].values.tolist()))
        self.comboBox_light_zone.addItems(light_gubun)
        self.selected_light['구분'] = light_gubun[0]

        light_types = list(dict.fromkeys(self.dict_materials['조명']['타입'].values.tolist()))
        self.comboBox_light_types.addItems(light_types)
        self.selected_light['타입'] = light_types[0]

        df = self.dict_materials['조명'].copy()
        df = df[(df['구분']==light_gubun[0]) & (df['타입']==light_types[0])]
        light_names = list(dict.fromkeys(df['제품명'].values.tolist()))
        self.comboBox_light_names.addItems(light_names)
        self.selected_light['제품명'] = light_names[0]

        self.set_lights_price_range(self.selected_light['제품명'])
        self.ChangeLightImage()

        # --------------------
        # 평수
        # --------------------
        self.spinBox_area.valueChanged.connect(self.ChangeArea)


        # --------------------
        # Level
        # --------------------
        self.horizontalSlider_level.valueChanged.connect(self.Changelevel)


        # --------------------
        # 철거
        # --------------------
        # 욕실
        self.ChangeArea()
        self.checkBox_demol_bath.stateChanged.connect(self.CheckDemolBath)
        self.doubleSpinBox_demol_area_bath.valueChanged.connect(self.ChangeDemolAreaBath)
        self.horizontalSlider_demol_bath.valueChanged.connect(self.ChangeDemolSliderBath)
        self.doubleSpinBox_demol_cost_bath.valueChanged.connect(self.ChangeDemolCostBath)

        # 싱크대
        self.checkBox_demol_sink.stateChanged.connect(self.CheckDemolSink)
        self.doubleSpinBox_demol_area_sink.valueChanged.connect(self.ChangeDemolAreaSink)
        self.horizontalSlider_demol_sink.valueChanged.connect(self.ChangeDemolSliderSink)
        self.doubleSpinBox_demol_cost_sink.valueChanged.connect(self.ChangeDemolCostSink)

        # 몰딩
        self.checkBox_demol_mold.stateChanged.connect(self.CheckDemolMold)
        self.doubleSpinBox_demol_area_mold.valueChanged.connect(self.ChangeDemolAreaMold)
        self.horizontalSlider_demol_mold.valueChanged.connect(self.ChangeDemolSliderMold)
        self.doubleSpinBox_demol_cost_mold.valueChanged.connect(self.ChangeDemolCostMold)

        # 문
        self.checkBox_demol_door.stateChanged.connect(self.CheckDemolDoor)
        self.doubleSpinBox_demol_area_door.valueChanged.connect(self.ChangeDemolAreaDoor)
        self.horizontalSlider_demol_door.valueChanged.connect(self.ChangeDemolSliderDoor)
        self.doubleSpinBox_demol_cost_door.valueChanged.connect(self.ChangeDemolCostDoor)

        # 문틀
        self.checkBox_demol_doorFrame.stateChanged.connect(self.CheckDemolDoorFrame)
        self.doubleSpinBox_demol_area_doorFrame.valueChanged.connect(self.ChangeDemolAreaDoorFrame)
        self.horizontalSlider_demol_doorFrame.valueChanged.connect(self.ChangeDemolSliderDoorFrame)
        self.doubleSpinBox_demol_cost_doorFrame.valueChanged.connect(self.ChangeDemolCostDoorFrame)

        # 문지방
        self.checkBox_demol_doorSill.stateChanged.connect(self.CheckDemolDoorSill)
        self.doubleSpinBox_demol_area_doorSill.valueChanged.connect(self.ChangeDemolAreaDoorSill)
        self.horizontalSlider_demol_doorSill.valueChanged.connect(self.ChangeDemolSliderDoorSill)
        self.doubleSpinBox_demol_cost_doorSill.valueChanged.connect(self.ChangeDemolCostDoorSill)

        # 강마루
        self.checkBox_demol_woodFloor.stateChanged.connect(self.CheckDemolWoodFloor)
        self.doubleSpinBox_demol_area_woodFloor.valueChanged.connect(self.ChangeDemolAreaWoodFloor)
        self.horizontalSlider_demol_woodFloor.valueChanged.connect(self.ChangeDemolSliderWoodFloor)
        self.doubleSpinBox_demol_cost_woodFloor.valueChanged.connect(self.ChangeDemolCostWoodFloor)

        # 조명
        self.checkBox_demol_light.stateChanged.connect(self.CheckDemolLight)
        self.doubleSpinBox_demol_area_light.valueChanged.connect(self.ChangeDemolAreaLight)
        self.horizontalSlider_demol_light.valueChanged.connect(self.ChangeDemolSliderLight)
        self.doubleSpinBox_demol_cost_light.valueChanged.connect(self.ChangeDemolCostLight)


        # --------------------
        # 도배
        # --------------------
        # 실크
        self.checkBox_wallpaper_silk.stateChanged.connect(self.CheckWallPaperSilk)
        self.doubleSpinBox_wallpaper_area_silk.valueChanged.connect(self.ChangeWallPaperAreaSilk)
        self.horizontalSlider_wallpaper_silk.valueChanged.connect(self.ChangeWallPaperSliderSilk)
        self.doubleSpinBox_wallpaper_cost_silk.valueChanged.connect(self.ChangeWallPaperCostSilk)

        # 합지
        self.checkBox_wallpaper_lamination.stateChanged.connect(self.CheckWallPaperLamination)
        self.doubleSpinBox_wallpaper_area_lamination.valueChanged.connect(self.ChangeWallPaperAreaLamination)
        self.horizontalSlider_wallpaper_lamination.valueChanged.connect(self.ChangeWallPaperSliderLamination)
        self.doubleSpinBox_wallpaper_cost_lamination.valueChanged.connect(self.ChangeWallPaperCostLamination)


        # --------------------
        # 조명
        # --------------------
        self.comboBox_light_zone.currentIndexChanged.connect(self.ChangeLightZone)
        self.comboBox_light_types.currentIndexChanged.connect(self.ChangeLightType)
        self.comboBox_light_names.currentIndexChanged.connect(self.ChangeLightName)
        self.horizontalSlider_light.valueChanged.connect(self.ChangeLightSlider)
        self.doubleSpinBox_light_quantity.valueChanged.connect(self.ChangeLightQuantity)


    def reset_ver(self):
        self.gubun = '아파트'
        self.dict_materials = {'조명': None,
                               '도어': None,
                               '중문': None,
                               '싱크대': None,
                               '붙박이장': None,
                               '방화문': None,
                               '기타철물': None}
        self.area = 24
        self.level = 1

        self.cost_total = 0.0
        self.cost_vat = 0.0

        self.df_lights = None
        self.selected_light = {'타입': None,
                               '구분': None,
                               '제품명': None,
                               '단가': None,
                               '갯수': None,
                               '비용': None}

        self.items_demol = {'욕실': [False, 0],
                            '싱크대': [False, 0],
                            '몰딩': [False, 0],
                            '문': [False, 0],
                            '문틀': [False, 0],
                            '문지방': [False, 0],
                            '식기': [False, 0],
                            '강마루': [False, 0],
                            '조명': [False, 0]}

        self.items_wallPaper = {'실크': [False, 0],
                                '합지': [False, 0]}



    # ==========================
    # Data
    # ==========================
    def get_excel_data(self):
        path = 'C:/sample_python/InEstimate/Data/자재.xlsx'
        if os.path.isfile(path):
            data = pd.read_excel(path, header=0, sheet_name=None)

            for k, v in data.items():
                if k == '조명':
                    self.dict_materials['조명'] = v.copy()

    def set_lights_price_range(self, name):
        df = self.dict_materials['조명'].copy()

        min_price = df.loc[df['제품명']==name, '제품가격'].values[0] * 10
        max_price = df.loc[df['제품명']==name, '시공가격'].values[0] * 10
        interval = int((max_price - min_price) / 10)

        self.horizontalSlider_light.setMinimum(int(min_price))
        self.horizontalSlider_light.setMaximum(int(max_price))
        self.horizontalSlider_light.setTickInterval(int(interval))
        self.horizontalSlider_light.setValue(int(max_price))

        self.ChangeLightSlider()


    # ==========================
    # Connect
    # ==========================
    # -------------------
    # 평수
    # -------------------
    def ChangeArea(self):
        area = self.spinBox_area.value()

        # 욕실
        if area >= 24:
            bath_area = 2
        elif area < 24:
            bath_area = 1

        self.doubleSpinBox_demol_area_bath.setValue(bath_area)


    # -------------------
    # Level
    # -------------------
    def Changelevel(self):
        level = self.horizontalSlider_level.value()

        # -------------
        # 변경
        # -------------
        # 욕실
        value = self.horizontalSlider_demol_bath.value()
        result = self.getValue_slider(self.horizontalSlider_demol_bath, level)
        self.horizontalSlider_demol_bath.setValue(int(result))

        # 싱크대
        value = self.horizontalSlider_demol_sink.value()
        result = self.getValue_slider(self.horizontalSlider_demol_sink, level)
        self.horizontalSlider_demol_sink.setValue(int(result))

        # 몰딩
        value = self.horizontalSlider_demol_mold.value()
        result = self.getValue_slider(self.horizontalSlider_demol_mold, level)
        self.horizontalSlider_demol_mold.setValue(int(result))

        # 문
        value = self.horizontalSlider_demol_door.value()
        result = self.getValue_slider(self.horizontalSlider_demol_door, level)
        self.horizontalSlider_demol_door.setValue(int(result))

        # 문틀
        value = self.horizontalSlider_demol_doorFrame.value()
        result = self.getValue_slider(self.horizontalSlider_demol_doorFrame, level)
        self.horizontalSlider_demol_doorFrame.setValue(int(result))

        # 문지방
        value = self.horizontalSlider_demol_doorSill.value()
        result = self.getValue_slider(self.horizontalSlider_demol_doorSill, level)
        self.horizontalSlider_demol_doorSill.setValue(int(result))

        # 강마루
        value = self.horizontalSlider_demol_woodFloor.value()
        result = self.getValue_slider(self.horizontalSlider_demol_woodFloor, level)
        self.horizontalSlider_demol_woodFloor.setValue(int(result))

        # 조명
        value = self.horizontalSlider_demol_light.value()
        result = self.getValue_slider(self.horizontalSlider_demol_light, level)
        self.horizontalSlider_demol_light.setValue(int(result))

        # 실크
        value = self.horizontalSlider_wallpaper_silk.value()
        result = self.getValue_slider(self.horizontalSlider_wallpaper_silk, level)
        self.horizontalSlider_wallpaper_silk.setValue(int(result))

        # 합지
        value = self.horizontalSlider_wallpaper_lamination.value()
        result = self.getValue_slider(self.horizontalSlider_wallpaper_lamination, level)
        self.horizontalSlider_wallpaper_lamination.setValue(int(result))

    def getValue_slider(self, slider, level):
        max = int(slider.maximum())
        min = int(slider.minimum())
        value_space = max - min

        if level == 1:
            value = min
        elif level == 10:
            value = max
        else:
            value = round(min + (value_space * (level / 10)), 1)

        return value


    # -------------------
    # 철거_욕실
    # -------------------
    def CheckDemolBath(self):
        check = self.checkBox_demol_bath.isChecked()
        self.items_demol['욕실'][0] = check

    def ChangeDemolAreaBath(self):
        unit = self.horizontalSlider_demol_bath.value()
        area = self.doubleSpinBox_demol_area_bath.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_bath.setValue(cost)

    def ChangeDemolSliderBath(self):
        unit = self.horizontalSlider_demol_bath.value()
        area = self.doubleSpinBox_demol_area_bath.value()
        cost = unit * area

        self.label_demol_bath.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_bath.setValue(cost)

    def ChangeDemolCostBath(self):
        cost = self.doubleSpinBox_demol_cost_bath.value()
        if self.items_demol['욕실'][0] == True:
            self.items_demol['욕실'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_싱크대
    # -------------------
    def CheckDemolSink(self):
        check = self.checkBox_demol_sink.isChecked()
        self.items_demol['싱크대'][0] = check

    def ChangeDemolAreaSink(self):
        unit = self.horizontalSlider_demol_sink.value() / 10
        area = self.doubleSpinBox_demol_area_sink.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_sink.setValue(cost)

    def ChangeDemolSliderSink(self):
        unit = self.horizontalSlider_demol_sink.value() / 10
        area = self.doubleSpinBox_demol_area_sink.value()
        cost = unit * area

        self.label_demol_sink.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_sink.setValue(cost)

    def ChangeDemolCostSink(self):
        cost = self.doubleSpinBox_demol_cost_sink.value()
        if self.items_demol['싱크대'][0] == True:
            self.items_demol['싱크대'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_몰딩
    # -------------------
    def CheckDemolMold(self):
        check = self.checkBox_demol_mold.isChecked()
        self.items_demol['몰딩'][0] = check

    def ChangeDemolAreaMold(self):
        unit = self.horizontalSlider_demol_mold.value() / 10
        area = self.doubleSpinBox_demol_area_mold.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_sink.setValue(cost)

    def ChangeDemolSliderMold(self):
        unit = self.horizontalSlider_demol_mold.value() / 10
        area = self.doubleSpinBox_demol_area_mold.value()
        cost = unit * area

        self.label_demol_mold.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_mold.setValue(cost)

    def ChangeDemolCostMold(self):
        cost = self.doubleSpinBox_demol_cost_mold.value()
        if self.items_demol['몰딩'][0] == True:
            self.items_demol['몰딩'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_문
    # -------------------
    def CheckDemolDoor(self):
        check = self.checkBox_demol_door.isChecked()
        self.items_demol['문'][0] = check

    def ChangeDemolAreaDoor(self):
        unit = self.horizontalSlider_demol_door.value() / 10
        area = self.doubleSpinBox_demol_area_door.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_door.setValue(cost)

    def ChangeDemolSliderDoor(self):
        unit = self.horizontalSlider_demol_door.value() / 10
        area = self.doubleSpinBox_demol_area_door.value()
        cost = unit * area

        self.label_demol_door.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_door.setValue(cost)

    def ChangeDemolCostDoor(self):
        cost = self.doubleSpinBox_demol_cost_door.value()
        if self.items_demol['문'][0] == True:
            self.items_demol['문'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_문틀
    # -------------------
    def CheckDemolDoorFrame(self):
        check = self.checkBox_demol_doorFrame.isChecked()
        self.items_demol['문틀'][0] = check

    def ChangeDemolAreaDoorFrame(self):
        unit = self.horizontalSlider_demol_doorFrame.value() / 10
        area = self.doubleSpinBox_demol_area_doorFrame.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_door.setValue(cost)

    def ChangeDemolSliderDoorFrame(self):
        unit = self.horizontalSlider_demol_doorFrame.value() / 10
        area = self.doubleSpinBox_demol_area_doorFrame.value()
        cost = unit * area

        self.label_demol_doorFrame.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_doorFrame.setValue(cost)

    def ChangeDemolCostDoorFrame(self):
        cost = self.doubleSpinBox_demol_cost_doorFrame.value()
        if self.items_demol['문틀'][0] == True:
            self.items_demol['문틀'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_문지방
    # -------------------
    def CheckDemolDoorSill(self):
        check = self.checkBox_demol_doorSill.isChecked()
        self.items_demol['문지방'][0] = check

    def ChangeDemolAreaDoorSill(self):
        unit = self.horizontalSlider_demol_doorSill.value() / 10
        area = self.doubleSpinBox_demol_area_doorSill.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_doorSill.setValue(cost)

    def ChangeDemolSliderDoorSill(self):
        unit = self.horizontalSlider_demol_doorSill.value() / 10
        area = self.doubleSpinBox_demol_area_doorSill.value()
        cost = unit * area

        self.label_demol_doorSill.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_doorSill.setValue(cost)

    def ChangeDemolCostDoorSill(self):
        cost = self.doubleSpinBox_demol_cost_doorSill.value()
        if self.items_demol['문지방'][0] == True:
            self.items_demol['문지방'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_강마루
    # -------------------
    def CheckDemolWoodFloor(self):
        check = self.checkBox_demol_woodFloor.isChecked()
        self.items_demol['강마루'][0] = check

    def ChangeDemolAreaWoodFloor(self):
        unit = self.horizontalSlider_demol_woodFloor.value() / 10
        area = self.doubleSpinBox_demol_area_woodFloor.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_woodFloor.setValue(cost)

    def ChangeDemolSliderWoodFloor(self):
        unit = self.horizontalSlider_demol_woodFloor.value() / 10
        area = self.doubleSpinBox_demol_area_woodFloor.value()
        cost = unit * area

        self.label_demol_woodFloor.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_woodFloor.setValue(cost)

    def ChangeDemolCostWoodFloor(self):
        cost = self.doubleSpinBox_demol_cost_woodFloor.value()
        if self.items_demol['강마루'][0] == True:
            self.items_demol['강마루'][1] = cost
            self.cal_cost()


    # -------------------
    # 철거_조명
    # -------------------
    def CheckDemolLight(self):
        check = self.checkBox_demol_light.isChecked()
        self.items_demol['조명'][0] = check

    def ChangeDemolAreaLight(self):
        unit = self.horizontalSlider_demol_light.value() / 10
        area = self.doubleSpinBox_demol_area_light.value()
        cost = unit * area

        self.doubleSpinBox_demol_cost_light.setValue(cost)

    def ChangeDemolSliderLight(self):
        unit = self.horizontalSlider_demol_light.value() / 10
        area = self.doubleSpinBox_demol_area_light.value()
        cost = unit * area

        self.label_demol_light.setText(str(f"{unit} 만"))
        self.doubleSpinBox_demol_cost_light.setValue(cost)

    def ChangeDemolCostLight(self):
        cost = self.doubleSpinBox_demol_cost_light.value()
        if self.items_demol['조명'][0] == True:
            self.items_demol['조명'][1] = cost
            self.cal_cost()


    # -------------------
    # 도배_실크
    # -------------------
    def CheckWallPaperSilk(self):
        check = self.checkBox_wallpaper_silk.isChecked()
        self.items_wallPaper['실크'][0] = check

    def ChangeWallPaperAreaSilk(self):
        unit = self.horizontalSlider_wallpaper_silk.value() / 10
        area = self.doubleSpinBox_wallpaper_area_silk.value()
        cost = unit * area * 2.5

        self.doubleSpinBox_wallpaper_cost_silk.setValue(cost)

    def ChangeWallPaperSliderSilk(self):
        unit = self.horizontalSlider_wallpaper_silk.value() / 10
        area = self.doubleSpinBox_wallpaper_area_silk.value()
        cost = unit * area * 2.5

        self.label_wallpaper_silk.setText(str(f"{unit} 만"))
        self.doubleSpinBox_wallpaper_cost_silk.setValue(cost)

    def ChangeWallPaperCostSilk(self):
        cost = self.doubleSpinBox_wallpaper_cost_silk.value()
        if self.items_wallPaper['실크'][0] == True:
            self.items_wallPaper['실크'][1] = cost
            self.cal_cost()


    # -------------------
    # 도배_합지
    # -------------------
    def CheckWallPaperLamination(self):
        check = self.checkBox_wallpaper_lamination.isChecked()
        self.items_wallPaper['합지'][0] = check

    def ChangeWallPaperAreaLamination(self):
        unit = self.horizontalSlider_wallpaper_lamination.value() / 10
        area = self.doubleSpinBox_wallpaper_area_lamination.value()
        cost = unit * area * 2.5

        self.doubleSpinBox_wallpaper_cost_lamination.setValue(cost)

    def ChangeWallPaperSliderLamination(self):
        unit = self.horizontalSlider_wallpaper_lamination.value() / 10
        area = self.doubleSpinBox_wallpaper_area_lamination.value()
        cost = unit * area * 2.5

        self.label_wallpaper_lamination.setText(str(f"{unit} 만"))
        self.doubleSpinBox_wallpaper_cost_lamination.setValue(cost)

    def ChangeWallPaperCostLamination(self):
        cost = self.doubleSpinBox_wallpaper_cost_lamination.value()
        if self.items_wallPaper['합지'][0] == True:
            self.items_wallPaper['합지'][1] = cost
            self.cal_cost()


    # -------------------
    # 조명
    # -------------------
    def ChangeLightZone(self):
        # 변수
        zone = self.comboBox_light_zone.currentText()
        self.selected_light['구분'] = zone
        df = self.dict_materials['조명'].copy()
        df = df[df['구분']==zone]

        # 타입
        types = list(dict.fromkeys(df['타입'].values.tolist()))
        self.comboBox_light_types.clear()
        self.comboBox_light_types.addItems(types)
        self.selected_light['타입'] = types[0]

        # 제품명
        names = list(dict.fromkeys(df['제품명'].values.tolist()))
        self.comboBox_light_names.clear()
        self.comboBox_light_names.addItems(names)
        self.selected_light['제품명'] = names[0]

        # 선택 제품명
        if len(names) > 0:
            self.lineEdit_light.setText(names[0])

        # Change Func
        # self.ChangeLightType()
        # self.ChangeLightName()

        # Set
        self.set_lights_price_range(self.selected_light['제품명'])

    def ChangeLightType(self):
        type = self.comboBox_light_types.currentText()
        self.selected_light['타입'] = type
        if type == '':
            return

        df = self.dict_materials['조명'].copy()
        df = df[(df['구분'] == self.selected_light['구분']) & (df['타입'] == type)]

        # 제품명
        names = list(dict.fromkeys(df['제품명'].values.tolist()))
        self.comboBox_light_names.clear()
        self.comboBox_light_names.addItems(names)
        self.selected_light['제품명'] = names[0]

        # 선택 제품명
        if len(names) > 0:
            self.lineEdit_light.setText(names[0])

            # Set
            self.set_lights_price_range(self.selected_light['제품명'])

    def ChangeLightName(self):
        # zone = self.comboBox_light_zone.currentText()
        # type = self.comboBox_light_types.currentText()
        # self.selected_light['구분'] = zone
        # self.selected_light['타입'] = type

        df = self.dict_materials['조명'].copy()
        name = self.comboBox_light_names.currentText()
        if name == '':
            return
        self.selected_light['제품명'] = name

        value = 0
        try:
            value = df.loc[(df['구분'] == self.selected_light['구분']) &
                           (df['타입'] == self.selected_light['타입']) &
                           (df['제품명'] == name), '시공가격'].values[0] * 10
        except Exception as e:
            traceback.print_exc()

        # Set
        self.lineEdit_light.setText(name)
        self.set_lights_price_range(self.selected_light['제품명'])
        self.horizontalSlider_light.setValue(int(value))

        self.ChangeLightImage()

    def ChangeLightSlider(self):
        unit = self.horizontalSlider_light.value() / 10
        self.selected_light['단가'] = unit
        if self.selected_light['제품명'] == '' or self.selected_light['제품명'] is None:
            return

        quantity = self.doubleSpinBox_light_quantity.value()

        # Set
        self.label_light.setText(str(f"{unit:.1f} 만"))
        self.doubleSpinBox_light_cost.setValue(unit*quantity)
        self.comboBox_light_names.setCurrentText(self.selected_light['제품명'])

    def ChangeLightQuantity(self):
        unit = self.horizontalSlider_light.value() / 10
        quantity = self.doubleSpinBox_light_quantity.value()
        cost = unit * quantity

        self.doubleSpinBox_light_cost.setValue(cost)

        # 선택 변수 저장
        self.selected_light['갯수'] = quantity
        self.selected_light['비용'] = cost

    def ChangeLightImage(self):
        path = f"C:/sample_python/InEstimate/Img/Lights/{self.selected_light['타입']}_{self.selected_light['제품명']}.jpg"

        # 그래프 이미지 보기
        pixmap = QPixmap()
        pixmap.load(path)
        pixmap = pixmap.scaledToWidth(245)
        self.pix_img.setPixmap(pixmap)


    # ==========================
    # Function
    # ==========================
    # 비용합산
    def cal_cost(self):
        self.cost_total = 0.0

        # 철거
        for key, val in self.items_demol.items():
            if val[0] == True:
                self.cost_total += val[1]

        # 도배
        for key, val in self.items_wallPaper.items():
            if val[0] == True:
                self.cost_total += val[1]

        # VAT
        self.cost_vat = self.cost_total * 0.1


        # VIEW
        self.doubleSpinBox_totalCost.setValue(float(self.cost_total))
        self.doubleSpinBox_vat.setValue(float(self.cost_vat))


    # ==========================
    # Close
    # ==========================
    def closeEvent(self,event):
        pass


    # ==========================
    # Button Func
    # ==========================
    def btnLightAdd(self):
        zone = self.comboBox_light_zone.currentText()
        type = self.comboBox_light_types.currentText()
        name = self.comboBox_light_names.currentText()
        unit = self.horizontalSlider_light.value() / 10
        quantity = self.doubleSpinBox_light_quantity.value()
        cost = unit * quantity

        col = ['구분', '타입', '제품명', '단가', '갯수', '비용']
        data = [zone, type, name, unit, quantity, cost]

        if self.df_lights is None:
            self.df_lights = pd.DataFrame(data=[data], columns=col)
        else:
            add_df = pd.DataFrame(data=[data], columns=col)
            self.df_lights = pd.concat([self.df_lights, add_df], ignore_index=True)

        # 중복합산
        self.df_lights = self.df_lights.groupby(['구분', '타입', '제품명', '단가']).agg(갯수=('갯수', 'sum'), 비용=('비용', 'sum')).reset_index()

        # 총비용
        total_cost = self.df_lights['비용'].sum()
        self.doubleSpinBox_light_cost_total.setValue(total_cost)

        # Table Widget
        self.TableWidgetDf(self.tableWidget_lights, self.df_lights)

    def btnLightMinus(self):
        pass

    def btnLightRefresh(self):
        pass


    # =================================
    # TableWdiget
    # =================================
    # 위젯 DataFrame 쓰기
    def TableWidgetDf(self, widget, df, div='None'):
        # Date
        if div == 'Date':
            cols = df.columns
            if 'Date' not in cols:
                col = ['Date'] + list(cols)
                df['Date'] = df.index

            v = df['Date'].values[0]
            if type(v) != str:
                df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            df = df[cols]

        # 초기화
        widget.clearContents()

        # Setting
        widget.setSelectionMode(QAbstractItemView.SingleSelection)

        widget.setRowCount(len(df.index))
        widget.setColumnCount(len(df.columns))
        try:
            widget.setHorizontalHeaderLabels(df.columns)
            widget.setVerticalHeaderLabels(df.index)
        except:
            pass

        idx = []
        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index, col_index, item)

        # Column ReSize
        for i in range(len(df.columns)):
            widget.resizeColumnToContents(i)


# =======================
# Main
# =======================
if __name__ == "__main__":
    # -------------------------
    # Trading Stock Bot
    # -------------------------
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())