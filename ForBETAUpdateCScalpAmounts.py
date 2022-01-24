import sys, os, shutil, time, requests, math, psutil

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore

import design


def my_round(var, size):
    result = ((var * 100000) // (size * 100000)) * size
    if size >= 1:
        return math.floor(result)
    else:
        return math.floor(result * 100000) / 100000


class MyApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    global CODE_FTXFutures
    global LEVERAGE_FTXFutures
    global DEPO_FTXFutures
    global PART1_FTXFutures
    global PART2_FTXFutures
    global PART3_FTXFutures
    global PART4_FTXFutures
    global PART5_FTXFutures

    global CODE_BinanceFutures
    global LEVERAGE_BinanceFutures
    global DEPO_BinanceFutures
    global PART1_BinanceFutures
    global PART2_BinanceFutures
    global PART3_BinanceFutures
    global PART4_BinanceFutures
    global PART5_BinanceFutures

    global CODE_FTXSpot
    global LEVERAGE_FTXSpot
    global DEPO_FTXSpot
    global CURRENCY_FTXSpot
    global PART1_FTXSpot
    global PART2_FTXSpot
    global PART3_FTXSpot
    global PART4_FTXSpot
    global PART5_FTXSpot

    global AMOUNTS_CAN_BE_EDITED

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.pushButton.clicked.connect(self.updateAmounts)
        self.pushButtonAbout.clicked.connect(self.showDialog)

        self.comboBox.addItem('FTX: Бессрочные фьючерсы')
        self.comboBox.addItem('FTX: Спот')
        self.comboBox.addItem('Binance: Бессрочные фьючерсы')
        # self.comboBox.addItem('Binance: Спот')

        self.comboBoxCurrency.addItem('USD')
        self.comboBoxCurrency.addItem('USDT')

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Price", "V1", "V2", "V3 ", "V4", "V5"])
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(2)
        self.tableWidget.resizeColumnToContents(3)
        self.tableWidget.resizeColumnToContents(4)
        self.tableWidget.resizeColumnToContents(5)
        self.tableWidget.resizeColumnToContents(6)
        self.change_mode()

        self.CODE_FTXFutures = ''
        self.LEVERAGE_FTXFutures = '20'
        self.DEPO_FTXFutures = '0'
        self.PART1_FTXFutures = '0'
        self.PART2_FTXFutures = '0'
        self.PART3_FTXFutures = '0'
        self.PART4_FTXFutures = '0'
        self.PART5_FTXFutures = '0'

        self.CODE_BinanceFutures = ''
        self.LEVERAGE_BinanceFutures = '1'
        self.DEPO_BinanceFutures = '0'
        self.PART1_BinanceFutures = '0'
        self.PART2_BinanceFutures = '0'
        self.PART3_BinanceFutures = '0'
        self.PART4_BinanceFutures = '0'
        self.PART5_BinanceFutures = '0'

        self.CODE_FTXSpot = ''
        self.LEVERAGE_FTXSpot = '1'
        self.DEPO_FTXSpot = '0'
        self.CURRENCY_FTXSpot = 'USD'
        self.PART1_FTXSpot = '0'
        self.PART2_FTXSpot = '0'
        self.PART3_FTXSpot = '0'
        self.PART4_FTXSpot = '0'
        self.PART5_FTXSpot = '0'

        self.AMOUNTS_CAN_BE_EDITED = ''

        if os.path.exists('config.ini'):
            with open('config.ini', "r") as f:
                data = f.read()
                self.CODE_FTXFutures = data.split('\n', 40)[0]
                self.LEVERAGE_FTXFutures = data.split('\n', 40)[1]
                self.DEPO_FTXFutures = data.split('\n', 40)[2]
                self.PART1_FTXFutures = data.split('\n', 40)[3]
                self.PART2_FTXFutures = data.split('\n', 40)[4]
                self.PART3_FTXFutures = data.split('\n', 40)[5]
                self.PART4_FTXFutures = data.split('\n', 40)[6]
                self.PART5_FTXFutures = data.split('\n', 40)[7]

                self.CODE_BinanceFutures = data.split('\n', 40)[8]
                self.LEVERAGE_BinanceFutures = data.split('\n', 40)[9]
                self.DEPO_BinanceFutures = data.split('\n', 40)[10]
                self.PART1_BinanceFutures = data.split('\n', 40)[11]
                self.PART2_BinanceFutures = data.split('\n', 40)[12]
                self.PART3_BinanceFutures = data.split('\n', 40)[13]
                self.PART4_BinanceFutures = data.split('\n', 40)[14]
                self.PART5_BinanceFutures = data.split('\n', 40)[15]

                self.CODE_FTXSpot = data.split('\n', 40)[16]
                self.LEVERAGE_FTXSpot = data.split('\n', 40)[17]
                self.DEPO_FTXSpot = data.split('\n', 40)[18]
                self.CURRENCY_FTXSpot = data.split('\n', 40)[19]
                self.PART1_FTXSpot = data.split('\n', 40)[20]
                self.PART2_FTXSpot = data.split('\n', 40)[21]
                self.PART3_FTXSpot = data.split('\n', 40)[22]
                self.PART4_FTXSpot = data.split('\n', 40)[23]
                self.PART5_FTXSpot = data.split('\n', 40)[24]

                self.AMOUNTS_CAN_BE_EDITED = data.split('\n', 40)[25]

        else:
            self.listWidget.addItem('Ошибка! Файл config.ini не найден')

        self.combobox_changed()
        self.listWidget.addItem('ВНИМАНИЕ! Закройте CScalp перед выполнением.')

        if self.CURRENCY_FTXSpot == 'USD':
            self.comboBoxCurrency.setCurrentIndex(0)
        elif self.CURRENCY_FTXSpot == 'USDT':
            self.comboBoxCurrency.setCurrentIndex(1)

        # CONNECTIONS
        self.comboBox.currentIndexChanged.connect(self.combobox_changed)
        self.comboBoxCurrency.currentIndexChanged.connect(self.combobox_currency_changed)
        self.editCode.textChanged.connect(self.edit_code_changed)
        self.editLeverage.textChanged.connect(self.edit_leverage_changed)
        self.editPart1.textChanged.connect(self.edit_part1_changed)
        self.editPart2.textChanged.connect(self.edit_part2_changed)
        self.editPart3.textChanged.connect(self.edit_part3_changed)
        self.editPart4.textChanged.connect(self.edit_part4_changed)
        self.editPart5.textChanged.connect(self.edit_part5_changed)
        self.editDepo.textChanged.connect(self.edit_depo_changed)
        self.radioButton.toggled.connect(self.change_mode)
        self.radioButton_2.toggled.connect(self.change_mode)

        if self.AMOUNTS_CAN_BE_EDITED == 'TRUE':
            self.pushButton.setEnabled(True)
            self.label_9.setVisible(True)
            self.editCode.setVisible(True)
            self.radioButton_2.setEnabled(True)
        else:
            self.pushButton.setEnabled(True)
            self.label_9.setVisible(False)
            self.editCode.setVisible(False)
            self.radioButton_2.setEnabled(False)

    def change_mode(self):
        if self.radioButton.isChecked():
            self.listWidget.setVisible(False)
            self.tableWidget.setVisible(True)
            self.pushButton.setText('Рассчитать объемы')
            self.pushButton.setEnabled(True)

        if self.radioButton_2.isChecked():
            self.listWidget.setVisible(True)
            self.tableWidget.setVisible(False)
            self.pushButton.setText('Обновить объемы в стаканах (Осторожно!)')
            # if self.AMOUNTS_CAN_BE_EDITED == 'TRUE':
            #     self.pushButton.setEnabled(True)
            # else:
            #     self.pushButton.setEnabled(False)

    def edit_code_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.CODE_FTXFutures = self.editCode.text()
        elif self.comboBox.currentIndex() == 1:
            self.CODE_FTXSpot = self.editCode.text()
        elif self.comboBox.currentIndex() == 2:
            self.CODE_BinanceFutures = self.editCode.text()

    def edit_leverage_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.LEVERAGE_FTXFutures = self.editLeverage.text()
        elif self.comboBox.currentIndex() == 1:
            self.LEVERAGE_FTXSpot = self.editLeverage.text()
        elif self.comboBox.currentIndex() == 2:
            self.LEVERAGE_BinanceFutures = self.editLeverage.text()

    def edit_depo_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.DEPO_FTXFutures = self.editDepo.text()
        elif self.comboBox.currentIndex() == 1:
            self.DEPO_FTXSpot = self.editDepo.text()
        elif self.comboBox.currentIndex() == 2:
            self.DEPO_BinanceFutures = self.editDepo.text()

    def edit_part1_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.PART1_FTXFutures = self.editPart1.text()
        elif self.comboBox.currentIndex() == 1:
            self.PART1_FTXSpot = self.editPart1.text()
        elif self.comboBox.currentIndex() == 2:
            self.PART1_BinanceFutures = self.editPart1.text()

    def edit_part2_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.PART2_FTXFutures = self.editPart2.text()
        elif self.comboBox.currentIndex() == 1:
            self.PART2_FTXSpot = self.editPart2.text()
        elif self.comboBox.currentIndex() == 2:
            self.PART2_BinanceFutures = self.editPart2.text()

    def edit_part3_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.PART3_FTXFutures = self.editPart3.text()
        elif self.comboBox.currentIndex() == 1:
            self.PART3_FTXSpot = self.editPart3.text()
        elif self.comboBox.currentIndex() == 2:
            self.PART3_BinanceFutures = self.editPart3.text()

    def edit_part4_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.PART4_FTXFutures = self.editPart4.text()
        elif self.comboBox.currentIndex() == 1:
            self.PART4_FTXSpot = self.editPart4.text()
        elif self.comboBox.currentIndex() == 2:
            self.PART4_BinanceFutures = self.editPart4.text()

    def edit_part5_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.PART5_FTXFutures = self.editPart5.text()
        elif self.comboBox.currentIndex() == 1:
            self.PART5_FTXSpot = self.editPart5.text()
        elif self.comboBox.currentIndex() == 2:
            self.PART5_BinanceFutures = self.editPart5.text()

    def combobox_currency_changed(self):
        self.CURRENCY_FTXSpot = self.comboBoxCurrency.currentText()

    def combobox_changed(self):
        self.listWidget.clear()
        self.comboBoxCurrency.setVisible(False)
        self.label_10.setVisible(False)

        if self.comboBox.currentIndex() == 3:
            self.listWidget.addItem('Режим [' + self.comboBox.currentText() + '] находится в разработке')
            self.pushButton.setEnabled(False)
        else:
            self.listWidget.addItem('Установлен режим [' + self.comboBox.currentText() + ']')
            self.pushButton.setEnabled(True)

        if self.comboBox.currentIndex() == 0:
            self.editCode.setText(self.CODE_FTXFutures)
            self.editLeverage.setText(self.LEVERAGE_FTXFutures)
            self.editPart1.setText(self.PART1_FTXFutures)
            self.editPart2.setText(self.PART2_FTXFutures)
            self.editPart3.setText(self.PART3_FTXFutures)
            self.editPart4.setText(self.PART4_FTXFutures)
            self.editPart5.setText(self.PART5_FTXFutures)
            self.editDepo.setText(self.DEPO_FTXFutures)

        elif self.comboBox.currentIndex() == 1:
            self.editCode.setText(self.CODE_FTXSpot)
            self.editLeverage.setText(self.LEVERAGE_FTXSpot)
            self.editPart1.setText(self.PART1_FTXSpot)
            self.editPart2.setText(self.PART2_FTXSpot)
            self.editPart3.setText(self.PART3_FTXSpot)
            self.editPart4.setText(self.PART4_FTXSpot)
            self.editPart5.setText(self.PART5_FTXSpot)
            self.editDepo.setText(self.DEPO_FTXSpot)

            if self.CURRENCY_FTXSpot == 'USD':
                self.comboBoxCurrency.setCurrentIndex(0)
            elif self.CURRENCY_FTXSpot == 'USDT':
                self.comboBoxCurrency.setCurrentIndex(1)

            self.comboBoxCurrency.setVisible(True)
            self.label_10.setVisible(True)

        elif self.comboBox.currentIndex() == 2:
            self.editCode.setText(self.CODE_BinanceFutures)
            self.editLeverage.setText(self.LEVERAGE_BinanceFutures)
            self.editPart1.setText(self.PART1_BinanceFutures)
            self.editPart2.setText(self.PART2_BinanceFutures)
            self.editPart3.setText(self.PART3_BinanceFutures)
            self.editPart4.setText(self.PART4_BinanceFutures)
            self.editPart5.setText(self.PART5_BinanceFutures)
            self.editDepo.setText(self.DEPO_BinanceFutures)

        if (self.comboBox.currentIndex() == 1) or (self.comboBox.currentIndex() == 3):
            self.editLeverage.setEnabled(False)
        else:
            self.editLeverage.setEnabled(True)

    def closeEvent(self, event):
        with open('config.ini', "w") as f:
            f.write(self.CODE_FTXFutures + '\n')
            f.write(self.LEVERAGE_FTXFutures + '\n')
            f.write(self.DEPO_FTXFutures + '\n')
            f.write(self.PART1_FTXFutures + '\n')
            f.write(self.PART2_FTXFutures + '\n')
            f.write(self.PART3_FTXFutures + '\n')
            f.write(self.PART4_FTXFutures + '\n')
            f.write(self.PART5_FTXFutures + '\n')

            f.write(self.CODE_BinanceFutures + '\n')
            f.write(self.LEVERAGE_BinanceFutures + '\n')
            f.write(self.DEPO_BinanceFutures + '\n')
            f.write(self.PART1_BinanceFutures + '\n')
            f.write(self.PART2_BinanceFutures + '\n')
            f.write(self.PART3_BinanceFutures + '\n')
            f.write(self.PART4_BinanceFutures + '\n')
            f.write(self.PART5_BinanceFutures + '\n')

            f.write(self.CODE_FTXSpot + '\n')
            f.write(self.LEVERAGE_FTXSpot + '\n')
            f.write(self.DEPO_FTXSpot + '\n')
            f.write(self.CURRENCY_FTXSpot + '\n')
            f.write(self.PART1_FTXSpot + '\n')
            f.write(self.PART2_FTXSpot + '\n')
            f.write(self.PART3_FTXSpot + '\n')
            f.write(self.PART4_FTXSpot + '\n')
            f.write(self.PART5_FTXSpot + '\n')

            f.write(self.AMOUNTS_CAN_BE_EDITED + '\n')

    def write_to_file(self, mvs_dir, account_code, ex_prefix, ticker, depo, price, size, punkti, part1, part2, part3, part4, part5, count_tickers):
        volume_max = float(depo) / float(price)
        size = float(size)
        part1 = float(part1)
        part2 = float(part2)
        part3 = float(part3)
        part4 = float(part4)
        part5 = float(part5)
        vol1 = my_round(volume_max * part1 / 100, size)
        vol2 = my_round(volume_max * part2 / 100, size)
        vol3 = my_round(volume_max * part3 / 100, size)
        vol4 = my_round(volume_max * part4 / 100, size)
        vol5 = my_round(volume_max * part5 / 100, size)

        dollars_ticks_from = 20000
        show_ticks_from = round(dollars_ticks_from / float(price))

        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(count_tickers - 1, 0, QTableWidgetItem(ticker))
        self.tableWidget.setItem(count_tickers - 1, 1, QTableWidgetItem(str(price)))
        self.tableWidget.setItem(count_tickers - 1, 2, QTableWidgetItem(str(vol1)))
        self.tableWidget.setItem(count_tickers - 1, 3, QTableWidgetItem(str(vol2)))
        self.tableWidget.setItem(count_tickers - 1, 4, QTableWidgetItem(str(vol3)))
        self.tableWidget.setItem(count_tickers - 1, 5, QTableWidgetItem(str(vol4)))
        self.tableWidget.setItem(count_tickers - 1, 6, QTableWidgetItem(str(vol5)))


        if self.radioButton_2.isChecked():
            filename = ex_prefix + ticker + '_Settings_' + account_code + '.tmp'
            fullname = mvs_dir + '\\' + filename
            if os.path.exists(fullname):

                with open(fullname, "r") as f, open('temp.txt', "w") as f2:
                    lines = f.readlines()

                    for line in lines:

                        st = str(line)

                        if (st.find('<First_WorkAmount Value=') != -1) and (part1 != 0):
                            f2.write('    <First_WorkAmount Value="' + str(vol1) + '" />\n')

                        elif (st.find('<Second_WorkAmount Value=') != -1) and (part2 != 0):
                            f2.write('    <Second_WorkAmount Value="' + str(vol2) + '" />\n')

                        elif (st.find('<Third_WorkAmount Value=') != -1) and (part3 != 0):
                            f2.write('    <Third_WorkAmount Value="' + str(vol3) + '" />\n')

                        elif (st.find('<Fourth_WorkAmount Value=') != -1) and (part4 != 0):
                            f2.write('    <Fourth_WorkAmount Value="' + str(vol4) + '" />\n')

                        elif (st.find('<Fifth_WorkAmount Value=') != -1) and (part5 != 0):
                            f2.write('    <Fifth_WorkAmount Value="' + str(vol5) + '" />\n')

                        elif st.find('<SlimLevelsFactor Value=')  != -1:
                            f2.write('    <SlimLevelsFactor Value="'  + str(1*punkti) +'" />\n')

                        #elif st.find('<RulerDataType Value=')  != -1:
                        #    f2.write('    <RulerDataType Value="2" />\n')

                        #elif st.find('<FatLevelsFactor Value=')  != -1:
                        #    f2.write('    <FatLevelsFactor Value="'  + str(10*punkti) +'" />\n')

                        # elif st.find('<SumTicks_Period Value=')  != -1:
                        #     f2.write('    <SumTicks_Period Value="500" />\n')
                        #
                        # elif st.find('<HideFilteredTicks Value=')  != -1:
                        #      f2.write('    <HideFilteredTicks Value="True" />\n')
                        #
                        # elif st.find('<PlaySoundOnTrade Value=')  != -1:
                        #     f2.write('    <PlaySoundOnTrade Value="True" />\n')

                        # elif st.find('<ShowTicksFrom Value=')  != -1:
                        #     f2.write('    <ShowTicksFrom Value="' + str(show_ticks_from) + '" />\n')

                        else:
                            f2.write(line)

                with open(fullname, "w") as f, open('temp.txt', "r") as f2:
                    new_data = f2.read()
                    f.write(new_data)

                f.close()
                f2.close()
                os.remove('temp.txt')

                if part1 == 0:
                    vol1 = 'X'

                if part2 == 0:
                    vol2 = 'X'

                if part3 == 0:
                    vol3 = 'X'

                if part4 == 0:
                    vol4 = 'X'

                if part5 == 0:
                    vol5 = 'X'

                round_st = ticker + ' ($' + str(price) + ') ' + str(vol1) + ' ' + str(vol2) + ' ' + str(
                    vol3) + ' ' + str(vol4) + ' ' + str(vol5)

                self.listWidget.addItem(round_st)

                return True

            else:
                self.listWidget.addItem('Файл с настройками для инструмента ' + ticker + ' не найден')
                return False


    def updateAmounts(self):

        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.listWidget.clear()
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Price", "V1", "V2", "V3", "V4", "V5"])
        self.tableWidget.setRowCount(0)


        thereIsError = False

        if self.radioButton_2.isChecked():
            for proc in psutil.process_iter():
                name = proc.name()
                if name == "CryptoScalp.exe":
                    self.listWidget.addItem('Ошибка! Запущен CScalp - выполнение невозможно.')
                    self.setCursor(QtGui.QCursor())
                    return

        try:
            depo = float(self.editDepo.text())
        except ValueError:
            self.listWidget.addItem('Ошибка! Некорректное значение депозита')
            thereIsError = True

        LEVERAGE = 0
        if not self.editLeverage.text().isdigit():
            self.listWidget.addItem('Ошибка! Некорректное значение плеча')
            thereIsError = True
        else:
            LEVERAGE = float(self.editLeverage.text())

        try:
            PART1 = float(self.editPart1.text())
        except ValueError:
            self.listWidget.addItem('Ошибка! Некорректное значение объема 1')
            thereIsError = True

        try:
            PART2 = float(self.editPart2.text())
        except ValueError:
            self.listWidget.addItem('Ошибка! Некорректное значение объема 2')
            thereIsError = True

        try:
            PART3 = float(self.editPart3.text())
        except ValueError:
            self.listWidget.addItem('Ошибка! Некорректное значение объема 3')
            thereIsError = True

        try:
            PART4 = float(self.editPart4.text())
        except ValueError:
            self.listWidget.addItem('Ошибка! Некорректное значение объема 4')
            thereIsError = True

        try:
            PART5 = float(self.editPart5.text())
        except ValueError:
            self.listWidget.addItem('Ошибка! Некорректное значение объема 5')
            thereIsError = True

        if thereIsError:
            self.setCursor(QtGui.QCursor())
            return

        #MVS_DIR = os.getenv('APPDATA') + '\CScalp\Visualizer\mvs_cs'
        MVS_DIR = 'C:\Program Files (x86)\FSR Launcher (beta)\SubApps\CScalp\Data\MVS'
        root_src_dir = MVS_DIR
        root_dst_dir = r'backup\backup ' + str(time.time())

        self.listWidget.addItem('Текущее UNIX-время: ' + str(time.time()))
        self.listWidget.addItem('Каталог с настройками: ' + root_src_dir)

        if self.radioButton_2.isChecked():
            for src_dir, dirs, files in os.walk(root_src_dir):
                dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)

                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.copy(src_file, dst_dir)

            self.listWidget.addItem('Сформирована резервная копия настроек: ' + root_dst_dir)

        number_updated_files = 0
        number_skipped_tickers = 0
        count_tickers = 0

        #  FTX Futures
        if self.comboBox.currentIndex() == 0:
            ex_prefix = 'FTXD.FUT.'
            api_endpoint = "https://ftx.com/api/futures"

            try:
                json_data = requests.get(api_endpoint).json()
            except:
                self.listWidget.addItem('Ошибка! Не удалось выполнить подключение к бирже.')
                self.setCursor(QtGui.QCursor())
                return

            depo = float(self.DEPO_FTXFutures) * float(self.LEVERAGE_FTXFutures)

            for item in json_data['result']:
                if (item['expiryDescription'] == 'Perpetual'):

                    ticker = item['name']
                    price = item['bid']
                    size = item['sizeIncrement']
                    priceIncrement = float(item['priceIncrement'])
                    PriceAggregationStep = 10
                    punkti = math.ceil((price * 0.0007) / (PriceAggregationStep * priceIncrement))

                    count_tickers += 1
                    if self.write_to_file(MVS_DIR, self.CODE_FTXFutures, ex_prefix, ticker, depo, price, size, punkti,
                                          self.PART1_FTXFutures, self.PART2_FTXFutures,
                                          self.PART3_FTXFutures, self.PART4_FTXFutures,
                                          self.PART5_FTXFutures, count_tickers):
                        number_updated_files += 1
                    else:
                        number_skipped_tickers += 1

        #  FTX Spot
        if self.comboBox.currentIndex() == 1:
            ex_prefix = 'FTXD.SPOT.'
            api_endpoint = "https://ftx.com/api/markets"

            try:
                json_data = requests.get(api_endpoint).json()
            except:
                self.listWidget.addItem('Ошибка! Не удалось выполнить подключение к бирже.')
                self.setCursor(QtGui.QCursor())
                return

            depo = float(self.DEPO_FTXSpot)

            for item in json_data['result']:
                if (item['type'] == 'spot') and (item['name'].endswith(self.CURRENCY_FTXSpot)):

                    ticker = item['name'].replace('/','')
                    price = item['bid']
                    size = item['sizeIncrement']
                    priceIncrement = float(item['priceIncrement'])
                    PriceAggregationStep = 10
                    punkti = math.ceil((price * 0.0007) / (1 * priceIncrement))
                    count_tickers += 1
                    if self.write_to_file(MVS_DIR, self.CODE_FTXSpot, ex_prefix, ticker, depo, price, size, punkti,
                                          self.PART1_FTXSpot, self.PART2_FTXSpot,
                                          self.PART3_FTXSpot, self.PART4_FTXSpot,
                                          self.PART5_FTXSpot, count_tickers):
                        number_updated_files += 1
                    else:
                        number_skipped_tickers += 1

        #  Binance Futures
        elif self.comboBox.currentIndex() == 2:

            ex_prefix = 'BINAD.CCUR_FUT.'
            api_endpoint_exchange = "https://binance.com/fapi/v1/exchangeInfo"
            api_endpoint_premiumIndex = "https://binance.com/fapi/v1/premiumIndex"

            try:
                json_data_exchange = requests.get(api_endpoint_exchange).json()
                json_data_premiumIndex = requests.get(api_endpoint_premiumIndex).json()
            except:
                self.listWidget.addItem('Ошибка! Не удалось выполнить подключение к бирже.')
                self.setCursor(QtGui.QCursor())
                return

            depo = float(self.DEPO_BinanceFutures) * float(self.LEVERAGE_BinanceFutures)

            for item in json_data_exchange['symbols']:
                ticker = item['symbol']
                for filter in item['filters']:
                    if filter['filterType'] == 'LOT_SIZE':
                        size = filter['stepSize']
                for item_prices in json_data_premiumIndex:
                    if item_prices['symbol'] == ticker:
                        price = item_prices['markPrice']

                        count_tickers += 1
                        if self.write_to_file(MVS_DIR, self.CODE_BinanceFutures, ex_prefix, ticker, depo, price, size, 0,
                                              self.PART1_BinanceFutures, self.PART2_BinanceFutures,
                                              self.PART3_BinanceFutures, self.PART4_BinanceFutures,
                                              self.PART5_BinanceFutures, count_tickers):
                            number_updated_files += 1
                        else:
                            number_skipped_tickers += 1

        self.listWidget.addItem(str(number_updated_files) + ' файлов обновлено')
        self.listWidget.addItem(str(number_skipped_tickers) + ' инструментов пропущено')

        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(2)
        self.tableWidget.resizeColumnToContents(3)
        self.tableWidget.resizeColumnToContents(4)
        self.tableWidget.resizeColumnToContents(5)
        self.tableWidget.resizeColumnToContents(6)

        self.setCursor(QtGui.QCursor())

    def showDialog(self):
        QMessageBox.about(self, "О программе",
                          "UpdateCScalpAmounts v0.1.5\n\nПрограмма подключается к бирже FTX или Binance, "
                          "где получает список инструментов с текущими ценами.\n\nИсходя из цены "
                          "инструмента, значений депозита, плеча и пропорций" +
                          " расcчитываются объемы.\n\nНастройки стаканов перезаписываются в папке"
                          "\nC:\\Users\\ИМЯ_ПОЛЬЗОВАТЕЛЯ\\\nAppData\\Roaming\\CScalp\\Visualizer\\mvs_cs\n"
                          "В *.tmp-файлах заменяются значения параметров First|Second|Third|Fourth|Fifth_WorkAmount. "
                          "Перед перезаписью настройки стаканов сохраняются в папку backup.\n\n" +
                          "В случае, если вы хотите оставить нетронутыми какие-то объемы в стаканах, то поставьте 0 "
                          "в соответствующем поле."
                          "\n\n FTX: Бессрочные фьючерсы\n/api/futures (цена bid)"
                          "\n\n FTX: Спот\n/api/markets (цена bid)"
                          "\n\nBinance: Бессрочные фьючерсы\n/fapi/v1/exchangeInfo\n/fapi/v1/premiumIndex (цена markPrice)"
                          "\n\nКонтакты:\nt.me/s1esarev\nL1FT@yandex.ru"
                          )


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
