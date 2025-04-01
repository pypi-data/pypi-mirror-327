
from setuptools import setup, find_packages

setup(
    name='hello3',  # 包名
    version='0.1.0',  # 版本号
    author='zwei',  # 作者
    author_email='1060656096@qq.com',  # 作者邮箱
    description='A simple hello world library',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常从 README.md 读取
    long_description_content_type='text/markdown',  # 长描述的内容类型
    url='https://github.com/qq1060656096/dev/py/hello',  # 项目主页
    packages=find_packages(),  # 自动查找包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python 版本要求
)