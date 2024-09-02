#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate robochain

# 显示当前环境变量中包含 'proxy' 的内容
env | grep -i proxy

# 取消所有代理设置
unset all_proxy
unset ALL_PROXY

# 运行 Python 脚本
# python ./gpt_client/gpt_client/examples/client_tcp_retrieval_local.py
python /home/gcj/robochain-main/gpt_client/gpt_client/examples/client_tcp_retrieval_local.py