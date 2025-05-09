@echo off

:: 设置环境名称和 Python 版本
set ENV_NAME=agentLearning
set PYTHON_VERSION=3.11

:: 检查 conda 是否存在
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: 未找到 conda，请先安装 Miniconda 或 Anaconda。
    pause
    exit /b
)

echo 正在创建 Conda 环境: %ENV_NAME% ...
call conda create --name %ENV_NAME% python=%PYTHON_VERSION% -y

echo 正在激活环境 ...
call conda activate %ENV_NAME%

echo 正在安装 pip ...
call conda install pip -y

echo 正在安装依赖包 ...
pip install -r requirements.txt

echo ✅ 环境 "%ENV_NAME%" 已成功创建并安装了所有依赖。
echo 要激活环境，请运行: conda activate %ENV_NAME%
pause