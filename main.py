"""
Author:Curtis
BeginTime:2019年11月5日 10:56:09

抓取B站画友摄影版块图片的工具，简单地抓取Cosplay分区和私服分区下最热和最新两类图片
项目参考：https://github.com/nishikinoyan/BiliBili--drawarea

使用requests，还用了进程池？（这个还不是很熟悉，虽然用了，但不知道对不对）
可以自己安排保存图片的路径
下载的图片为数字编号，放在以pagenum为名的文件下，基本上一页有个100多张图片

虽然爬取到图片，但是分类还是看着不太舒服，后期等本领强了再进行修改，或者有感兴趣的大佬们可以down回去自己玩
非常感谢哥们 nishikinoyan 的帮助，这个小项目也是参考他的

觉得还不错的可以给个star噢！

EndTime:2019年11月6日 17:38:32
"""
import requests
import json
import time
import os
from multiprocessing import Pool


def download(pictures_list):
    """
    下载获取的图片url
    """
    picname = str(p)
    new = new_picture_dir + '/' + picname
    os.mkdir(new)
    for i, pic_url in enumerate(pictures_list):
        try:
            pic = requests.get(pic_url, timeout=15)
            string = str(i + 1) + '.jpg'
            with open(os.path.join(new +'/'+ string), 'wb')as o:
                o.write(pic.content)
            print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue


def select(json_info):
    """
    筛选所需的页面信息,获取所有图片的url
    """
    dict = json.loads(json_info)
    all_url = []
    # print(json.dumps(dict, indent=4, ensure_ascii=False))
    for picture_list_temp in dict['data']['items']:
    #  print(picture_list_temp)
        for pictures_temp in picture_list_temp['item']['pictures']:
            # time.sleep(0.1)
            # print(pictures_temp)
            for url in pictures_temp:
                time.sleep(0.01)
                b = pictures_temp.get('img_src')
            all_url.append(b)
    return all_url


def print_fozu():
    print("                            _ooOoo_                             ")
    print("                           o8888888o                            ")
    print("                           88  .  88                            ")
    print("                           (| -_- |)                            ")
    print("                            O\\ = /O                            ")
    print("                        ____/`---'\\____                        ")
    print("                      .   ' \\| |// `.                          ")
    print("                       / \\||| : |||// \\                       ")
    print("                     / _||||| -:- |||||- \\                     ")
    print("                       | | \\\\\\ - /// | |                     ")
    print("                     | \\_| ''\\---/'' | |                      ")
    print("                      \\ .-\\__ `-` ___/-. /                    ")
    print("                   ___`. .' /--.--\\ `. . __                    ")
    print("                ."" '< `.___\\_<|>_/___.' >'"".                 ")
    print("               | | : `- \\`.;`\\ _ /`;.`/ - ` : | |             ")
    print("                 \\ \\ `-. \\_ __\\ /__ _/ .-` / /              ")
    print("         ======`-.____`-.___\\_____/___.-`____.-'======         ")
    print("                            `=---='                             ")
    print("                                                                ")
    print("         .............................................          ")
    print("                 佛祖镇楼             BUG辟邪                    \n\n")

bl_session = requests.session()
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br'
    }

if __name__ == '__main__':
    print_fozu()

    print('-------------欢迎使用B站画友摄影版块图片下载工具-------------\n')
    print('------本工具仅供自己学习使用，抓取内容切勿商用，请尊重版权------')
    print('*************************工具正在运行************************\n')

    print('请输入存储路径')
    imgpath = input()
    if not os.path.exists(imgpath):
        os.mkdir(imgpath)

    print('选择Cosplay区还是私服区？   A.Cos区   |    B.私服区       【输入字母编号即可，注意大小写】')

    cate_type = input()
    cate_type_url = ''
    if(cate_type == 'A'):
        cate_type_url = 'cos'
        picture_dir = imgpath + '/COS'
        if not os.path.exists(picture_dir):
            os.mkdir(picture_dir)
    else:
        cate_type_url = 'sifu'
        picture_dir = imgpath + '/SIFU'
        if not os.path.exists(picture_dir):
            os.mkdir(picture_dir)

    print('选择最新还是最热门？  1：最热  |  2：最新      【输入数字编号即可】')
    pool = Pool()
    catch_type = input()
    max_page = 0
    catch_type_url = ''
    if (catch_type == '1'):
        max_page = 24
        catch_type_url = 'hot'
        new_picture_dir = picture_dir + '/HOT'
        if not os.path.exists(new_picture_dir):
            os.mkdir(new_picture_dir)

    else:
        max_page = 1000
        catch_type_url = 'new'
        new_picture_dir = picture_dir + '/NEW'
        if not os.path.exists(new_picture_dir):
            os.mkdir(new_picture_dir)
    p = 0
    while p <= max_page:
        print('###############第' + str(p) + '页###############')
        start_url = 'https://api.vc.bilibili.com/link_draw/v2/Photo/list?category='+ cate_type_url + '&type=' + catch_type_url + '&page_num=' + str(
            p) + '&page_size=20'
        print(start_url)
        print('抓取中............')

        bilibili_photo_json_page = bl_session.get(start_url, headers=headers).content
        picture_items = select(bilibili_photo_json_page)
        download(picture_items)
        p = p + 1
    groups = ([x * 20 for x in range(p, max_page + 1)])
    pool.map(download, groups)
    pool.close()
    pool.join()
