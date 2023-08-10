import requests
import os
from time import sleep

from services.download_services import download


def createDir(directory):
    """
    创建目录，如果目录已经存在，则不创建
    :param directory: 指定要合建的目录
    :return: 无
    """
    if not os.path.exists(directory):
        os.mkdir(directory)


def start_download(url:str, filename):
    """
    根据URL下载视频文件,如果指定目录下同名文件存在，则不下载。
    :param url: 文件下载链接
    :param filename: 存储的目标文件名（含路径）
    :return: None
    """
    if os.path.exists(filename):
        print(filename + "\033[32m-->已下载\033[0m")
    else:
        print(filename + "\033[31m-->开始下载\033[0m")
        try:
            download(url=url.replace("\\", ""), file_name=filename)
        except NameError as e:
            print(e)
            # sleep(range(0, 5))


def get_tuoyufuwu_video(base_path: str, url: str):
    """
    中托论坛视频下载:https://jt.tuoyufuwu.org.cn/edu/index.html#/zhongtuo/index
    根据指定的URL下载视频文件
    :type base_path: string，保存下载文件的根目录
    :type url: string， 下载视频的页面
    """
    rs = requests.get(url=url)
    record = eval(str(rs.content, encoding="utf-8"))  # 由于返回是bytes类型，要先转换成str，再转换成dict
    # print(record['data'])
    course_base_name = record['data']['base']['name']  # 课程名称
    # print(course_base_name)

    course_dir = base_path + course_base_name  # 课程目录名称
    createDir(course_dir)  # 创建课程目录

    if record['data'].__contains__('list') and len(record['data']['list']) > 0:
        for chapter in range(0, len(record['data']['list'])):
            course_chapter_name = (record['data']['list'][chapter]['name']).replace(" ", "")  # 章名称

            course_chapter_dir = course_dir + "\\" + course_chapter_name  # 章目录路径
            createDir(course_chapter_dir)  # 创建章目录
            chapters = record['data']['list'][chapter]  # 课程下面所有的章
            if chapters.__contains__('lesson') and len(chapters['lesson']) > 0:
                lessons = record['data']['list'][chapter]['lesson']  # 章下面所有的节
                for node in range(0, len(lessons)):
                    course_chapter_node_name = lessons[node]['name'].replace(" ", "")  # 节名称
                    course_chapter_node_dir = course_chapter_dir + "\\" + course_chapter_node_name  # 节目录路径
                    createDir(course_chapter_node_dir)  # 创建节目录
                    speaks = lessons[node]  # 节下面所有的小节
                    if speaks.__contains__('speak'):
                        for speak in range(0, len(speaks['speak'])):
                            course_chapter_node_speak_name = speaks['speak'][speak]['name'].replace(" ", "")  # 第几讲，小节名称
                            course_chapter_node_speak_url = speaks['speak'][speak]['video_ids'][0]['resource'][0][
                                'url'].replace(" ", "")  # 小节的下载链接（第XX讲）

                            # 开始下载
                            final_file_name = course_chapter_node_dir + "\\" + course_chapter_node_speak_name + ".mp4"
                            start_download(course_chapter_node_speak_url, final_file_name)
            else:  # 没有章、节的情况，直接下载课程
                course_chapter_node_speak_name = record['data']['list'][chapter]['video_ids'][0]['resource'][0][
                    'name'].replace(" ", "")
                course_chapter_node_speak_url = record['data']['list'][chapter]['video_ids'][0]['resource'][0][
                    'url'].replace(" ", "")

                final_file_name = course_chapter_dir + '\\' + course_chapter_node_speak_name + ".mp4"
                start_download(course_chapter_node_speak_url, final_file_name)


if __name__ == '__main__':
    # url = "https://jt.tuoyufuwu.org.cn/api/institute/course/info/get?goods_id=743"
    base_path = "E:\\course\\"
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
        get_tuoyufuwu_video(base_path, url)
