#!/bin/bash
# chmod +x setup.sh
# ./setup.sh
# 设置环境名称和Python版本
ENV_NAME="agentLearning"
PYTHON_VERSION="3.11"

# 检查 conda 是否已安装
if ! command -v conda &> /dev/null
then
    echo "Error: Conda 未找到，请先安装 Miniconda 或 Anaconda。"
    exit
fi

# 创建 Conda 环境（如果不存在）
echo "正在创建 Conda 环境: $ENV_NAME ..."
conda create --name $ENV_NAME python=$PYTHON_VERSION -y

# 激活 Conda 环境
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME

# 安装 pip（Conda 新版默认带pip）
conda install pip -y

# 安装依赖包
echo "正在使用 pip 安装 requirements.txt 中的依赖..."
pip install -r requirements.txt

# 提示完成
echo "✅ 环境 '$ENV_NAME' 已成功创建并安装了所有依赖。"
echo "要激活环境，请运行: conda activate $ENV_NAME"