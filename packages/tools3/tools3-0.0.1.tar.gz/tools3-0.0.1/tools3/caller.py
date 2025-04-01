import os
import inspect

class Caller(object):
    def get_caller_filename(with_extension=True):
        """
        获取调用者的文件名。

        :param with_extension: 是否包含扩展名，默认为 True。
        :return: 调用者的文件名。
        """
        # 获取调用栈信息
        stack = inspect.stack()
        caller_frame = stack[1]

        # 提取调用者的文件名
        caller_file_path = caller_frame.filename

        if with_extension:
            return os.path.basename(caller_file_path)
        else:
            # 去掉扩展名
            return os.path.splitext(os.path.basename(caller_file_path))[0]

    @staticmethod
    def get_caller_filepath(new_extension=None, include_filename=True, absolute=True):
        """
        获取调用者的文件路径，并支持替换扩展名。

        :param new_extension: 新的扩展名（如 ".custom"），默认为 None。
        :param include_filename: 是否包含文件名，默认为 True。
        :param absolute: 是否返回绝对路径，默认为 True。
        :return: 调用者的文件路径。
        """
        try:
            # 获取当前帧的上一级帧（即调用此函数的代码的上下文）
            caller_frame = inspect.currentframe().f_back
            caller_info = caller_frame.f_code.co_filename

            # 获取文件路径
            caller_file_path = caller_info

            # 如果需要绝对路径
            if absolute:
                caller_file_path = os.path.abspath(caller_file_path)

            # 如果不需要文件名，仅返回目录路径
            if not include_filename:
                return os.path.dirname(caller_file_path)

            # 如果需要替换扩展名
            if new_extension:
                # 分离文件目录和文件名
                directory, filename = os.path.split(caller_file_path)
                # 获取文件名，不带扩展名
                name_without_extension, _ = os.path.splitext(filename)
                # 组合新文件名
                new_filename = f"{name_without_extension}{new_extension}"
                # 重新构建文件路径
                caller_file_path = os.path.join(directory, new_filename)

            return caller_file_path
        except Exception as e:
            print(f"Error occurred while getting caller file path: {e}")
            return None


