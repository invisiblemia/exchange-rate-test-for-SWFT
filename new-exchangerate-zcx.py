from openpyxl import Workbook
import os
import time
import re
import requests
import json
class rate_test():
    def __init__(self, **_):
        self.headers={'Content-Type':'application/json;charset=UTF-8',
               'Referer':'https://test.swftcoin.com/swft-v3/swft-v3-pc/login.html',
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    #用户登陆加载cookies和存储session
    def swft_session(self):
        swftlogin_url='https://test.swftcoin.com/accountapi/login_web'
        login_payload={"equipmentNo":"QM8BF1tXTnpqMQyZ4b4bn8K9qL2Va6xb",
        "sessionUuid":"","sourceType":"H5","userNo":'1211024726@qq.com',"userPassword":'1qaz2wsx'}
        swftloginSession = requests.session()
        swftlogin_req1=swftloginSession.post(swftlogin_url,data=json.dumps(login_payload),headers=self.headers).text
        swftlogin_req2=json.loads(swftlogin_req1)
        return swftloginSession

    def queryCoinList(self):
        queryCoinListUrl='https://test.swftcoin.com/api/v1/queryCoinList'
        queryCoinList_payload={}
        session=self.swft_session()
        res1=session.post(queryCoinListUrl, data=json.dumps(queryCoinList_payload), headers=self.headers, allow_redirects=False).text
        res2 = json.loads(res1)
        # global queryCoinList
        # queryCoinList = res2
        # # print(queryCoinList)
        # global num
        # num = len(queryCoinList['data'])
        return res2
        # print(num)

    def getBaseInfo(self, upper_dep, upper_rec):
        baseInfoUrl='https://test.swftcoin.com/api/v3/getBaseInfo'
        baseInfo_payload={'depositCoinCode': upper_dep,
                            'receiveCoinCode': upper_rec
                        }
        session = self.swft_session()
        res1 = session.post(baseInfoUrl, data=json.dumps(baseInfo_payload), headers=self.headers, allow_redirects=False).text
        res2 = json.loads(res1)

        result = {}
        try:
            # global depCoininstantRate
            depCoininstantRate = res2['data']['instantRate']['depositCoinDepth']
            result.update({"depCoininstantRate": depCoininstantRate})
            # for i in range(len(depCoininstantRate)):
            #     print(depCoininstantRate[i])
            # global depositMax
            depositMax = float(res2['data']['depositMax'])
            result.update({"depositMax": depositMax})
            # global depositMin
            depositMin = float(res2['data']['depositMin'])
            result.update({"depositMin": depositMin})
        except:
            print(res2)
            # currentlist.append(res2['resMsg'])

        try:
            # global recCoininsantRate
            recCoininsantRate = res2['data']['instantRate']['receiveCoinDepth']
            result.update({"recCoininsantRate": recCoininsantRate})
        #print(recCoininsantRate)
            # for i in range(len(recCoininsantRate)):
            #     print(recCoininsantRate[i])
        except:
            print(res2)

        return result

    def exchangeAm(self, depositMax, depositMin):
        try:
            # global exchangeAmount
            exchangeAmount = (depositMax-depositMin)/5+depositMin
            # print('存币数量:',exchangeAmount)
            # currentlist.append(exchangeAmount)
            return exchangeAmount
        except:
            print('原因参见上条')
            currentlist.append('原因参见上条')

        # global exchangeAmount
        # exchangeAmount=float(input('存入币种兑换值:'))#需要定义
        # print('存入币种兑换值:',exchangeAmount)
        #判断存入币种深度及汇率
        return

    def exchangeRate(self, params, exchangeAmount):
        depCoininstantRate = params['depCoininstantRate']
        recCoininsantRate = params['recCoininsantRate']
        try:
            if exchangeAmount > depCoininstantRate[len(depCoininstantRate)-1][1]:
                print('超出存币范围1')
                #curentlist.append('超出存币范围1')
            else:#存币开始是数量校验
                for amount in range(len(depCoininstantRate)):
                    if exchangeAmount<=depCoininstantRate[amount][1]:
                        global exchangeRate1
                        exchangeRate1=depCoininstantRate[amount][0]
                        global Amount1
                        Amount1=exchangeRate1*exchangeAmount
                        print('存币币种汇率:',exchangeRate1)
                        currentlist.append(exchangeRate1)
                        break
                    else:
                        continue
                try:
                    if Amount1>recCoininsantRate[len(recCoininsantRate)-1][2]:
                        print('超出存币范围2')
                        currentlist.append('超出存币范围2')
                    else:
                        for amount in range(len(recCoininsantRate)):
                            if Amount1<recCoininsantRate[amount][2]:
                                global exchangeRate2
                                exchangeRate2=recCoininsantRate[amount][0]
                                print('目标币种汇率:',exchangeRate2)
                                currentlist.append(exchangeRate2)
                                break
                            else:
                                continue
                        global rate
                        rate=exchangeRate1/exchangeRate2
                        currentlist.append(rate)
                        print(rate)
                        return rate
                except:
                    print('无法交易1')
                    currentlist.append('无法交易1')
                    return "null"
        except:
            print('无法交易2')
            currentlist.append('无法交易2')
            return "null"

    def realBaseinfo(self, upper_dep, upper_rec):
        realBaseinforUrl = 'https://transfer.swft.pro/api/v1/getBaseInfo'
        realBaseinfor_payload = {'depositCoinCode': upper_dep,
                                'receiveCoinCode': upper_rec
                                }
        session = self.swft_session()
        res1 = session.post(realBaseinforUrl,
                            data=json.dumps(realBaseinfor_payload), headers=self.headers, allow_redirects=False).text
        res2 = json.loads(res1)
        try:
            realInstantRate = float(res2['data']['instantRate'])
            return realInstantRate
        except:
            print(res2)
            return "0"


if __name__=='__main__':

    rate_test = rate_test()
    currentlist=[]
    start = 1
    rate_test.swft_session()#必须保留
    coin_list = rate_test.queryCoinList()
    for i in range(len(coin_list)):
        upper_dep = coin_list['data'][i]['coinCode']
        for k in range(len(coin_list)):
            # print('存币:',upper_dep)
            upper_rec = coin_list['data'][k]['coinCode']
            if upper_dep == upper_rec:
                continue
            else:
                base_info = rate_test.getBaseInfo(upper_dep,upper_rec)
                exchange_am = rate_test.exchangeAm(base_info['depositMax'], base_info['depositMin'])
                rate_test.exchangeRate(base_info, exchange_am)
                realInstantRate = rate_test.realBaseinfo(upper_dep, upper_rec)
                print(upper_dep, upper_rec, '存币数量:', exchange_am, '误差:', float((rate-realInstantRate)/realInstantRate))
                # print(currentlist)
                # currentlist=[]
                start = start+1
