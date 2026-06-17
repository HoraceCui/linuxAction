import os
import csv
import requests
import sys

def str_to_bool(s):
    """
    将字符串转换为布尔值 / Convert string to boolean
    """
    return s.lower() in ['true', '1', 't', 'y', 'yes']

def update_dns_record(record_id, record_name, record_type, record_content, proxied, ttl):
    """
    使用内置的 API Token 更新特定的 DNS 记录 / Update specific DNS record using embedded credentials
    """
    zone_id = "7d4952a548a6eabe5252460470c6cbe7"
    api_token = "TLSeQERPVhJv5YuISJSEdbBnzIv2OxyzZdQ5Qygr"
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    data = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": ttl,
        "proxied": proxied
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"DNS record '{record_name}' updated successfully.")
        return response.json()
    else:
        print(f"Failed to update DNS record '{record_name}': {response.status_code}")
        return response.json()

def get_records(pre):
    """
    从 CSV 文件读取 DNS 解析配置，并将 IPv6 的前缀拼接上参数中传入的前缀，进行更新。
    Read DNS config from CSV file, prepend the provided IPv6 prefix to the host address, and update DNS.
    参数:
        pre (str): IPv6 地址的前缀 (e.g. "2409:8a1e:a9a1:2811")
    """
    # 获取当前脚本所在的目录路径 / Get current script directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # 拼接成 list.csv 的完整路径 / Join list.csv path
    file_path = os.path.join(script_dir, 'list.csv')
    
    # 读取 CSV 并逐条更新 Cloudflare DNS 记录 / Read CSV and update records one by one
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if 'Content' in row:
                # 拼接 IPv6 前缀 / Prepend the dynamic prefix to the IPv6 address
                row['Content'] = pre + ':' + row['Content']
            
            record_id = row['ID']
            record_name = row['Name']
            record_type = row['Type']
            record_content = row['Content']
            proxied = str_to_bool(row['proxied'])
            ttl = int(row['TTL'])
            
            update_dns_record(record_id, record_name, record_type, record_content, proxied, ttl)

if __name__ == '__main__':
    # 示例运行 / Entry Point
    if len(sys.argv) != 2:
        print("Usage: python update.py <ipv6_prefix>")
        print("Example fallback execution:")
        get_records("2409:8a1e:a9a1:2811")
    else:
        pre = sys.argv[1]
        get_records(pre)