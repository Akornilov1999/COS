import math, sys, csv, numpy as np
from pyqtgraph import PlotCurveItem, BarGraphItem, mkPen, setConfigOption
from PyQt5 import QtWidgets, uic
from scipy.io import wavfile
from scipy.signal import iirdesign, filtfilt
from scipy.signal.filter_design import butter
from numpy.fft import fft

setConfigOption('foreground', 0.0)
setConfigOption('background', 1.0)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('MainWindow.ui', self)
        self.setWindowTitle('Цифровая Обработка Сигналов')
        for i in range(6):
            self.number.addItem('Лабораторная работа №' + str(i+1))
        self.number.currentIndexChanged.connect(self.numberChanged)
        self.option.currentIndexChanged.connect(self.optionChanged)
        self.signal = PlotCurveItem()
        self.h = BarGraphItem(x = [], height = [], width = 0)
        self.graphWidget.plotItem.showGrid(True, True, 0.5)
        self.graphWidget.addItem(self.signal)
        self.graphWidget.plotItem.addLegend()
        self.graphWidget2.plotItem.showGrid(True, True, 0.5)
        self.noise = list(np.random.uniform(-1, 1, 10000))
        self.graphWidget2.addItem(self.h)
        self.graphWidget2.plotItem.addLegend()
        self.lab1()
        self.lab2()
        self.lab3()
        self.lab4()
        self.lab5()
        self.lab6()
        self.numberChanged()

    def numberChanged(self):
        if self.number.currentIndex() == 0:
            self.option.currentIndexChanged.disconnect()
            self.option.clear()
            self.option.addItem('Показать весь сигнал')
            self.option.addItem('Показать фрагмент сигнала')
            self.option.currentIndexChanged.connect(self.optionChanged)
            self.optionChanged()
        elif self.number.currentIndex() == 1:
            self.option.currentIndexChanged.disconnect()
            self.option.clear()
            self.option.addItem('Показать весь шум')
            self.option.addItem('Показать фрагмент шума')
            self.option.addItem('Показать плотность распределения шума')
            self.option.currentIndexChanged.connect(self.optionChanged)
            self.optionChanged()
        elif self.number.currentIndex() == 2:
            self.option.currentIndexChanged.disconnect()
            self.option.clear()
            self.option.addItem('Показать весь сигнал + шум')
            self.option.addItem('Показать фрагмент сигнала + шума')
            self.option.currentIndexChanged.connect(self.optionChanged)
            self.optionChanged()
        elif self.number.currentIndex() == 3:
            self.option.currentIndexChanged.disconnect()
            self.option.clear()
            self.option.addItem('Показать спектр сигнала')
            self.option.addItem('Показать фрагмент спектра сигнала')
            self.option.addItem('Показать спектр шума')
            self.option.addItem('Показать фрагмент спектра шума')
            self.option.addItem('Показать спектр сигнала + шума')
            self.option.addItem('Показать фрагмент спектра сигнала + шума')
            self.option.currentIndexChanged.connect(self.optionChanged)
            self.optionChanged()
        elif self.number.currentIndex() == 4:
            self.option.currentIndexChanged.disconnect()
            self.option.clear()
            self.option.addItem('Показать спектр стереосигнала')
            self.option.addItem('Показать спектр сигнала после прохождения через низкочастотный фильтр')
            self.option.addItem('Показать спектр сигнала после прохождения через высокочастотный фильтр')
            self.option.addItem('Показать спектр разностной составляющей после демодуляции сигнала')
            self.option.currentIndexChanged.connect(self.optionChanged)
            self.optionChanged()
        elif self.number.currentIndex() == 5:
            self.option.currentIndexChanged.disconnect()
            self.option.clear()
            self.option.addItem('Показать спектр исходного сигнала')
            self.option.addItem('Показать спектр исходного сигнала с уточнением ширины полосы шумов')
            self.option.addItem('Показать спектральную характеристику отфильтрованного сигнала')
            self.option.addItem('Показать паразитные гармоники')
            self.option.currentIndexChanged.connect(self.optionChanged)
            self.optionChanged()

    def optionChanged(self):
        if self.number.currentIndex() == 0:
            if self.option.currentIndex() == 0:
                self.signal.setData(x=self.points1[0], y=self.points1[1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График сигнала')
            elif self.option.currentIndex() == 1:
                self.signal.setData(x=self.points1[0][:1000], y=self.points1[1][:1000],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График сигнала увеличенный')
            self.graphWidget.plotItem.setLabel('bottom', 't, мс')
            self.graphWidget.plotItem.setLabel('left', 'y, В')
            self.graphWidget.plotItem.legend.removeItem(self.signal)
            self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            self.graphWidget.setVisible(True)
            self.graphWidget.setEnabled(True)
            self.graphWidget2.setVisible(False)
            self.graphWidget2.setEnabled(False)
        elif self.number.currentIndex() == 1:
            if self.option.currentIndex() == 0 or self.option.currentIndex() == 1:
                if self.option.currentIndex() == 0:
                    self.signal.setData(x=self.points2[0], y=self.points2[1],
                                        pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                    self.graphWidget.plotItem.setTitle('График шума')
                if self.option.currentIndex() == 1:
                    self.signal.setData(x=self.points2[0][:1000], y=self.points2[1][:1000],
                                        pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                    self.graphWidget.plotItem.setTitle('График шума увеличенный')
                self.graphWidget.plotItem.setLabel('bottom', 't, мс')
                self.graphWidget.plotItem.setLabel('left', 'y, В')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Noise')
                self.graphWidget.setVisible(True)
                self.graphWidget.setEnabled(True)
                self.graphWidget2.setVisible(False)
                self.graphWidget2.setEnabled(False)
            elif self.option.currentIndex() == 2:
                self.h.setOpts(x=self.count2[0], x0=self.count2[0], height=self.count2[1], width=0.01, pen='k',
                               brush='b')
                self.graphWidget2.plotItem.setTitle('График плотности распределения')
                self.graphWidget2.plotItem.setLabel('bottom', 'x, B')
                self.graphWidget2.plotItem.setLabel('left', 'n')
                self.graphWidget2.plotItem.legend.removeItem(self.h)
                self.graphWidget2.plotItem.legend.addItem(self.h, 'Uniform')
                self.graphWidget.setVisible(False)
                self.graphWidget.setEnabled(False)
                self.graphWidget2.setVisible(True)
                self.graphWidget2.setEnabled(True)
        elif self.number.currentIndex() == 2:
            if self.option.currentIndex() == 0:
                self.signal.setData(x=self.points3[0], y=self.points3[1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График сигнала + шума')
            elif self.option.currentIndex() == 1:
                self.signal.setData(x=self.points3[0][:1000], y=self.points3[1][:1000],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График сигнала + шума увеличенный')
            self.graphWidget.plotItem.setLabel('bottom', 't, мс')
            self.graphWidget.plotItem.setLabel('left', 'y, В')
            self.graphWidget.plotItem.legend.removeItem(self.signal)
            self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal + Noise')
            self.graphWidget.setVisible(True)
            self.graphWidget.setEnabled(True)
            self.graphWidget2.setVisible(False)
            self.graphWidget2.setEnabled(False)
        elif self.number.currentIndex() == 3:
            if self.option.currentIndex() == 0:
                self.signal.setData(x=self.points4[0], y=self.points4[1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График спектра сигнала')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Fft(Signal)')
            elif self.option.currentIndex() == 1:
                self.signal.setData(x=self.points4[0][:1000], y=self.points4[1][:1000],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График спектра сигнала увеличенный')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Fft(Signal)')
            elif self.option.currentIndex() == 2:
                self.signal.setData(x=self.points4[0], y=self.points4[2],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График спектра шума')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Fft(Noise)')
            elif self.option.currentIndex() == 3:
                self.signal.setData(x=self.points4[0][:1000], y=self.points4[2][:1000],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График спектра шума увеличенный')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Fft(Noise)')
            elif self.option.currentIndex() == 4:
                self.signal.setData(x=self.points4[0], y=self.points4[3],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График спектра сигнала + шума')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Fft(Signal + Noise)')
            elif self.option.currentIndex() == 5:
                self.signal.setData(x=self.points4[0][:1000], y=self.points4[3][:1000],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('График спектра сигнала + шума увеличенный')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Fft(Signal + Noise)')
            self.graphWidget.plotItem.setLabel('bottom', 'f, гц')
            self.graphWidget.plotItem.setLabel('left', 'y, В')
            self.graphWidget.setVisible(True)
            self.graphWidget.setEnabled(True)
            self.graphWidget2.setVisible(False)
            self.graphWidget2.setEnabled(False)
        elif self.number.currentIndex() == 4:
            if self.option.currentIndex() == 0:
                self.signal.setData(x=self.x5[int(30000 * len(self.x5) / int(self.x5[len(self.x5) - 1])):int(48000 * len(self.x5) / int(self.x5[len(self.x5) - 1]))],
                # [0:int(math.pow(2, 24) / 2) - 1],
                                    y=self.fft5[2]
                                    # [0:int(math.pow(2, 24) / 2) - 1],
                                    [int(30000 * len(self.x5) / int(self.x5[len(self.x5) - 1])):
                                     int(48000 * len(self.x5) / int(self.x5[len(self.x5) - 1]))],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Спектр стереосигнала')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            elif self.option.currentIndex() == 1:
                self.signal.setData(x=self.x5[0:int(math.pow(2, 24) / 2) - 1],
                                    y=self.fft5[1][0:int(math.pow(2, 24) / 2) - 1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Cпектр сигнала после прохождения через низкочастотный фильтр')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            elif self.option.currentIndex() == 2:
                self.signal.setData(x=self.x5[0:int(math.pow(2, 24) / 2) - 1],
                                    y=self.fft5[2][0:int(math.pow(2, 24) / 2) - 1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Cпектр сигнала после прохождения через высокочастотный фильтр')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            elif self.option.currentIndex() == 3:
                self.signal.setData(x=self.x5[0:int(math.pow(2, 24) / 2) - 1],
                                    y=self.fft5[3][0:int(math.pow(2, 24) / 2) - 1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Спектр разностной составляющей после демодуляции')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            self.graphWidget.plotItem.setLabel('bottom', 'f, гц')
            self.graphWidget.plotItem.setLabel('left', 'y, В');
            self.graphWidget.setVisible(True)
            self.graphWidget.setEnabled(True)
            self.graphWidget2.setVisible(False)
            self.graphWidget2.setEnabled(False)
        elif self.number.currentIndex() == 5:
            if self.option.currentIndex() == 0:
                self.signal.setData(
                    x=self.x6[0:int(math.pow(2, 24) / 2) - 1],
                    y=self.fft6[0][0:int(math.pow(2, 24) / 2) - 1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Спектр исходного сигнала')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            elif self.option.currentIndex() == 1:
                self.signal.setData(
                    x=self.x6[int(8000 * len(self.x6) / int(self.x6[len(self.x6) - 1])):
                                              int(10500 * len(self.x6) / int(self.x6[len(self.x6) - 1]))],
                    y=self.fft6[0][int(8000 * len(self.x6) / int(self.x6[len(self.x6) - 1])):
                                                   int(10500 * len(self.x6) / int(self.x6[len(self.x6) - 1]))],
                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Спектр исходного сигнала с уточнением ширины полосы шумов')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            elif self.option.currentIndex() == 2:
                self.signal.setData(x=self.x6[0:int(math.pow(2, 24) / 2) - 1],
                                    y=self.fft6[1][0:int(math.pow(2, 24) / 2) - 1],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Спектральная характеристика отфильтрованного сигнала')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            elif self.option.currentIndex() == 3:
                self.signal.setData(x=self.x6[int(6200 * len(self.x6) / int(self.x6[len(self.x6) - 1])):
                                              int(6300 * len(self.x6) / int(self.x6[len(self.x6) - 1]))],
                                    y=self.fft6[0][int(6200 * len(self.x6) / int(self.x6[len(self.x6) - 1])):
                                                   int(6300 * len(self.x6) / int(self.x6[len(self.x6) - 1]))],
                                    pen=mkPen(color=(0, 0, 255, 255,), width=2, style=1))
                self.graphWidget.plotItem.setTitle('Паразитные гармоники')
                self.graphWidget.plotItem.legend.removeItem(self.signal)
                self.graphWidget.plotItem.legend.addItem(self.signal, 'Signal')
            self.graphWidget.plotItem.setLabel('bottom', 'f, гц')
            self.graphWidget.plotItem.setLabel('left', 'y, В')
            self.graphWidget.setVisible(True)
            self.graphWidget.setEnabled(True)
            self.graphWidget2.setVisible(False)
            self.graphWidget2.setEnabled(False)

    def lab1(self):
        self.points1 = [[], []]
        with open('lab1//2_signal.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Id', 'Time', 'Value'])
            for i in range(10000):
                self.points1[0].append((i + 1) / 100.0)
                self.points1[1].append(0.2 * math.cos(0.84364 * self.points1[0][i] + 0.17453) + 0.5)
                writer.writerow([str(i + 1), str(self.points1[0][i]), str(self.points1[1][i])])
                if i == 14:
                    print('Лабораторная работа 1:')
                    print(' F(0.15) = ' + str(self.points1[1][i]) + '\n')

    def lab2(self):
        self.points2 = [[]]
        evrg = 0
        sgm = 0
        with open('lab2//2_noise.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Id', 'Time', 'Value'])
            for i in range(10000):
                self.points2[0].append(float(i) / 100)
                writer.writerow([str(i + 1), str(self.points2[0][i]), str(self.noise[i])])
                evrg += self.noise[i] * 0.0001
                sgm += self.noise[i] * self.noise[i] * 0.0001
            sgm += evrg * evrg
        self.points2.append(self.noise)
        self.count2 = [[], []]
        for i in range(101):
            self.count2[0].append(i / 100.0)
            self.count2[1].append(0)
        for i in range(100):
            for j in range(len(self.points2[1])):
                if self.count2[0][i] <= self.points2[1][j] < self.count2[0][i + 1]:
                    self.count2[1][i] += 1
        self.count2[0] = self.count2[0][:100]
        self.count2[1] = self.count2[1][:100]
        print('Лабораторная работа 2:')
        print(' \u00b5 = ' + str(evrg))
        print(' \u03c3\u00b2 = ' + str(sgm) + '\n')

    def lab3(self):
        self.points3 = [[], []]
        signalModule = 0
        noiseModule = 0
        dotSignalNoise = 0
        with open('lab3//2_sn.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Id', 'Time', 'Value'])
            for i in range(10000):
                self.points3[0].append(float(i) / 100)
                self.points3[1].append(self.points1[1][i] + 0.1002374 * self.points2[1][i])
                signalModule += self.points1[1][i] * self.points1[1][i]
                noiseModule += self.points2[1][i] * self.points2[1][i]
                dotSignalNoise += self.points1[1][i] * self.points2[1][i]
                writer.writerow([str(i + 1), str(self.points3[0][i]), str(self.points3[1][i])])
            signalModule = math.sqrt(signalModule)
            noiseModule = math.sqrt(noiseModule)
        print('Лабораторная работа 3:')
        print('Норма сигнала = ' + str(signalModule))
        print('Норма щума = ' + str(noiseModule))
        print('Скалярное произведение сигнала и шума = ' + str(dotSignalNoise))
        print('Косинус = ' + str(dotSignalNoise / (signalModule * noiseModule)) + '\n')

    def lab4(self):
        self.points4 = []
        self.points4.append(np.arange(0, 81.92, 0.01))
        self.points4.append(list(abs(fft(self.points1[1], 8192))))
        self.points4.append(abs(fft(self.points2[1], 8192)))
        self.points4.append(list(abs(fft(self.points3[1], 8192))))
        self.points4.append(list(abs(fft(self.points3[1], 10000))))
        dictionary1 = {}
        dictionary2 = {}
        dictionary3 = {}
        for i in range(len(self.points4[0])):
            if self.points4[1][i] < 2000:
                dictionary1[i + 1] = self.points4[1][i]
            else:
                self.points4[1][i] = 0
        for i in range(len(self.points4[3])):
            if self.points4[3][i] < 2000:
                dictionary2[i + 1] = self.points4[3][i]
            else:
                self.points4[3][i] = 0
        for i in range(len(self.points4[4])):
            if self.points4[4][i] < 2000:
                dictionary3[i + 1] = self.points4[4][i]
            else:
                self.points4[4][i] = 0
        sorted_tuples1 = sorted(dictionary1.items(), key=lambda item: item[1])
        sorted_tuples2 = sorted(dictionary2.items(), key=lambda item: item[1])
        sorted_tuples3 = sorted(dictionary3.items(), key=lambda item: item[1])
        sumSign = (math.pow(sorted_tuples2[len(sorted_tuples2) - 1][1], 2)
                   + math.pow(sorted_tuples2[len(sorted_tuples2) - 2][1], 2))
        sumNoise = 0
        for i in range(len(self.points4[3])):
            sumNoise += math.pow(self.points4[3][i], 2)
        sumNoise -= sumSign
        sumSign2 = (math.pow(sorted_tuples3[len(sorted_tuples3) - 1][1], 2)
                   + math.pow(sorted_tuples3[len(sorted_tuples3) - 2][1], 2))
        sumNoise2 = 0
        for i in range(len(self.points4[4])):
            sumNoise2 += math.pow(self.points4[4][i], 2)
        sumNoise2 -= sumSign2
        print('Лабораторная работа 4:')
        print('1-ая пиковая точка:')
        print('Номер отсчёта: ' + str(sorted_tuples1[len(sorted_tuples1) - 2][0]))
        print('Значение спектра: ' + str(sorted_tuples1[len(sorted_tuples1) - 2][1]))
        print('2-ая пиковая точка:')
        print('Номер отсчёта: ' + str(sorted_tuples1[len(sorted_tuples1) - 1][0]))
        print('Значение спектра: ' + str(sorted_tuples1[len(sorted_tuples1) - 1][1]))
        print('SNR = ' + str(10 * math.log(sumSign / sumNoise, 10)))
        print('При N = 10000 SNR = ' + str(10 * math.log(sumSign2 / sumNoise2, 10)) + '\n')

    def lab5(self):
        self.samplerate5, self.data5 = wavfile.read('lab5//sample2.wav')
        print('Частота дискретизации: ' + str(self.samplerate5))
        self.x5 = np.linspace(0, self.samplerate5, int(math.pow(2, 24)))
        self.fft5 = []
        self.fft5.append(abs(fft(self.data5, int(math.pow(2, 24)))))
        self.s1 = 38247
        self.s2 = 38753
        self.ss = (self.s1 + self.s2) / 2
        d1, d11 = iirdesign(wp=0.2, ws=0.25, gpass=1, gstop=60, ftype='butter')
        self.dataRes = filtfilt(d1, d11, self.data5)
        self.fft5.append(abs(fft(self.dataRes, int(math.pow(2, 24)))))
        d2, d22 = iirdesign(wp=0.25, ws=0.2, gpass=0.5, gstop=60, ftype='butter')
        self.dataResH5 = filtfilt(d2, d22, self.data5)
        self.fft5.append(abs(fft(self.dataResH5, int(math.pow(2, 24)))))
        def demod(dataResH, ss, fs):
            t = np.arange(len(dataResH)) / fs
            dataResHC = dataResH * np.cos(2 * np.pi * ss * t)
            b, a = butter(5, ss * 2 / fs)
            dataResHCos = filtfilt(b, a, dataResHC)
            return dataResHCos
        self.dataResHCos = demod(self.dataResH5, self.ss, self.samplerate5)
        self.dataResCosFiltRazn = filtfilt(d1, d11, self.dataResHCos) * 2
        self.fft5.append(abs(fft(self.dataResCosFiltRazn, int(math.pow(2, 24)))))
        self.s11 = (self.dataRes + self.dataResCosFiltRazn) / 2
        self.s22 = (self.dataRes - self.dataResCosFiltRazn) / 2
        wavfile.write('lab5//2ch1.wav', self.samplerate5, self.s11)
        wavfile.write('lab5//2ch2.wav', self.samplerate5, self.s22)

    def lab6(self):
        self.samplerate6, self.data6 = wavfile.read('lab6//sample2.wav')
        print('Лабораторная работа №6')
        print('Частота дискретизации: ' + str(self.samplerate6) + '\n')
        self.x6 = np.linspace(0, self.samplerate6, int(math.pow(2, 24)))
        self.fft6 = []
        self.fft6.append(abs(fft(self.data6, int(math.pow(2, 24)))))
        d2, d22 = iirdesign(0.2, 0.25, 1, 60, ftype='butter')
        self.dataResH6 = filtfilt(d2, d22, self.data6)
        self.fft6.append(abs(fft(self.dataResH6, int(math.pow(2, 24)))))
        wavfile.write('lab6//2_filt_sample.wav', self.samplerate6, self.dataResH6)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())