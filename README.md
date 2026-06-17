# LinuxAction Repository (Merged Master Repository)

本仓库是经过整理与合并后的主仓库，收纳了先前散落在各个独立仓库中的 GitHub Actions 工作流、自定义复合 Action (Composite Actions) 以及 DNS 自动更新脚本等功能，避免了功能的重复。

---

## 目录结构 / Directory Structure

```
linuxAction/
├── .github/
│   ├── workflows/
│   │   ├── docker_migration.yml       # Docker 镜像迁移工作流 (原 dockerAction)
│   │   ├── keep_alive.yml             # Linux 实例存活测试工作流 (原 test)
│   │   ├── windows_server_rdp.yml     # Windows 实例 RDP 远程配置工作流 (原 win1)
│   │   └── windows_server_codeserver.yml # Windows 实例 code-server 部署工作流 (原 win1)
│   └── actions/
│       └── hello-world/
│           ├── action.yml             # Hello World 复合 Action (原 hello-world-composite-action)
│           └── goodbye.sh             # Hello World 复合 Action 配套的退出脚本
├── docs/
│   └── docker_migration_guide.md      # Docker 镜像迁移环境配置与操作手册 (原 dockerAction 说明)
├── scripts/                           # Cloudflare DNS 管理与动态更新脚本目录 (原 python)
│   ├── cloudflare_dns.py              # 更新单条 DNS 记录的 Cloudflare API 封装
│   ├── list_dns_records.py            # 获取并显示 Zone 下的所有 DNS 解析记录
│   ├── queryDNS.py                    # 查询域名的 AAAA (IPv6) 解析记录
│   ├── update.py                      # 基于 CSV 配置动态拼接前缀批量更新 DDNS 记录
│   ├── list.csv                       # DNS 批量更新的目标记录表
│   └── use.md                         # DNS 脚本的详细使用教程
├── action.yml                         # 根目录的复合 Action：解压安全文件并执行系统配置
├── zipFile.zip                        # 包含核心配置的加密压缩包 (config.yaml, id_rsa.pub, linux.sh)
├── version                            # 全局版本控制触发文件
└── README.md                          # 本说明文档
```

---

## 功能模块详述 / Detailed Module Descriptions

### 1. 根目录复合 Action (action.yml)
* **功能描述**：用于解压加密的 `zipFile.zip`，将解压出的 `config.yaml` 配置文件和 SSH 公钥 `id_rsa.pub` 部署至系统家目录，并执行启动脚本 `linux.sh`。
* **参数输入**：
  * `zipCode`: 解压文件所需的密码。

### 2. GitHub 工作流 (.github/workflows/)
所有工作流均已支持 `workflow_dispatch`（手动触发）以及 `push` 触发（仅限修改 `version` 文件时）。

* **Docker 镜像迁移 (docker_migration.yml)**
  * **用途**：手动输入 Docker Hub 的镜像全名与目标 Tag，自动拉取、重新打标，并安全地推送到个人的阿里云容器镜像仓库。
  * **参数**：`dockerhub_image`, `new_tag`。
  * **配合文档**：参阅 [docs/docker_migration_guide.md](file:///home/cyh/github/linuxAction/docs/docker_migration_guide.md) 获取 Secrets 设置指南。

* **实例存活测试 (keep_alive.yml)**
  * **用途**：测试 GitHub Actions 容器生命周期，执行网络 ping 检测，并阻止实例在一定时间内被立即回收。

* **Windows 虚拟机控制工作流 (windows_server_rdp.yml & windows_server_codeserver.yml)**
  * **用途**：
    * `windows_server_rdp.yml`: 在 GitHub 提供的 Windows 虚拟机上安装 `cloudflared`，打通 RDP 远程桌面连接隧道。
    * `windows_server_codeserver.yml`: 在 Windows 虚拟机上安装 Nodejs 并全局部署 `code-server`，启动基于 Web 端的远程 VS Code 编辑器。

### 3. 子目录复合 Action (.github/actions/hello-world/)
* **功能描述**：标准自定义复合 Action 的示例。根据输入问候指定的人，在后台生成随机数作为输出，并使用路径检索方式运行 `goodbye.sh` 退出脚本。
* **参数输入**：
  * `who-to-greet`: 问候的名称（默认为 `World`）。

### 4. Cloudflare DNS Python 脚本工具 (scripts/)
* **功能描述**：一套高效的 Cloudflare DNS 解析维护工具，通常可部署于拥有动态 IPv6 地址的设备上作为 DDNS 更新客户端。
* **配合文档**：参阅 [scripts/use.md](file:///home/cyh/github/linuxAction/scripts/use.md) 查看具体的运行命令与 API 传参方式。

---

## 升级触发机制 / Version Trigger Mechanism
为了避免每个工作流频繁地由于日常代码提交而被重复运行，所有工作流（除手动触发外）的自动执行条件都绑定在根目录的 `version` 文件上。
若需要升级或启动某个自动化流程，只需在 [version](file:///home/cyh/github/linuxAction/version) 文件中递增版本号并提交即可。
