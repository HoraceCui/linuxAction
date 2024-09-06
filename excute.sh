#!/bin/bash

# 定义变量，指定脚本路径
SCRIPT_PATH="./zipFile/linux1.sh"

# 检查变量指定的路径是否存在
if [ -f "$SCRIPT_PATH" ]; then
  # 如果存在，执行脚本
  bash "$SCRIPT_PATH"
else
  # 如果不存在，输出提示信息
  echo "$SCRIPT_PATH 文件不存在"
fi