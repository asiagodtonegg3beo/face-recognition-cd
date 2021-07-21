from datetime import datetime
import pandas as pd
import math
import os
os.chdir("C:/Users/90813/Desktop/python策略模組")
exec(open('Order.py',encoding = 'utf8').read())
exec(open('Get_quote.py',encoding = 'utf8').read())

# startTime進場,endTime出場
def HighLowSpread(startTime,endTime,outTime):

　currDate = datetime.now().strftime('%Y-%m-%d')
　startTime = datetime.strptime(currDate +' '+ startTime,'%Y-%m-%d %H:%M:%S.%f')
　endTime = datetime.strptime(currDate +' '+ endTime,'%Y-%m-%d %H:%M:%S.%f')
　outTime = datetime.strptime(currDate +' '+ outTime,'%Y-%m-%d %H:%M:%S.%f')

　#### 定義變數 & 初始化 ####
　print("Initialize......")
　Date=time.strftime("%Y%m%d")
　code = "TXFD8"
　TXF_MatchPrice = ""
　TXF_MatchTime = ""
　BPrice = ""
　SPrice = ""
　BTime = ""
　STime = ""

　BorS = ''
　position = 0
　TradingRecord = pd.DataFrame(columns=['BorS','OpenPrice','ClosePrice','OpenTime','CloseTime','Profit'])
　SingleRecord = pd.DataFrame(columns=['BorS','OpenPrice','ClosePrice','OpenTime','CloseTime','Profit'])
　profit = 0

　high = 0
　low = math.inf
　spread = 0

　#### 設定策略參數 ####
　print("Set the parameter......")

　#設定 單筆下單口數 & 最大在倉口數
　lot = 1
　Maxlot = 1

　#### 執行交易 ####
　print("Calculate indicator.....")

　## 計算指標 {高低點}
　for Mdata in getMatch(code):
　　　## 取得最新報價
　　　currDate = datetime.now().strftime('%Y-%m-%d')
　　　TXF_MatchTime = datetime.strptime(currDate + " " + Mdata.split(",")[1],"%Y-%m-%d %H:%M:%S.%f")
　　　TXF_MatchPrice = Mdata.split(",")[2]

　　　#print(TXF_MatchTime)
　　　#print(TXF_MatchPrice)

　　　indicTime1 = datetime.strptime(currDate +' 08:45:00.00','%Y-%m-%d %H:%M:%S.%f')
　　　indicTime2 = datetime.strptime(currDate +' 09:00:00.00','%Y-%m-%d %H:%M:%S.%f')
　　　if( indicTime1 < TXF_MatchTime < indicTime2 ):
　　　　　if( int(TXF_MatchPrice) > high):
　　　　　　　　high = int(TXF_MatchPrice)
　　　　　if( int(TXF_MatchPrice) < low):
　　　　　　　　low = int(TXF_MatchPrice)
　　　　　if((high-low) > spread):
　　　　　　　　spread = (high-low)
　　　else:
　　　　　print("High:",high," Low:",low," Spread:",spread)
　　　　　break


　print("Open position...........")
　## 進場
　for Mdata in getMatch(code):

　　　## 取得最新報價
　　　currDate = datetime.now().strftime('%Y-%m-%d')
　　　TXF_MatchTime = datetime.strptime(currDate + " " + Mdata.split(",")[1],"%Y-%m-%d %H:%M:%S.%f")
　　　TXF_MatchPrice = Mdata.split(",")[2]

　　　#print(TXF_MatchTime)
　　　#print(TXF_MatchPrice)

　　　## 破高 --> 做多進場
　　　if( startTime < TXF_MatchTime < endTime):
　　　　　if( int(TXF_MatchPrice) > high ):

　　　　　　　OrderMKT(code,"B",str(lot))
　　　　　　　BorS = "B"
　　　　　　　BPrice = TXF_MatchPrice
　　　　　　　BTime = TXF_MatchTime
　　　　　　　position = position + lot
　　　　　　　print("Buy "+ code +" | Buy Price: "+ TXF_MatchPrice +" | Time: "+ datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

　　　## 破低 --> 放空進場
　　　elif( int(TXF_MatchPrice) < low ):

　　　　　　　OrderMKT(code,"S",str(lot))
　　　　　　　BorS = "S"
　　　　　　　SPrice = TXF_MatchPrice
　　　　　　　STime = TXF_MatchTime
　　　　　　　position = position - lot
　　　　　　　print("Sell "+ code +" | Sell Price: "+ TXF_MatchPrice +" | Time: "+ datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
　　　else:
　　　　　break
　　　## 最大口數限制
　　　if abs(position) >= Maxlot : break

　## 出場
　print("Close position...........")
　for Mdata in getMatch(code):

　　　if( position != 0 ):

　　　　　　　## 取得最新報價
　　　　　　　currDate = datetime.now().strftime('%Y-%m-%d')
　　　　　　　TXF_MatchTime = datetime.strptime(currDate + " " + Mdata.split(",")[1],"%Y-%m-%d %H:%M:%S.%f")
　　　　　　　TXF_MatchPrice = Mdata.split(",")[2]

　　　　　　　## 停損 = Spread
　　　　　　　if( position > 0 and (int(BPrice) - int(TXF_MatchPrice)) > spread ):

　　　　　　　　　OrderMKT(code,"S",str(position))
　　　　　　　　　SPrice = TXF_MatchPrice
　　　　　　　　　STime = TXF_MatchTime
　　　　　　　　　position = 0
　　　　　　　　　print("Sell "+code+" | Sell Price: "+TXF_MatchPrice+" | Time: "+datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
　　　　　　　　　break

　　　　　　　elif( position < 0 and (int(TXF_MatchPrice) - int(SPrice)) > spread ):

　　　　　　　　　OrderMKT(code,"B",str(abs(position)))
　　　　　　　　　BPrice = TXF_MatchPrice
　　　　　　　　　BTime = TXF_MatchTime
　　　　　　　　　position = 0
　　　　　　　　　print("Buy "+code+" | Buy Price: "+TXF_MatchPrice+" | Time: "+datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
　　　　　　　　　break


　　　　　　　## 時間到 --> 出場
　　　　　　　if( TXF_MatchTime >= outTime ):

　　　　　　　　　　　if( position > 0 ):
　　　　　　　　　　OrderMKT(code,"S",str(position))
　　　　　　　　　　SPrice = TXF_MatchPrice
　　　　　　　　　　STime = TXF_MatchTime
　　　　　　　　　　position = 0
　　　　　　　　　　print("Sell "+code+" | Sell Price: "+TXF_MatchPrice+" | Time: "+datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
　　　　　　　　　　break
　　　　　　　else:
　　　　　　　　　　OrderMKT(code,"B",str(abs(position)))
　　　　　　　　　　SPrice = TXF_MatchPrice
　　　　　　　　　　STime = TXF_MatchTime
　　　　　　　　　　position = 0
　　　　　　　　　　print("Buy "+code+" | Buy Price: "+TXF_MatchPrice+" | Time: "+datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
　　　　　　　　　　break

　#### 計算損益 ####
　if( SPrice!='' and BPrice!='' ):
　　　　profit = int(SPrice) - int(BPrice)
　　　　print("Profit :" + str(profit))

　## 回傳交易紀錄
　if(BorS == "B"):
　　　SingleRecord = pd.DataFrame({'BorS':"Buy",'OpenPrice':BPrice,'ClosePrice':SPrice,
　　　　　　　　　　　'OpenTime':datetime.strftime(BTime,"%Y-%m-%d %H:%M:%S.%f"),
　　　　　　　　　　　'CloseTime':datetime.strftime(STime,"%Y-%m-%d %H:%M:%S.%f"),
　　　　　　　　　　　'Profit':profit}
　　　　　　　　　　　,index=[0])

　elif(BorS == "S"):
　　　SingleRecord = pd.DataFrame({'BorS':"Sell",'OpenPrice':SPrice,'ClosePrice':BPrice,
　　　　　　　　　　　'OpenTime':datetime.strftime(STime,"%Y-%m-%d %H:%M:%S.%f"),
　　　　　　　　　　　'CloseTime':datetime.strftime(BTime,"%Y-%m-%d %H:%M:%S.%f"),
　　　　　　　　　　　'Profit':profit}
　　　　　　　　　　　,index=[0])
　else:
　　　print("No any signal !")


　TradingRecord = TradingRecord.append([SingleRecord],ignore_index=True)
　#print(TradingRecord)
　return(TradingRecord)



## Testing
Record = HighLowSpread('09:00:00.00','12:00:00.00','13:29:00.00')
Record