import requests
import sys

def list_dns_records(api_token, zone_id):
    """
    列出 Cloudflare 指定区域的所有 DNS 记录 / List all DNS records for a given Cloudflare Zone
    参数:
        api_token (str): Cloudflare API 令牌
        zone_id (str): 区域 ID (Zone ID)
    """
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    # 发送 GET 请求获取记录 / Send GET request to retrieve records
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dns_records = response.json()
        for record in dns_records['result']:
            print(f"Type: {record['type']}, Name: {record['name']}, Content: {record['content']}, ID: {record['id']}, TTL: {record['ttl']}, proxied: {record['proxied']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
    # 如果未提供命令行参数，则使用默认的凭证（注意：请保证这些凭据的安全，避免在公共代码库泄露）
    # If command line arguments are not supplied, fallback to default credentials
    if len(sys.argv) != 3:
        zone_id = "7d4952a548a6eabe5252460470c6cbe7"
        api_token = "TLSeQERPVhJv5YuISJSEdbBnzIv2OxyzZdQ5Qygr"
        list_dns_records(api_token, zone_id)
        print("\nUsage: python list_dns_records.py <api_token> <zone_id>")
    else:
        api_token = sys.argv[1]
        zone_id = sys.argv[2]
        list_dns_records(api_token, zone_id)
