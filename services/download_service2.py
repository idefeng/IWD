import multiprocessing
import time
from contextlib import closing
from multiprocessing import Process, Queue

import os
import requests


# 通过多进程实现实时速度显示
def download(download_url, download_path, headers) -> {}:
    file_name = os.path.basename(download_path)
    result = dict()
    with closing(requests.get(download_url, timeout=10, verify=False, stream=True, headers=headers)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])

        with multiprocessing.Manager() as mng:  # 通过Manager向定时显示进程传递信
            mdict = mng.dict()
            mdict['download_url'] = download_url
            mdict['file_name'] = os.path.basename(download_url)
            mdict['data_bytes'] = 0  # 当前下载字节数
            mdict['exit'] = False  # 进程是否继续
            process = Process(target=cron, args=(file_name, content_size, mdict))  # 生成进程对象，执行显示函数

            process.start()
            with open(download_path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):  # 每取满chunk_size字节即存储
                    file.write(data)
                    mdict['data_bytes'] += len(data)
            # 下载完毕
            mdict['exit'] = True
            result = mdict.copy()
            process.join(3)  # 3秒超时时间，显示完全
            process.terminate()  # 超时时直接终止
    for key in result:
        print(f'{key}: {result[key]}')
    return result


def cron(file_name, content_size, mdict):  # 显示任务函数
    interval = 0.5  # 执行间隔

    content_size_formated = format_bytes_num(content_size)  # 文件总大小转换为恰当显示格式
    data_bytes_prev = mdict['data_bytes']  # 计算字节增量所需
    time_prev = time_now = time.time()  # 初始时间
    while True:  # 显示循环
        data_bytes = mdict['data_bytes']  # 当前下载字节数
        try:
            speed_num = (data_bytes - data_bytes_prev) / (time_now - time_prev)  # 计算速度
        except ZeroDivisionError:
            speed_num = 0
        data_bytes_prev = data_bytes  # 存储当前字节数作为下次计算的参照
        time_prev = time_now  # 存储当前时间作为下次计算的参照

        # 显示
        speed = format_bytes_num(speed_num)
        data_bytes_formated = format_bytes_num(data_bytes)
        persent = data_bytes / content_size * 100  # 当前下载百分比
        done_block = '|' * int(persent // 2)  # 共显示50块，故以2除百作五十，计为所下载的显示块数
        print(
            f"\r {file_name} ------>[{done_block:50}]{persent:.2f}% {speed}/s {data_bytes_formated}/{content_size_formated}",
            end=" ")

        mdict['persent'] = persent
        mdict['speed'] = speed
        mdict['data_bytes_formated'] = data_bytes_formated
        mdict['content_size_formated'] = content_size_formated

        if mdict['exit']:
            break

        time_now = time.time()
        sleep_time = time_prev + interval - time_now
        if sleep_time > 0:
            time.sleep(sleep_time)
            time_now = time.time()  # 避免误差


def format_bytes_num(bytes_num):
    i = 0
    while bytes_num > 1024 and i < 9 - 1:
        bytes_num /= 1024
        i += 1
    unit = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')[i]
    return "%.2f" % bytes_num + unit


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    download('https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe',
             'e:\\dev\\iwd\\test.exe', headers)
