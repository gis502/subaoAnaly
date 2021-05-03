import requests
from bs4 import BeautifulSoup

def start_requests():
    base_url = "https://weibo.cn"
    ids = march_T_id()
    urls = [
        f"{base_url}/comment/{item['t_id']}?uid={item['u_id']}rl=0&display=0&retcode=6102&page=1" for item in ids]
    for url in urls:
        parse(url)


def march_T_id():
    base_url = "https://weibo.cn"
    user_ids = ['2817059020','2656274875','3349909324']
    resulte = []
    for user_id in user_ids:
        url = base_url+'/'+user_id+'/profile'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
            'Cookie':'_T_WM=180befa99f5cfb98498a91d32761c8c2; SUB=_2A25NYFWbDeRhGeNH7FcT-S_NzDyIHXVuq3vTrDV6PUJbktAfLWTnkW1NSpPRRRBcsWh7RziViycB0hoTGiUnH0fQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh.qGeV71r9uBdJik6kEAWL5NHD95Qf1KMfeo.peKM7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSK.NSKz4eK2Ne5tt',
            'content-type': 'application/x-www-form-urlencoded',
            'referer':'https://weibo.cn/'+user_id+'/search?f=u&rl=0'
        }
        loaddata = {
            'advancedfilter':'1',
            'uid': user_id,
            'keyword':'日本本州东岸近海',
            'hasori':'0',
            'haspic':'0',
            'starttime':'20210320',
            'endtime':'20210409',
            'smblog':'筛选'
        }
        res = requests.post(base_url, headers=headers, data=loaddata)
        res.encoding = res.apparent_encoding
        # print(res)
        soup = BeautifulSoup(res.text, 'lxml')
        # with open("foo.html",'wb') as f:
        #     f.write(res.text.encode(encoding='UTF-8',errors='strict'))
        tweet_id_pre = soup.find('div',id=lambda x: x and x.startswith('M_'))
        resulte.append({
            't_id': tweet_id_pre.get('id').replace('M_',''),
            'u_id': user_id
        })
    return resulte

        # print(res.text)

def parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
        'Cookie': '_T_WM=180befa99f5cfb98498a91d32761c8c2; SUB=_2A25NYFWbDeRhGeNH7FcT-S_NzDyIHXVuq3vTrDV6PUJbktAfLWTnkW1NSpPRRRBcsWh7RziViycB0hoTGiUnH0fQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh.qGeV71r9uBdJik6kEAWL5NHD95Qf1KMfeo.peKM7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSK.NSKz4eK2Ne5tt; SSOLoginState=1617176012',
        'content-type': 'text/html; charset=utf-8'
        }
    response = requests.get(url, headers=headers)
    # print(url)
    # response.encoding = response.apparent_encoding
    # print(response.text)
    with open("foo.html",'wb') as f:
        f.write(response.text.encode(encoding='UTF-8',errors='strict'))
    soup = BeautifulSoup(response.text, 'lxml')
    if response.url.endswith('page=1') and len(soup.select('.pa div')) != 0:
        # all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
        pre_page = soup.select('.pa div')[0].get_text()
        split_location = pre_page.find('/') + 1
        all_page = pre_page[split_location:len(pre_page)-1]
        # print(soup.select('.pa div')[0].get_text())
        # print(all_page)
        if all_page:
            all_page=int(all_page)
            all_page=all_page if all_page <= 50 else 50
            for page_num in range(2, all_page + 1):
                page_url=response.url.replace(
                    'page=1', 'page={}'.format(page_num))
                res=requests.get(page_url)
                parse(page_url)
    eq_comment=[]
    comment_nodes=soup.findAll('div',id=lambda x: x and x.startswith('C_'))
    for comment_node in comment_nodes:
        comment_user_url=comment_node.a.get('href')
        if not comment_user_url:
            continue
        # comment_item = CommentItem()
        # comment_item['crawl_time'] = int(time.time())
        # if len(comment_node.select('.ctt')) > 0:
        #     continue
        # print(comment_node)
        print(comment_node.select('.ctt')[0].get_text())
        eq_comment.append({
            'comment_user_id': comment_user_url,
            'content': comment_node.select('.ctt')[0].get_text(),
            'comment_id': comment_node.find('a').get_text()
        })
    return eq_comment


start_requests()
# march_T_id()
