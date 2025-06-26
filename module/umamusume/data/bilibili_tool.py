import hashlib

def generate_sign(params, secret_key=""):
    # 参数排序并拼接
    sorted_params = sorted(params.items())
    param_str = '&'.join([f'{k}={v}' for k, v in sorted_params])
    # 添加 salt
    param_str += secret_key
    # 选择加密算法（MD5 / SHA256 / SHA1）
    return hashlib.md5(param_str.encode()).hexdigest()

# 测试数据
params = {
    'hero_card_id': '100101',
    'ts': '1750853417176',
    'nonce': '66e92f99-46f6-4f61-98c8-ea1b544f8656',
    'appkey': 'd053991039404237a44023da011d3e08'
}

print(generate_sign(params))