import paramiko, getpass  # getpass是隐藏密码
import os
import subprocess

# 可用

def ssh_connect():
    host_ip = 'localhost'
    user_name = 'mazc'
    host_port = '8114'
    password = 'ma1239'

    # 待执行的命令
    sed_command = "sed -i 's/123/abc/g' /root/test/test.txt"
    ls_command = "ls /root/test/"


    # 注意：依次执行多条命令时，命令之间用分号隔开
    # command = sed_command + ";" + ls_command
    command = "nvidia-smi"

    try:
        # SSH远程连接
        ssh = paramiko.SSHClient()
        # invoke = ssh.invoke_shell()
        # invoke.send("ssh smile2021@smile403.vicp.fun\n")

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
        ssh.connect(host_ip, host_port, user_name, password)
    except Exception as e:
        print(e.args)
        exit()
    # 执行命令并获取执行结果
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.readlines()
    err = stderr.readlines()

    # 关闭连接
    ssh.close()

    return out, err


if __name__ == '__main__':
    # popen_way = os.popen('ssh smile2021@smile403.vicp.fun')
    # print(popen_way.read())
    # subprocess_way = subprocess.getoutput('ssh smile2021@smile403.vicp.fun')
    # print(subprocess_way)

    # pwd = getpass.getpass("请输入密码：")

    # 有了密码，开始调用函数
    result = ssh_connect()

    print(result)