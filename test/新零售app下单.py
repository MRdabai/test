�˽ű�����Ϊ����µ������֧������
import requests
import random
import pymysql

header = {'client-id': 'b34749d6aa46a3f1', 'channel-id': '1102', 'version': '2.0.0',
 'sign': '190618155913287 Iclvn + La9mJIFhLU3Zl2inxpyllSLkCnAwVZCrecpkc =',
 'content-type': 'application/json', 'charset': 'UTF-8', 'content -length': '83',
 'accept-encoding': 'gzip', 'user-agent': 'okhttp / 3.11.0'
 }
# ���������ݿ������
db = pymysql.connect(host='39.108.4.250', user="app_retail_rw", passwd="l6i6pzLMSqbm7WRLoSRo", port=29383,
 db="retail_product")
# ��ȡ�����α�
cursor = db.cursor()
# ִ��sql
cursor.execute(
    "select product_item_no,price from product_item where company_id=589476621404831744 and product_id in(select product_id from shop_product where shop_id=590127304537767936)")
datas = cursor.fetchall()  # �����ݿ���ȡ���ܲ��Թ�˾������

db.commit()
cursor.close()
db.close()


class RunMain:
    def __init__(self):
        pass

 def url(self, api):
        host = 'https://rtapi-qa002.blissmall.net'
 url = host + api
        return url

    def loginBySms(self, phone):  # ��������֤���¼
 api = '/apis/authc/anon/sms/V1.0.0/sendSmsCode'
 url = self.url(api)
        data = {
            "clientId": "b34749d6aa46a3f1",
 "mobile": "11111111111",
 "typeCode": "retailUserLogin"
 }
        data["mobile"] = phone
        res = self.run_main('post', url, data, header)

        print('���Ͷ���', res.json())
        url = 'https://rtapi-qa002.blissmall.net/apis/auth/userApp/V1.0.0/loginBySms'
 data = {
            "loginType": 1,
 "mobile": "11111111111",
 "smsCode": "123456"
 }
        data["mobile"] = phone
        re = self.run_main('post', url, data, header)
        print('��¼', re.json())
        header['token'] = re.json()['data']["authMemberInfo"]['token']
        self.userId = re.json()['data']["authMemberInfo"]['userId']

        return header

    def add(self, phone):  # �����ջ���ַ
 header = self.loginBySms(phone)
        url = 'https://rtapi-qa002.blissmall.net/apis/members/userApp/receiverAddress/V1.0.0/add'
 data = {"addressDetail": "�ִ���������(����)���޹�˾", "cityName": "������", "gender": 1, "house": "��", "latitude": 22.58419,
 "longitude": 113.94671, "provinceName": "�㶫ʡ", "receiverMobile": "11111111111", "receiverName": "�ƶ�",
 "regionName": "��ɽ��"}

        re = self.run_main('post', url, data, header)
        print(re.json())

    def findAdressList(self, phone):
        header = self.loginBySms(phone)
        url = 'https://rtapi-qa002.blissmall.net/apis/members/userApp/receiverAddress/V1.0.0/list'
 data = {}
        re = self.run_main('get', url, data, header)
        adressId = []
        for i in range(len(re.json()['data'])):
            adressId.append(re.json()['data'][i]['id'])
        return adressId

    def submit(self, phone):  # �ύ�������������֧��
 url = 'https://rtapi-qa002.blissmall.net/apis/trade/userApp/order/V2.0.0/submit'
 data = {
            "postAmount": 0,
 "remark": "",
 "buyerAddressId": 572000925652893696,
 "buyerId": 566585536936779776,
 "buyerPhone": "11111111111",
 "deliveryTime": "2019-06-18 20:30",
 "deliveryType": 2,
 "orderItemList": [{
                "productItemNo": "1_P03789_K05288",
 "quantity": 1,
 "unitPrice": 11000
 }],
 "orderReachedGiveParamList": [],
 "promotionList": [],
 "shopId": 590127304537767936
 }

        buyerAddressId = self.findAdressList(phone)
        data["buyerId"] = self.userId
        for i in range(85):
            data["orderItemList"][0]["productItemNo"] = datas[i][0]
            data["orderItemList"][0]["unitPrice"] = datas[i][1]
            data['buyerAddressId'] = random.choice(buyerAddressId)

            res = self.run_main("post", url, data, header)
            try:
                print('�ύ����', res.json()['data']['orderId'])
                url1 = 'https://rtapi-qa002.blissmall.net/apis/trade/userApp/order/V1.0.0/getPayInfo'
 data1 = {
                    "orderId": "590614580648656896",
 "payType": 1
 }

                data1['orderId'] = res.json()['data']['orderId']
                print(data1)
                re = self.run_main("post", url1, data1, header)
                print('���֧���ɹ�', re.json())
            except:
                print('�ύʧ��', res.json()['message'])

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
            print("����")
        return result


if __name__ == '__main__':
    run = RunMain()
    run.submit(11111111111)#�˴������ֻ�����