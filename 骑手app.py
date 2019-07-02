import requests
header = {'accept': 'application/json',
 'accept-encoding': 'gzip, deflate',
 'accept-charset': 'UTF-8,*;q=0.5',
 'cache-control': 'no-cache',
 'client-type': '3',
 'version': '1.2.0',
 'ua': 'RiderApp/1.2.0/Android/6.0/Redmi Note 4/78:02:F8:72:2B:09/com.xfxb.rider/1920/1080/73dd6a28-9855-4c46-8237-0036292f862a/3',
 'content-type': 'application/json',
 'content-length': '82',
 'user-agent': 'okhttp/3.11.0',
 }


class RunMain:
    def __init__(self):
        pass

 def url(self, api):
        host = 'https://retailadmin-qa002.blissmall.net/'
 url = host + api
        return url

    def login(self, user):
        api = 'apis/auth/appUser/login'
 run = RunMain()
        url = run.url(api)
        data = {"clientType": "3", "loginName": "12222222222", "loginType": "1", "password": "sz123456"}
        data["loginName"] = user
        res = run.run_main("post", url, data, header)
        header['token'] = res.json()['data']['token']
        return header

    def findWaitPickList(self):
        api = 'apis/logistics/app/v2.0.0/deliveryOrder/findWaitPickList'

 url = self.url(api)
        data = {"deliveryDate": "2019-05-30", "deliveryStoreId": "589061232149598208", "pageNum": 1, "pageSize": 10}
        res = run.run_main("post", url, data, header)
        print(res.text)

    def pickOrder(self, phone):#任务池接单
 api = 'apis/logistics/app/v2.0.0/deliveryOrder/findTaskPoolList'
 url = self.url(api)
        data = {"deliveryDate": "2019-06-18", "deliveryStoreId": "589061232149598208", "pageNum": 1, "pageSize": 10}#此处修改日期配送站ID
 header = self.login(phone)
        res = self.run_main("post", url, data, header)
        orderIds = []
        print(res.json())
        for i in range(len(res.json()['data']['list'])):
            orderIds.append(res.json()['data']['list'][i]['orderId'])
        print(orderIds)
        for orderId in orderIds:
            api = '/apis/logistics/app/v2.0.0/deliveryOrder/receive?orderId=%s&client-type=3' % orderId
            run = RunMain()
            url = run.url(api)
            res = run.run_main("get", url, data, header)
            print(res.text)

    def pickup(self, phone):#扫码取货
 api = 'apis/logistics/app/v2.0.0/deliveryOrder/findWaitPickList'
 url = self.url(api)
        data = {"deliveryDate": "2019-06-18", "deliveryStoreId": "589061232149598208", "pageNum": 1, "pageSize": 10}
        header = self.login(phone)
        res = self.run_main("post", url, data, header)
        total = len(res.json()['data']['list'])
        orderIds = []
        for i in range(total):
            try:
                orderIds.append(res.json()['data']['list'][i]['orderId'])
            except:
                print('当前列表无单可以接')
        for orderId in orderIds:
            api = '/apis/logistics/app/v2.0.0/deliveryOrder/pickup?orderId=%s&client-type=3' % orderId
            run = RunMain()
            url = run.url(api)
            res = run.run_main("get", url, data, header)
            print(res.json())

    def deliverySign(self, phone):#签收，无幸福承若
 api = 'apis/logistics/app/v2.0.0/deliveryOrder/findWaitSignList'
 url = self.url(api)
        data = {"deliveryDate": "2019-06-18", "deliveryStoreId": "589061232149598208", "pageNum": 1, "pageSize": 10}
        header = self.login(phone)
        res = self.run_main("post", url, data, header)
        orderIds = []
        print(res.json())
        for i in range(len(res.json()['data']['list'])):
            orderIds.append(res.json()['data']['list'][i]['orderId'])
        print(orderIds)
        for orderId in orderIds:
            api = '/apis/logistics/app/v2.0.0/deliveryOrder/deliverySign'
 run = RunMain()
            url = run.url(api)
            data = {
                "signTime": "2019-06-17 14:19:53",
 "codPayTradeNo": "0",
 "userSignRecord": "",
 "xfxbPromiseType": "0",
 "financePayAmount": "0",
 "orderPayType": "0",
 "codPayAmount": "0",
 "orderId": "590135152319553536",
 "xfxbPromisePayType": "0",
 "xfxbPromiseAmount": "0",
 "lateMinute": "49",
 "codRealPayAmount": "0"
 }
            data["orderId"] = orderId
            res = run.run_main("post", url, data, header)
            print(res.text)

    def send_post(self, url, data, header):
        result = requests.post(url=url, json=data, headers=header)
        return result

    def send_get(self, url, data, header):
        result = requests.get(url=url, json=data, headers=header)
        return result

    def run_main(self, method, url=None, data=None, header=None):
        result = None
 if method == 'post':
            result = self.send_post(url, data, header)
        elif method == 'get':
            result = self.send_get(url, data, header)
        else:
            print("错误")
        return result



if __name__ == '__main__':
    run = RunMain()
    # run.submit()
 # run.beginPack()
 for i  in range(10):
        run.pickOrder(13333333333)
        run.pickup(13333333333)