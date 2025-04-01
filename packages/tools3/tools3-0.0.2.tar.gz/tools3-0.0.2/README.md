```shell
pip install unittest
pip install python-json-logger

```

### 运行单元测试

```shell
python3.10 -m unittest discover tests
```

### 构建包上传包到PyPI
```shell
python3.10 setup.py sdist bdist_wheel
python3.10 -m twine upload dist/*
```

### 运行示例
```shell
python3.10 examples/demo.py
python3.10 examples/bug_11741.py
python3.10 examples/bug_11768.py
python3.10 examples/bug_11775.py
python3.10 examples/bug_11779.py
python3.10 examples/xq_14941.py
```

### 安装本地包
> 在开发过程中，你可以通过 pip install -e . 将包以“可编辑模式”安装到本地环境
```shell
pip install -e .
```
