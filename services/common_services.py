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
    elif file_type[-1].upper() in ('ZIP', 'RAR'):
        return 2
    elif file_type[-1].upper() in ('DOC', 'DOCX', 'XLS', 'XLSX', 'PPT', 'PPTX', 'TXT'):
        return 3
    elif file_type[-1].upper() in 'MP3':
        return 4
    elif file_type[-1].upper() in ('MP4', 'AVI', 'WMV'):
        return 5
    else:
        return 6

