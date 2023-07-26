import os


def verify_file_type(filename) -> int:
    """
    判断文件类型
    :param filename: 文件名称
    :return: 文件类型代码
    """
    file_type = filename.split('.')
    if file_type[-1].upper() in ('EXE', 'MSI'):
        return 1
    elif file_type[-1].upper() in ('ZIP', 'RAR', 'GZ'):
        return 2
    elif file_type[-1].upper() in ('DOC', 'DOCX', 'XLS', 'XLSX', 'PPT', 'PPTX', 'TXT', 'PDF'):
        return 3
    elif file_type[-1].upper() in ('MP3', 'MID', 'WAV', 'AU', 'RAM', 'WMA', 'MMF', 'AMR', 'AAC', 'FLAC'):
        return 4
    elif file_type[-1].upper() in ('MP4', 'AVI', 'WMV', 'RM', 'MPG', 'MOV', 'SWF'):
        return 5
    elif file_type[-1].upper() in ('BMP', 'GIF', 'JPG', 'JPEG', 'PIC', 'PNG', 'TIF'):
        return 6
    else:
        return 7


if __name__ == '__main__':
    filename = "a.doc.zip"
    print(verify_file_type(filename))
