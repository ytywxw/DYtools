import requests, re, json, os

def __fetch(content):
    url = re.findall('[a-zA-z]+:\/\/[^\s]*', content)
    if len(url) == 0 or 'douyin.com' not in url[0]:
        res = 0
    else:
        res = url[0]
    return res

def __video(data):
    loc = data.headers.get('Location')
    if type(loc) == list:
        loc = loc[0]
    id = re.findall('(?<=video/).+(?=/\?region)', loc)[0]
    api = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + id
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    data = requests.get(api, headers = headers)
    arr = json.loads(data.text)['item_list'][0]
    images = []
    image = arr['images']
    if image == None:
        video = re.findall('href="(.*?)">Found', requests.get(arr['video']['play_addr']['url_list'][0].replace('playwm', 'play'), headers = headers, allow_redirects = False).text)[0]
    else:
        for i in range(len(image)):
            images.append(image[i]['url_list'][0])
    # vid = arr['video']['vid']
    author = arr['author']['nickname']
    avatar = arr['author']['avatar_larger']['url_list'][0]
    signature = arr['author']['signature']
    title = arr['share_info']['share_title']
    music = arr['music']['play_url']['url_list'][0]
    # mid = arr['music']['mid']
    mtitle = arr['music']['title']
    # cover = arr['video']['origin_cover']['url_list'][0]
    print('------------------------------')
    i = input('请选择操作：\n1.下载视频/图片\n2.下载背景音乐\n3.查看文案\n4.查看作者信息\n请输入序号：')
    path = os.getcwd()
    if i == '1':
        if images == []:
            if not os.path.exists(path + '/video'):
                os.mkdir(path + '/video')
            video = requests.get(video) 
            with open(path + '/video/' + title.replace('\n', ' ') + '(' + id + ').mp4', 'wb') as f:
                f.write(video.content)
            res = '下载视频成功！\n结果保存在' + path + '/video'
        else:
            if not os.path.exists(path + '/image'):
                os.mkdir(path + '/image')
            if not os.path.exists(path + '/image/' + id):
                os.mkdir(path + '/image/' + id)
            for i in range(len(images)):
                image = requests.get(images[i]) 
                with open(path + '/image/' + id + '/' + title.replace('\n', ' ') + '(' + str(i) + ').webp', 'wb') as f:
                    f.write(image.content)
            res = '下载图片成功！\n结果保存在' + path + '/image/' + id
    elif i == '2':
        if not os.path.exists(path + '/music'):
            os.mkdir(path + '/music')
        music = requests.get(music) 
        with open(path + '/music/' + mtitle + '(' + id + ').mp3', 'wb') as f:
            f.write(music.content)
        res = '下载背景音乐成功！\n结果保存在' + path + '/music/'
    elif i == '3':
        res = signature
    elif i == '4':
        res = '作者：' + author + '\n头像：' + avatar
    else:
        res = '指令错误！！！'
    return '------------------------------\n' + res + '\n------------------------------'

def __author(sec_uid):
    all = input('是否全量下载(y/n)：')
    path = os.getcwd()
    if not os.path.exists(path + '/author'):
        os.mkdir(path + '/author')
    max_cursor = 0
    total_new = 0
    total_old = 0
    has_more = True
    aweme_list = ''
    while has_more:
        url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=' + sec_uid + '&max_cursor=' + str(max_cursor) + '&count=2000'
        video_info = json.loads(requests.get(url).text)
        aweme_list = video_info['aweme_list']
        if all == 'y' or all == '':
            has_more = video_info['has_more']
        else:
            has_more = False
        if aweme_list != []:
            uid = aweme_list[0]['author']['uid']
            # short_id = aweme_list[0]['author']['short_id']
            # unique_id = aweme_list[0]['author']['unique_id']
            # nickname = aweme_list[0]['author']['nickname']
            dl_path = path + '/author/' + uid
            if not os.path.exists(dl_path):
                os.mkdir(dl_path)
            max_cursor = video_info['max_cursor']
            f = open(dl_path + '/history.txt', 'a')
            h = open(dl_path + '/history.txt')
            history = h.readlines()
            h.close()
            for aweme in aweme_list:
                aweme_id = aweme['aweme_id']
                video_url = aweme['video']['play_addr']['url_list'][0]
                vid = aweme['video']['vid']
                desc = aweme['desc']
                if aweme_id + '\n' not in history:
                    if vid == '':
                        if not os.path.exists(dl_path + '/' + aweme_id):
                            os.mkdir(dl_path + '/' + aweme_id)
                        api = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + aweme_id
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
                        }
                        data = requests.get(api, headers = headers)
                        images = json.loads(data.text)['item_list'][0]['images']
                        for i in range(len(images)):
                            print('正在下载图片(' + aweme_id + ')(' + str(i + 1) + '/' + str(len(images)) + ')...')
                            image = requests.get(images[i]['url_list'][0])
                            with open(dl_path + '/' + aweme_id + '/' + desc.replace('\n', ' ') + '(' + str(i) + ').webp', 'wb') as v:
                                v.write(image.content)
                    else:
                        print('正在下载视频(' + aweme_id + ')...')
                        video = requests.get(video_url) 
                        with open(dl_path + '/' + desc.replace('\n', ' ') + '(' + aweme_id + ').mp4', 'wb') as v:
                            v.write(video.content)
                    f.write(aweme_id + '\n')
                    print(aweme_id + '下载完成\n------------------------------')
                    total_new += 1
                else:
                    total_old += 1
            if has_more == False: 
                f.close()
                break
    return '共' + str(total_new + total_old) + '个视频，本次新增下载' + str(total_new) + '个' + '\n------------------------------'

def dl(content):
    if __fetch(content) != 0:
        url = __fetch(content)
        data = requests.get(url, allow_redirects = False)
        sec_uid = re.findall('(?<=sec_uid=)[A-Za-z0-9-_]+', data.text)
        if sec_uid == []:
            res = __video(data)
        else:
            res = __author(sec_uid[0])
    else:
        res = '链接错误'
    return res

if __name__ == '__main__':
    # print(dl('https://v.douyin.com/FAsAnHC/'))
    # print(dl('3.05 RxS:/ %抖音热门 %jk护奶裙 %双马尾的小可爱 %二次元 %双肩包  https://v.douyin.com/FD8TKGN/ 复制此链接，打开Dou音搜索，直接观看视频！'))
    # print(dl('9- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/FAtP3kr/'))
    print(dl('8- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/Ff89yJs/'))
    # print(dl('8- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/FfB1nax/'))