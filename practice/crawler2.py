# coding=utf-8 ##

import os, re, urllib.request, ssl, random, json

def getResponse(url):
    headers = {'cookie':'over18=1'}

    # 模擬各種瀏覽器帶的header
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]

    # 創建請求體(先加上cookie的header)
    req = urllib.request.Request(url,headers=headers)

    # 再讓請求體的header隨機加上一個 瀏覽器資訊(User-Agent)
    req.add_header('User-Agent', random.choice(my_headers))

    # context = ssl._create_unverified_context() https可能須要??

    # 用請求體打開URL
    response = urllib.request.urlopen(req)#,context = context)

    return response.read().decode('utf-8')


temp = 'https://shopee.tw/api/v2/fe_category/get_list'

data = getResponse(temp)
data = json.loads(data)
data = data['data']['category_list']

# print(data)

path = 'output.txt'

for product in data:
    childUrl = 'https://shopee.tw/api/v2/fe_category/get_children?catid=' + str(product['catid'])
    childData = getResponse(childUrl)
    childData = json.loads(childData)['data']['category_list']

    # print(childData)

    for child in childData:
        childProductUrl = 'https://shopee.tw/api/v4/search/search_items?by=relevancy&fe_categoryids=' + str(child['catid']) + '&limit=20&newest=0&order=desc&page_type=search&scenario=PAGE_SUB_CATEGORY&version=2'
        productData = json.loads(getResponse(childProductUrl))['items']

        for productInfo in productData:
            infomation = []
            infomation.append(str(productInfo['itemid']) + ',')  # productId: 11708405
            infomation.append('"' + productInfo['item_basic']['name'] + '"' + ',')    # productName: 【CHING'S獨家】超顯瘦彈性極佳中高腰黑褲 長褲 S-2XL 黑釦真拉鍊前後口袋 黑褲 女裝 褲子
            infomation.append('"https://cf.shopee.tw/file/' + productInfo['item_basic']['image'] + '_tn"' + ',')    # productImg: https://cf.shopee.tw/file/2a684c81589bb509d79dec9c3e5bbee1_tn
            infomation.append(str(productInfo['item_basic']['price']/100000) + ',')   # discountPrice: 29900000(須 除以100000)
            infomation.append(str(productInfo['item_basic']['price_before_discount']/100000) + ',')   # originalPrice: 0(若此商品無打折，此值為0)
            infomation.append(str(product['catid']) + ',') # (大分類)categoryId: 11040766
            infomation.append(str(child['catid']) + ',')   # (子類)childId: 11042304
            infomation.append('"' + child['display_name'] + '"' + ',')    # (子類名稱)childName: T恤
            infomation.append( '"' + (productInfo['item_basic']['shop_location'] + '"' + ',') if (productInfo['item_basic']['shop_location']) else '"none",')   # (出貨地點)shopLocation: 臺北市南港區
            infomation.append(str(productInfo['item_basic']['historical_sold']) + ',') # (目前銷量)sales: 67741
            infomation.append(str(round(productInfo['item_basic']['item_rating']['rating_star'], 2)) + ',')  # (熱門?星星)hot: 4.95
            infomation.append(str(random.randint(20, 70)) + ',')    # inventory庫存
            infomation.append('0')  # isDelete
            # print(infomation)
            with open(path, 'a', encoding="utf-8") as f:
                f.write('(')
                f.writelines(infomation)
                f.write('),')

