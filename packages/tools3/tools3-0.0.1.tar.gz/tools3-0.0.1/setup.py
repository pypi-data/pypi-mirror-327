from setuptools import setup, find_packages

setup(
    name='tools3',  # 库名
    version='0.0.1',  # 版本号
    author='qq1060656096',  # 作者名
    author_email='1060656096@qq.com',  # 作者邮箱
    description='develop tools',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常从 README.md 读取
    long_description_content_type='text/markdown',  # 描述内容类型
    url='https://github.com/dev/tools',  # 项目主页
    packages=find_packages(),  # 自动查找包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Python 版本要求
)