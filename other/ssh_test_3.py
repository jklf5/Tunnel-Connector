import paramiko
import socks
from paramiko import AuthenticationException

# https://stackoverflow.com/questions/18968069/paramiko-port-forwarding-around-a-nat-router/19039769#19039769
# 用 paramiko 模块实现 SSH -L ，然后再 SSH 连接。
# 比如： ssh -L 8096:10.3.125.96:22 smile2021@smile403.vicp.fun    ssh -p 8096 goujp@localhost

# 代理服务器信息
PROXY_HOST = 'smile403.vicp.fun'
PROXY_PORT = 22
PROXY_USERNAME = 'smile2021'
PROXY_PASSWORD = '2021smile'

# 目标服务器信息
TARGET_HOST = '10.3.125.96'
TARGET_PORT = 22
TARGET_USERNAME = 'goujp'  # 局域网服务器用户名
TARGET_PASSWORD = 'goujp@123'  # 局域网服务器用户密码

def main():
    command = "whoami"
    proxy_client = paramiko.SSHClient()
    proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    proxy_client.connect(
        PROXY_HOST,
        port=PROXY_PORT,
        username=PROXY_USERNAME,
        password=PROXY_PASSWORD
    )

    transport = proxy_client.get_transport()
    dest_addr = (TARGET_HOST, TARGET_PORT)
    local_addr = ('localhost', 8096)
    channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

    remote_client = paramiko.SSHClient()
    remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_client.connect(
        'localhost',
        port=8096,
        username=TARGET_USERNAME,
        password=TARGET_PASSWORD,
        sock=channel
    )

    stdin, stdout, stderr = remote_client.exec_command(command)
    out = stdout.readlines()
    err = stderr.readlines()

    print(out)
    print(err)

    # 关闭连接
    proxy_client.close()
    remote_client.close()

if __name__ == '__main__':
    main()