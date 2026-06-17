import requests
import sys

def str_to_bool(s):
    """
    将字符串转换为布尔值 / Convert string to boolean
    """
    return s.lower() in ['true', '1', 't', 'y', 'yes']

def update_dns_record(api_token, zone_id, record_id, record_name, record_type, record_content, proxied=True, ttl=1):
    """
    更新 Cloudflare DNS 解析记录 / Update a Cloudflare DNS record
    参数:
        api_token (str): Cloudflare API 令牌
        zone_id (str): 区域 ID (Zone ID)
        record_id (str): 解析记录 ID (DNS Record ID)
        record_name (str): 域名/记录名 (e.g. sub.example.com)
        record_type (str): 记录类型 (A, AAAA, CNAME, etc.)
        record_content (str): 解析的目标内容 (IP 地址或域名)
        proxied (bool): 是否通过 Cloudflare CDN 代理
        ttl (int): 生效时间 (Time to Live)，1 代表自动 (Auto)
    """
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

    # 发送 PUT 请求更新 DNS 记录 / Send PUT request to update DNS record
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print("DNS record updated successfully.")
        return response.json()
    else:
        print(f"Failed to update DNS record: {response.status_code}")
        return response.json()

# 模块直接调用时的示例用法 / Example usage when calling from CLI
if __name__ == "__main__":
    if len(sys.argv) != 8:
        print(len(sys.argv))
        print("Usage: python cloudflare_dns.py <api_token> <zone_id> <record_id> <record_name> <record_type> <record_content> <proxied:True|False>")
    else:
        # Replace with your actual data
        api_token = sys.argv[1]
        zone_id = sys.argv[2]
        record_id = sys.argv[3]
        record_name = sys.argv[4]
        record_type = sys.argv[5]
        record_content = sys.argv[6]
        proxied = str_to_bool(sys.argv[7])
        result = update_dns_record(api_token, zone_id, record_id, record_name, record_type, record_content, proxied)

        print(result)
