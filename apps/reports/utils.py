
def get_file_content(filename, chunk_size=1024):
    """
    文件读取生成器
    :param filename:
    :param chunk_size:
    :return:
    """
    with open(filename) as f:
        while True:
            content = f.read(chunk_size)
            if not content:
                break
            yield content
