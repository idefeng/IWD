import requests
import os
from time import sleep

from services.download_services import download


def createDir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def start_download(url, filename):
    if os.path.exists(filename):
        print(filename + " 已下载")
    else:
        print(filename + " 开始下载")
        try:
            download(url=url.replace("\\", ""),
                     file_name=filename)
        except NameError as e:
            print(e)
            # sleep(range(0, 5))


def main(url):
    rs = requests.get(url=url)
    record = eval(str(rs.content, encoding="utf-8"))  # 由于返回是bytes类型，要先转换成str，再转换成dict
    # print(record['data'])
    course_base_name = record['data']['base']['name']  # 课程名称
    # print(course_base_name)
    base_path = "E:\\course\\"
    course_dir = base_path + course_base_name  # 课程目录名称
    createDir(course_dir)  # 创建课程目录

    if record['data'].__contains__('list') :
        for chapter in range(0, len(record['data']['list'])):
            course_chapter_name = (record['data']['list'][chapter]['name']).replace(" ", "")  # 章名称
            # print(course_chapter_name)
            course_chapter_dir = course_dir + "\\" + course_chapter_name  # 章目录名称
            createDir(course_chapter_dir)  # 创建章目录
            chapters = record['data']['list'][chapter]  # 课程下面所有的章
            if chapters.__contains__('lesson') and len(chapters['lesson']) > 0:
                lessons = record['data']['list'][chapter]['lesson']  # 章下面所有的节
                for node in range(0, len(lessons)):
                    course_chapter_node_name = lessons[node]['name'].replace(" ", "")  # 节名称
                    course_chapter_node_dir = course_chapter_dir + "\\" + course_chapter_node_name  # 节目录名称
                    createDir(course_chapter_node_dir)  # 创建节目录
                    speaks = record['data']['list'][chapter]['lesson'][node]  # 节下面所有的小节
                    if speaks.__contains__('speak'):
                        for speak in range(0, len(speaks['speak'])):
                            course_chapter_node_speak_name = speaks['speak'][speak]['name'].replace(" ", "")  # 第几讲，小节名称
                            course_chapter_node_speak_url = speaks['speak'][speak]['video_ids'][0]['resource'][0][
                                'url'].replace(" ", "")  # 第几讲下载链接

                            # 开始下载
                            final_file_name = base_path + course_base_name + "\\" + course_chapter_name + "\\" + course_chapter_node_name + "\\" + course_chapter_node_speak_name + ".mp4"
                            if os.path.exists(final_file_name):
                                print(course_chapter_node_speak_name + " 已下载")
                            else:
                                print(course_chapter_node_speak_name + " 开始下载")
                                try:
                                    download(url=course_chapter_node_speak_url.replace("\\", ""),
                                             file_name=base_path + course_base_name + "\\" + course_chapter_name + "\\" + course_chapter_node_name + "\\" + course_chapter_node_speak_name + ".mp4")
                                except NameError as e:
                                    print(e)
                                    # sleep(range(0, 5))
            else:  # 没有节的情况
                course_chapter_node_speak_name = record['data']['list'][chapter]['video_ids'][0]['resource'][0][
                    'name'].replace(" ", "")
                course_chapter_node_speak_url = record['data']['list'][chapter]['video_ids'][0]['resource'][0][
                    'url'].replace(" ", "")
                final_file_name = base_path + course_base_name + '\\' + course_chapter_node_speak_name + ".mp4"
                start_download(course_chapter_node_speak_url, final_file_name)


if __name__ == '__main__':
    # url = "https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=743"
    urls = [
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=587',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=743',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=742',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=741',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=740',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=715',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=714',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=713',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=712',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=711',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=710',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=707',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=706',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=705',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=704',
        'https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=703',

    ]
    for url in urls:
        main(url)
