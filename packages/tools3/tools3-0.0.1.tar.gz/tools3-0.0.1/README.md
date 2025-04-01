```shell
pip install unittest
pip install python-json-logger

```

### 运行单元测试

```shell
python3.11 -m unittest discover tests
```

### 构建包上传包到PyPI
```shell
python3.10 setup.py sdist bdist_wheel
python3.10 -m twine upload dist/*
```
