from tools3 import ParamsGenerator, Caller

def generate_test_params_json(params, value_formatters, expected, include_field_names=False, separator="_"):
    # 创建 TestCaseGenerator 实例
    params_generator = ParamsGenerator(
        params=params,
        value_formatters=value_formatters,
        expected=expected,  # 传入动态生成函数
        include_field_names=include_field_names,
        separator=separator,
    )

    # 生成测试用例
    params_generator.generate_cases()
    caller = Caller()
    file_name = caller.get_caller_filepath(".json", True, True, 2)
    # 保存测试用例到 JSON 文件
    params_generator.save_to_json(file_name)
