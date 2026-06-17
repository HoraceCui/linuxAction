import dns.resolver
import ipaddress
import sys

# 依赖安装提示 / Dependency Info:
# sudo apt install python3-pip
# pip install dnspython

def get_aaaa_record(domain):
    """
    获取指定域名的 AAAA 记录 / Resolve AAAA (IPv6) record for a domain
    参数:
        domain (str): 要查询的域名
    返回:
        str: 返回完整展开形式的 IPv6 地址，如果没有记录或查询失败，返回 None
    """
    try:
        # 查询 AAAA 记录 / Query AAAA records
        answers = dns.resolver.resolve(domain, 'AAAA')
        # 返回标准化展开形式的 IPv6 地址 / Return standard exploded IPv6 address
        return ipaddress.ip_address(answers[0].to_text()).exploded
    except dns.resolver.NoAnswer:
        return None  # 没有 AAAA 记录 / No AAAA record
    except dns.resolver.NXDOMAIN:
        return None  # 域名不存在 / Domain does not exist
    except Exception as e:
        print(f"查询时出错 / Error during query: {e}")
        return None

def main():
    # 检查命令行参数 / Check command line args
    if len(sys.argv) != 2:
        print("用法: python queryDNS.py <域名>")
        sys.exit(1)

    domain = sys.argv[1]
    aaaa_records = get_aaaa_record(domain)

    if aaaa_records:
        print("AAAA 记录:", aaaa_records)
    else:
        print("未找到 AAAA 记录或查询失败")

if __name__ == "__main__":
    main()
