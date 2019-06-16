import talib as ta
import numpy as np
import pandas as pd

"""
将macd策略需要用到的信号生成器抽离出来
"""

class macdSignalClass():

    def __init__(self):
        self.author = 'JerryLam'

    def maEnvironment(self, am, paraDict):
        envPeriod = paraDict["envPeriod"]

        envMa = ta.MA(am.close, envPeriod)
        envDirection = 1 if am.close[-1]>envMa[-1] else -1
        return envDirection, envMa


    def macdCross(self,am,paraDict):

        fastPeriod = paraDict["fastPeriod"]
        slowPeriod = paraDict["slowPeriod"]
        signalPeriod = paraDict["signalPeriod"]

        macd,macdSignal,macdHist = ta.MACD(am.close,fastPeriod,slowPeriod,signalPeriod)

        goldenCross = (macd[-1]>macdSignal[-1] and macd[-2]<=macdSignal[-2] and macdHist>=0)
        deathCross = (macd[-1]<macdSignal[-1] and macd[-2]>=macdSignal[-2] and macdHist<=0)

        macdCrossSignal = 0
        if goldenCross:
            macdCrossSignal = 1
        elif deathCross:
            macdCrossSignal = -1
        else:
            macdCrossSignal = 0
        return macdCrossSignal,macd,macdSignal,macdHist