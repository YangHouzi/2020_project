import requests

from bs4 import BeautifulSoup





headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'

}





def get_cities(start_url):

    response = requests.get(start_url, headers=headers)

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')  # 这里不能用lxml解析

    cities = soup.select('#c02 a')

    datas = []

    for city in cities:

        data = {

            'city': city.text,

            'url': city.get('href')

        }

        datas.append(data)

    return datas





def choose_city(datas):

    input_city = input('请输入你想爬取的城市（北京或上海）：')

    for data in datas:

        if input_city == data['city']:

            url = data['url']

            print(url)

            break

        else:

            None

    return url





def get_ershoufang(start_url, page):

    url = start_url + '/house/i3' + str(page) + '/'

    print(url)

    response = requests.get(url, headers=headers)

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.select('h4.clearfix > a > span')

    prices = soup.select('span.red')

    areas = soup.select('p.tel_shop')

    addresses = soup.select('p.add_shop span')

    for title, price, area, address in zip(titles, prices, areas, addresses):

        data = {

            'price': price.text,

            'area': area.text.strip().split('|')[1].strip().split('�')[0] + '平方米',

        }

        if ',' in title.text:

            b = ' '

            for i in title.text.split(','):

                b = i + b

            a = {

                'title': b

            }

        else:

            a = {

                'title': title.text

            }

        if ',' in address.text:

            c = ' '

            for q in address.text.split(','):

                c = q + c

            d = {

                'address': c

            }

        else:

            d = {

                'address': address.text

            }

        data.update(a)

        data.update(d)

        save_to_file(data)

        print(data)





def save_to_file(data):

    with open('data.csv', 'a', encoding='utf-8') as f:

        f.write(data['title'] + ',' + data['price'] + ',' + data['area'] + ',' + data['address'] + '\n')





def main():

    url = 'http://esf.fang.com/newsecond/esfcities.aspx'

    datas = get_cities(url)

    start_url = choose_city(datas)

    with open('data.csv', 'a') as f:

        f.write('title,price,area,address' + '\n')

    str_num = input('请输入你想爬取的页数：')

    num = int(str_num)

    for i in range(1, num + 1):

        get_ershoufang(start_url, i)





if __name__ == '__main__':

    main()
    
