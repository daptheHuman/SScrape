import requests
import json
import bs4 as bs
import pandas as pd

your_head={
'GET':"wss: '// chat - ws.shopee.co.id / socket.io /?EIO = 3 & transport = websocket HTTP / 1.1",
'connection': 'Upgrade',
'pragma': 'no - cache',
'cache - Control': 'no - cache',
'user - Agent': 'Mozilla / 5.0(Linux;Android 6.0;Nexus 5 Build / MRA58N) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 90.0.4430.85 Mobile Safari / 537.36',
'upgrade': 'websocket',
'origin': 'https: // shopee.co.id',
'sec - WebSocket - Version': '13',
'accept - Encoding': 'gzip, deflate, br',
'accept - Language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
'sec-WebSocket-Key': 'fGdhEcMGmjsA84qcQVzaDQ==',
'sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
'sec-fetch-dest': 'empty'
}

shopee_id = input("Enter the shop id ")

def shop_product(shopee_id):
    order= input("Please choose (priceasc,pricedsc,relevancy,sales,newer) ")
#    order = 'sales'
    if order == 'priceasc':
        url = 'https://shopee.co.id/api/v4/search/search_items?' \
              'by=price&limit=20&match_id={}&newest=0&order=asc&page_type=shop&version=2'.format(shopee_id)
    if order == 'pricedsc':
        url = '{https://shopee.co.id/api/v4/search/search_items?' \
              'by=price&limit=20&match_id={}&newest=0&order=desc&page_type=shop&version=2}'.format(shopee_id)
    if order == 'relevancy':
        url = 'https://shopee.co.id/api/v4/search/search_items?' \
              'by=relevancy&limit=20&match_id={}&newest=0&order=desc&page_type=shop&version=2'.format(shopee_id)
    if order == 'newer':
        url = 'https://shopee.co.id/api/v4/search/search_items?' \
              'by=ctime&limit=20&match_id={}&newest=0&order=desc&page_type=shop&version=2'.format(shopee_id)
    if order == 'sales':
        url = 'https://shopee.co.id/api/v4/search/search_items?' \
              'by=sales&limit=20&match_id={}&newest=0&order=desc&page_type=shop&version=2'.format(shopee_id)
    return url

shopee_url= shop_product(shopee_id)
data= requests.get(shopee_url).text
page= json.loads(data)
prod_data = {}

namedata = []
imgdata = []
storedata = []
pricedata = []

for item in page['items']:
    name=item['item_basic']['name']#nama produk
    namedata.append(name)

    id=item['item_basic']['shopid'] #ambil id toko
    store=['https://shopee.co.id/shop/{}'.format(id)] #link toko
    storedata.append(store)

    images = ['https://cf.shopee.co.id/file/{}'.format(img) for img in item['item_basic']['images']] #ambil gambar
    imgdata.append(images)

    price = [item['item_basic']['price']//100000]
    pricedata.append(price)

prod_data['prod_name']= namedata
prod_data['prod_img']= imgdata
prod_data['prod_store']= storedata
prod_data['prod_price']= pricedata

print(prod_data)
print(type(prod_data))

df = pd.DataFrame(prod_data)
df.to_excel("outputshopee.xlsx")

