def switch_model(model_list, current_model_name):
    print(current_model_name + "：请输入模型名称，目前支持的模型有以下几种：", end="\n")
    print(', '.join(model_list), end="\n")
    new_model = input("请输入模型名称：")
    if new_model in model_list:
        current_model = new_model
        current_model_name = current_model
        print(f"模型已切换到 {current_model}")
        return current_model_name
    else:
        print("无效的模型名称")
