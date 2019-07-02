import requests
import queue
import time

dataQueue = queue.Queue()


def qa002_login():
    header = {'accept': 'application/json',
 'accept-encoding': 'gzip, deflate',
 'accept-charset': 'UTF-8,*;q=0.5',
 'cache-control': 'no-cache',
 'client-type': '3',
 'cookie': 'gr_user_id=2af98dbd-db03-4ac5-8b6c-1f9a84b9463b; _ga=GA1.2.2074536304.1558689151',
 'content-type': 'application/json',
 'content-length': '82',
 'user-agent': 'okhttp/3.11.0',
 }
    data = {
        "loginName": "system",
 "password": "123456",
 "verifyCode": "z",
 "loginType": 1,
 "clientType": 1,
 "verifyId": "1f73bf75-242f-4137-b641-abf6269ae6ef"
 }
    url = 'https://retailadmin-qa002.blissmall.net/apis/auth/sysUser/login'
 res = requests.post(url=url, json=data, headers=header)

    header['token'] = res.json()['data']['token']
    return header


header = qa002_login()


class RunMain:
    def url(self, api):
        host = 'https://retailadmin-qa002.blissmall.net'
 url = host + api
        return url

    def addCompanyProductRel(self, pageNum):  # 一级公司分发商品到二级公司
 api = '/apis/prd/backend/companyProduct/findPageCompanyProduct'
 url = self.url(api)
        data = {'companyId': "589476501972025344", 'pageNum': "1", 'pageSize': "10"}
        data['pageNum'] = pageNum
        res = self.run_main('post', url, data, header)
        print(res.text)
        for i in range(len(res.json()['data']['list'])):
            topProductId = res.json()['data']['list'][i]['topProductId']
            api = '/apis/prd/backend/companyProduct/addCompanyProductRel'
 url = self.url(api)
            data = {'productId': "585791021933793280",
 'addCompanyRelList': [{'companyId': "589476621404831744", 'checked': 1}]}
            data['productId'] = topProductId
            re = self.run_main('post', url, data, header)
            print(re.json(), 1)

    def addCompanyProductShopRel(self, pageNum):  # 从二级公司分发商品到车公庙店
 api = '/apis/prd/backend/companyProduct/findPageCompanyProduct'
 data = {"pageSize": 10, "pageNum": 1, "companyId": "589476621404831744"}
        data["pageNum"] = pageNum
        url = self.url(api)
        res = self.run_main('post', url, data, header)
        print('现在是第', pageNum, '页')
        for i in range(len(res.json()['data']['list'])):
            topProductId = res.json()['data']['list'][i]['id']
            api = '/apis/prd/backend/companyProduct/getProductDetail?productId=%s' % topProductId
            url = self.url(api)
            re = self.run_main('get', url, data, header)
            print(re.json(), 1)
            api = '/apis/prd/backend/companyProduct/companyUpdate'
 url = self.url(api)
            data = {
                "companyId": "589059415797862400",
 "id": "585826385700458496",
 "spuId": "585517711480197120",
 "deliveryTypes": "1,2",
 "detailDesc": "商品描述",
 "sharedDesc": "分享描述",
 "content": "<p>详情页面</p>",
 "contentForPc": "",
 "status": 1,
 "labelEnabled": 0,
 "supplierId": "580056206731300864",
 "spuPropertyList": [{
                    "propertyId": 2,
 "propertyValue": 1
 }, {
                    "propertyId": 3,
 "propertyValue": 1
 }],
 "detailDefined": 1,
 "productItemList": [{
                    "imageUrl": "",
 "erpCode": "1592",
 "barCode": "1_1010085_0159203671",
 "remark": "配件备注",
 "recommendedPrice": 19800,
 "price": 19900,
 "skuId": "585517711538917376",
 "skuPropertyList": [{
                        "propertyId": "585160442058108928",
 "propertyValueId": "585160442058108929"
 }]
                }],
 "productTax": {
                    "taxCategoryId": "21",
 "showLeaf": 0,
 "outputRate": 9
 }
            }
            data["spuId"] = re.json()['data']["spuId"]
            data["id"] = topProductId
            data["productItemList"] = re.json()['data']["productItemList"]
            if "spuPropertyList" in re.json()['data'].keys():
                data["spuPropertyList"] = re.json()['data']["spuPropertyList"]
            self.run_main('post', url, data, header)
            data = {"productId": "585826385700458496",
 "addShopRelList": [{"shopId": "590127304537767936", "checked": 1}]}
            data['productId'] = topProductId
            api = '/apis/prd/backend/shop/product/addCompanyProductShopRel'
 url = self.url(api)
            rs = self.run_main('post', url, data, header)
            print(rs.json())

    def updateStation(self, pageNum):
        api = '/apis/prd/backend/storeProduct/findPageShopProduct'
 data = {"shopId": "589061232149598208", "pageNum": "1", "pageSize": "10", 'status': 0, }
        data["pageNum"] = pageNum
        url = self.url(api)
        res = self.run_main('post', url, data, header)
        print(pageNum, res.json())
        for i in range(len(res.json()['data']['list'])):
            id = res.json()['data']['list'][i]['id']
            url = 'https://retailadmin-qa002.blissmall.net/apis/prd/backend/shop/product/updateStation'
 data = {"companyId": "589059415797862400", "id": "586212000128458752", "spuId": "585791007455055872",
 "shopId": "589061232149598208", "status": 1, "saleType": 0, "deliveryTypes": "1,2", "bookedType": 1}
            data['id'] = id
            rq = self.run_main('post', url, data, header)
            print(rq.json())

    def updateSmall(self, pageNum):  # 微店店铺商品上架
 api = '/apis/prd/backend/storeProduct/findPageShopProduct'
 data = {"shopId": "589060076207804416", "pageNum": "1", "pageSize": "10", 'status': 0, }
        data["pageNum"] = pageNum
        url = self.url(api)
        res = self.run_main('post', url, data, header)

        for i in range(len(res.json()['data']['list'])):
            id = res.json()['data']['list'][i]['id']
            url = 'https://retailadmin-qa002.blissmall.net/apis/prd/backend/shop/product/updateSmall'
 data = {
                "companyId": "589059415797862400",
 "id": "587596277487448064",
 "spuId": "587311840895905792",
 "shopId": "589060076207804416",
 "status": 1,
 "saleType": 1,
 "deliveryRegionType": 0,
 "deliveryRegion": "",
 "startSaleTime": "07:56",
 "prepareTime": 1,
 "channelList": [{
                    "channelId": 1,
 "enabled": 1
 }, {
                    "channelId": 2,
 "enabled": 0
 }, {
                    "channelId": 3,
 "enabled": 0
 }],
 "deliveryTypes": "2,1",
 "bookedType": 2,
 "statusSettings": [{
                    "spentTime": "1",
 "statusName": "生产计划"
 }],
 "produceStatusEnabled": 1
 }
            data['id'] = id
            re = self.run_main('post', url, data, header)
            print(re.json())

    def updateRetail(self, pageNum):  # 车公庙店铺商品上架
 api = '/apis/prd/backend/storeProduct/findPageShopProduct'
 data = {"shopId": "590127304537767936", "pageNum": "1", "pageSize": "10", 'status': 1, }
        data["pageNum"] = pageNum
        url = self.url(api)
        res = self.run_main('post', url, data, header)
        print(res.json())

        for i in range(len(res.json()['data']['list'])):
            id = res.json()['data']['list'][i]['id']
            url = 'https://retailadmin-qa002.blissmall.net/apis/prd/backend/shop/product/updateRetail'
 data = {
                "companyId": "589476621404831744",
 "id": "590145795198214144",
 "spuId": "590145599148056576",
 "shopId": "590127304537767936",
 "status": 1,
 "saleType": 1,
 "deliveryRegionType": 0,
 "deliveryRegion": "",
 "startSaleTime": "07:56",
 "prepareTime": 1,
 "channelList": [{
                    "channelId": 1,
 "enabled": 1
 }, {
                    "channelId": 2,
 "enabled": 0
 }, {
                    "channelId": 3,
 "enabled": 0
 }],
 "deliveryTypes": "2,1",
 "bookedType": 2,
 "statusSettings": [{
                    "spentTime": "1",
 "statusName": "揉面"
 }],
 "produceStatusEnabled": 1
 }
            data['id'] = id
            re = self.run_main('post', url, data, header)
            print(re.json())

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
            print("请传入请求方法 post or get")
        return result


if __name__ == '__main__':
    run = RunMain()
    for i in range(1,10):
    # run.addCompanyProductRel(i)
 # run.addCompanyProductShopRel(i)
 run.updateRetail(i)