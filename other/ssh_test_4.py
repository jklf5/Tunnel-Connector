from sshtunnel import SSHTunnelForwarder

# 可用
# https://blog.csdn.net/liuhao192/article/details/122810316
# 使用 SSHTunnelForwarder 建立 SSH 隧道，仅实现 SSH -L 命令。

# 代理服务器信息
PROXY_HOST = 'smile403.vicp.fun'
PROXY_PORT = 22
PROXY_USERNAME = 'smile2021'
PROXY_PASSWORD = '2021smile'

# 目标服务器信息
TARGET_HOST = '10.3.125.114'
TARGET_PORT = 22
TARGET_USERNAME = 'mazc'
# TARGET_PASSWORD = 'cy@1236'

CLIENT_PORT = 8114

def operate_sshtunnel():
    try:
        tunnel = SSHTunnelForwarder(
            (PROXY_HOST, PROXY_PORT),
            ssh_username=PROXY_USERNAME,
            ssh_password=PROXY_PASSWORD,
            remote_bind_address=(TARGET_HOST, TARGET_PORT),
            local_bind_address=('localhost', CLIENT_PORT)
        )
        return tunnel
    except Exception as e:
        print(e.args[0])
        return

def main():
    tunnel = operate_sshtunnel()
    if tunnel is not None:
        try:
            tunnel.start()
            tunnel.tunnel_is_up
        except Exception as e:
            print(e.args[0])
            exit()

    tunnel.stop()


if __name__ == '__main__':
    main()