#coding: utf-8
__author__ = 'randy'
import requests
from bs4 import BeautifulSoup
from bs4 import element
import pymysql
def main():

    head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    htmlurl = 'http://www.smzdm.com/jingxuan/p'
    promotioninfo = []
    for nums in range(0,1):
        html = requests.get(htmlurl+str(nums), headers=head, timeout=60).text
        bs = BeautifulSoup(html, 'lxml')
        listpage = bs.find(id='feed-main-list')
        for item in listpage.children:
            if isinstance(item, element.Tag) and item['class'][0] == 'feed-row-wide':
                product_name = item.h5.a.contents[0]
                print(product_name)
                try:
                    product_price = item.h5.a.span.text.strip()
                    print(product_price)
                    tagnominate_info = item.div.find_all('div')[1].find(class_='feed-block-info')
                except AttributeError:
                    continue
                if tagnominate_info:
                    nomination_person = tagnominate_info.span.string
                    print(nomination_person)
                    if nomination_person == u'爆料人：商家自荐':
                        isselfnomination = '1'
                    else:
                        isselfnomination = '0'
                    tagss =[]
                    for tag in tagnominate_info.find_all('span')[1].children:
                        if isinstance(tag, element.Tag):
                            tagss.append(tag.string)
                            print(tag.string)
                    tags = ' '.join(tagss)

                zhi = int(item.find(class_='J_zhi_like_fav price-btn-up').span.span.text)
                buzhi = int(item.find(class_='J_zhi_like_fav price-btn-down').span.span.text)
                # print(zhi)
                # print(buzhi)
                promotioninfo.append((product_name, product_price, isselfnomination, tags, zhi, buzhi))
        # with open('promotioninfo.txt', 'w', encoding='utf-8') as filew:
        #     for item in promotioninfo:
        #         print('\t'.join(item))
        #         filew.write('\t'.join(item))
        #         filew.write('\n')

        store_to_database(promotioninfo)

def store_to_database(promotiondata):
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'xq1993',
        'db': 'promotioninfo',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    # Connect to the database
    connection = pymysql.connect(**config)
    # 执行sql语句
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO promotion_info (product_name, product_price, isselfnomination, tags, zhi, buzhi) VALUES (%s, %s, %s, %s, %s, %s)'

            # sql = 'SELECT * FROM promotion_info'
            product_name, product_price, isselfnomination, tags, zhi, buzhi  = promotiondata[0]
            # cursor.execute(sql, (product_name, product_price, isselfnomination, tags, int(zhi), int(buzhi)))
            cursor.executemany(sql, promotiondata)
            # 获取查询结果
            # result = cursor.fetchone()
            # print(result)
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close();

if __name__=='__main__':
    main()