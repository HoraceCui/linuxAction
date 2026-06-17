要编写一个 GitHub Actions 工作流（workflow），用于手动触发，从 Docker Hub 拉取镜像，修改镜像的 tag 并将其推送到阿里云的 Docker 仓库，可以按照以下步骤实现。我们会通过 `workflow_dispatch` 手动触发该 Action，并通过输入参数接收 Docker 镜像名称和新的 tag。

### 1. **准备工作**
首先，你需要确保：
- 阿里云的 Docker 仓库已经创建好，并获取到了阿里云 Docker Registry 的地址，例如：`registry.cn-hangzhou.aliyuncs.com/your-repo-name`.
- 在 GitHub 仓库的设置中添加以下机密（Secrets）：
  - `DOCKERHUB_USERNAME`：Docker Hub 的用户名。
  - `DOCKERHUB_PASSWORD`：Docker Hub 的密码或访问令牌。
  - `ALIYUN_USERNAME`：阿里云的 Docker 仓库用户名（通常是阿里云账号）。
  - `ALIYUN_PASSWORD`：阿里云的 Docker 仓库密码或访问令牌。

### 2. **GitHub Action Workflow 编写**

创建 `.github/workflows/docker-migration.yml` 文件，内容如下：

```yaml
name: Docker Image Migration

on:
  workflow_dispatch:
    inputs:
      dockerhub_image:
        description: 'Docker Hub 镜像名称 (全名，包括用户名/组织名和镜像名)'
        required: true
        type: string
      new_tag:
        description: '需要修改的镜像 tag 名'
        required: true
        type: string

jobs:
  migrate-image:
    runs-on: ubuntu-latest

    steps:
    # Step 1: 登录 Docker Hub
    - name: Login to Docker Hub
      run: |
        echo "${{ secrets.DOCKERHUB_PASSWORD }}" | docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" --password-stdin

    # Step 2: 拉取 Docker Hub 上的镜像
    - name: Pull image from Docker Hub
      run: |
        docker pull ${{ github.event.inputs.dockerhub_image }}

    # Step 3: 给镜像打上新标签
    - name: Retag Docker image
      run: |
        OLD_IMAGE=${{ github.event.inputs.dockerhub_image }}
        NEW_TAG=${{ github.event.inputs.new_tag }}
        NEW_IMAGE="registry.cn-hangzhou.aliyuncs.com/your-repo-name/$(echo ${OLD_IMAGE} | cut -d/ -f2):${NEW_TAG}"
        docker tag ${OLD_IMAGE} ${NEW_IMAGE}
        echo "New image: ${NEW_IMAGE}"

    # Step 4: 登录阿里云 Docker 仓库
    - name: Login to Aliyun Docker Registry
      run: |
        echo "${{ secrets.ALIYUN_PASSWORD }}" | docker login -u "${{ secrets.ALIYUN_USERNAME }}" registry.cn-hangzhou.aliyuncs.com --password-stdin

    # Step 5: 推送新标签的镜像到阿里云 Docker 仓库
    - name: Push image to Aliyun
      run: |
        NEW_TAG=${{ github.event.inputs.new_tag }}
        OLD_IMAGE=${{ github.event.inputs.dockerhub_image }}
        NEW_IMAGE="registry.cn-hangzhou.aliyuncs.com/your-repo-name/$(echo ${OLD_IMAGE} | cut -d/ -f2):${NEW_TAG}"
        docker push ${NEW_IMAGE}
```

### 3. **详细说明**

- **手动触发 (`workflow_dispatch`)**：
  这个工作流是手动触发的，要求输入两个参数：
  - `dockerhub_image`：Docker Hub 上的完整镜像名称（包括用户名或组织名）。
  - `new_tag`：镜像的新标签。

- **步骤解析**：
  1. **登录 Docker Hub**：使用 GitHub Secrets 中存储的 Docker Hub 凭证登录 Docker Hub。
  2. **拉取镜像**：使用 `docker pull` 拉取指定的 Docker Hub 镜像。
  3. **修改镜像标签**：将拉取的镜像打上新标签，并格式化为阿里云 Docker 仓库的地址。`$(echo ${OLD_IMAGE} | cut -d/ -f2)` 是为了提取镜像名称（去掉前面的 Docker Hub 用户名/组织名）。
  4. **登录阿里云 Docker 仓库**：使用 GitHub Secrets 中存储的阿里云 Docker 仓库凭证登录。
  5. **推送到阿里云**：使用 `docker push` 将带有新标签的镜像推送到阿里云 Docker 仓库。

### 4. **运行 GitHub Action**

在 GitHub 仓库的 **Actions** 标签页下，您可以看到创建好的 Action。点击该工作流并手动触发，填写输入的 `dockerhub_image` 和 `new_tag`，然后运行该 Action。

### 5. **检查推送结果**
您可以登录阿里云容器镜像服务（ACR）来验证镜像是否已经成功推送，并检查镜像标签是否正确。

### 总结
这个 GitHub Actions 工作流可以手动触发并从 Docker Hub 拉取镜像，修改标签后推送到阿里云的 Docker 仓库。使用了 GitHub Secrets 来安全地存储凭证，并通过参数输入实现灵活操作。
