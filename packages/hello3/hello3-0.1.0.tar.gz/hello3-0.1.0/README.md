# hello3 库

一个简单的 Python 库，打印 "Hello, World!"。

## 安装

使用 pip 安装库

```bash
pip install hello3
```

## 使用

```python
from hello3 import say_hello

say_hello("World")  # Output: Hello, World!
```

## 构建和发布到 PyPI

### 安装必要的工具: 安装 `setuptools`、`wheel` 和 `twine`，它们是用来打包和上传库的工具。
```shell
pip install setuptools twine wheel
```

### 2.构建包
> 在项目根目录下运行以下命令来生成分发包
```shell
python3.10 setup.py sdist bdist_wheel
```

### 3.上传到 PyPI
确保你已经拥有 PyPI 的发布权限。然后，使用以下命令将包上传到 PyPI:
```shell
python3.10 -m twine upload dist/*
```