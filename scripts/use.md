# Python Scripts Usage Guide / Python 脚本使用指南

本目录包含一组 Cloudflare DNS 操作和查询脚本。

## 环境变量配置 / Environment Setup
在运行脚本前，建议先配置以下环境变量：
```bash
# 导入配置文件，例如包含 Token 的 profile 脚本
source ~/myProfile

# 或者直接在终端导出
export CLOUDFLARE_TOKEN="your_api_token"
export ZONE_ID="your_zone_id"
```

## 脚本说明与执行 / Script Descriptions & Commands

### 1. 查询域名的 AAAA 记录 / Resolve AAAA Record
查询指定域名已解析的 IPv6 地址：
```bash
# 安装依赖
pip install dnspython

# 执行查询
python3 queryDNS.py pvev6.cuiyinhu.site
```

### 2. 列出 Cloudflare 区域内的所有解析记录 / List Cloudflare DNS Records
```bash
# 使用命令行传参
python3 list_dns_records.py $CLOUDFLARE_TOKEN $ZONE_ID

# 或者若未传参，脚本将默认回退使用脚本内置的默认凭证运行：
python3 list_dns_records.py
```

### 3. 更新特定 Cloudflare 解析记录 / Update a Specific Cloudflare DNS Record
```bash
python3 cloudflare_dns.py $CLOUDFLARE_TOKEN $ZONE_ID <record_id> <record_name> <record_type> <record_content> <proxied:True|False>
```

### 4. 批量更新动态 DDNS 解析 (从 list.csv 读取) / Bulk Update DNS Records (DDNS from CSV)
读取同目录下的 [list.csv](file:///home/cyh/github/linuxAction/scripts/list.csv)，自动将指定的 IPv6 前缀拼接到记录中并更新到 Cloudflare：
```bash
# 传递前缀参数（例如：2409:8a1e:a9a1:2811）
python3 update.py 2409:8a1e:a9a1:2811
```