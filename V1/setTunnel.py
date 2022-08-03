from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from setTunnelUI import Ui_MainWin
from sshtunnel import SSHTunnelForwarder
import json
import cryptocode
import re


class setTunnel(QtWidgets.QMainWindow, Ui_MainWin):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # self.setWindowTitle("test")
        # self.resize(600, 500)
        self.setupUi(self)
        self.statusShowTime()
        self.json_file_pth = './serverList2_test.json'
        self.tunnel_start_status = []
        self.other_key = "EjdsB27ciQMK2LHf"
        self.pass_key = "F1jgDu5trCyxmUqC"

        # 设置TableWidget不可编辑
        self.tblWdgStatus.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置TableWidget表头自适应窗口
        self.tblWdgStatus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置第0，4列列宽可以手动调节
        self.tblWdgStatus.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.tblWdgStatus.horizontalHeader().setSectionResizeMode(4, QHeaderView.Interactive)

        # self.pushButton()
        # self.load_server_json()
        self.fun_page_ende()
        self.fun_page_del()
        self.fun_page_revise()
        self.fun_page_add()
        self.fun_page_autoset()

        # self.serverListBox.setCurrentIndex(0)
        # self.proxyListBox.setCurrentIndex(0)

        self.btnStart.clicked.connect(self.fun_btn_start)
        self.btnStop.clicked.connect(self.fun_btn_stop)
        self.btnAllStart.clicked.connect(self.fun_btn_all_start)
        self.btnAllStop.clicked.connect(self.fun_btn_all_stop)

        self.actionAutoSet.triggered.connect(self.fun_page_autoset)
        self.actionAdd.triggered.connect(self.fun_page_add)
        self.actionEnDe.triggered.connect(self.fun_page_ende)
        self.actionRevise.triggered.connect(self.fun_page_revise)
        self.actionDel.triggered.connect(self.fun_page_del)

        self.btnEnPass.clicked.connect(self.fun_pass_encode)
        self.btnDePass.clicked.connect(self.fun_pass_decode)
        self.btnEnOther.clicked.connect(self.fun_other_encode)
        self.btnDeOther.clicked.connect(self.fun_other_decode)

        self.btnAddTarget.clicked.connect(self.fun_add_target)
        self.btnAddProxy.clicked.connect(self.fun_add_proxy)
        self.btnReviseTarget.clicked.connect(self.fun_revise_target)
        self.btnReviseProxy.clicked.connect(self.fun_revise_proxy)
        self.btnDelTarget.clicked.connect(self.fun_del_target)
        self.btnDelProxy.clicked.connect(self.fun_del_proxy)

        self.comboBoxReviseTarget.activated.connect(self.fun_revise_show_select_target)
        self.comboBoxReviseProxy.activated.connect(self.fun_revise_show_select_proxy)
        self.comboBoxDelTarget.activated.connect(self.fun_del_show_select_target)
        self.comboBoxDelProxy.activated.connect(self.fun_del_show_select_proxy)

        # self.serverListBox.currentIndexChanged.connect(self.fun_connect_show_target_info)

        # self.fun_connect_show_target_info()


    def load_server_json(self):
        with open(self.json_file_pth, "r") as f:
            server_data = json.load(f)
        target_info = server_data["Target_Server"]
        proxy_info = server_data["Proxy"]
        # for each_server in server_info.items():
        #     name = each_server[1]["Name"]
        #     self.txtBrowerLog.append(name)
        return server_data, target_info, proxy_info


    def operate_sshtunnel(self, proxy_host, proxy_port, proxy_username, proxy_password, target_host, target_port,
                          client_port):
        try:
            tunnel = SSHTunnelForwarder(
                (proxy_host, proxy_port),
                ssh_username=proxy_username,
                ssh_password=proxy_password,
                remote_bind_address=(target_host, target_port),
                local_bind_address=('localhost', client_port)
            )
            return tunnel
        except Exception as e:
            self.txtBrowerLog.append(e.args[0])
            self.txtBrowerLog.append("<font color='red'> 设置隧道失败 <font>")
            return

    def current_select(self, target_combox, proxy_combox):
        # select_target = self.serverListBox.currentText()
        # select_proxy = self.proxyListBox.currentText()

        select_target = target_combox.currentText()
        select_proxy = proxy_combox.currentText()
        server_data, target_info, proxy_info = self.load_server_json()
        for each_target in server_data['Target_Server'].items():
            if select_target == each_target[1]["Name"]:
                target_host = each_target[1]["Host"]
                target_port = each_target[1]["Port"]
                # target_username = each_target[1]["UserName"]
                client_port = each_target[1]["LocalPort"]
        for each_proxy in server_data['Proxy'].items():
            if select_proxy == each_proxy[1]["Name"]:
                proxy_host = each_proxy[1]["Host"]
                proxy_port = each_proxy[1]["Port"]
                proxy_username = each_proxy[1]["UserName"]
                proxy_userpasswd = each_proxy[1]["UserPass"]
        try:
            proxy_userpasswd = cryptocode.decrypt(cryptocode.decrypt(proxy_userpasswd, self.pass_key), self.other_key)
            target_host = cryptocode.decrypt(target_host, self.other_key)
            proxy_host = cryptocode.decrypt(proxy_host, self.other_key)
        except Exception as e:
            self.txtBrowerLog.append(e.args[0])
            self.txtBrowerLog.append("<font color='red'> 解码出错 <font>")

        return [select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd]

    # def fun_connect_show_target_info(self):
    #     select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select()
    #     self.lineEditLocalPort.setText(str(client_port) + "[可临时修改(不会修改文件)，不修改则默认]")
        # self.lineEditUserName.setText(str(target_username) + "[可临时修改(不会修改文件)，不修改则默认]")

    def update_connect_status(self):
        self.tblWdgStatus.clear()
        self.tblWdgStatus.setRowCount(0)
        self.tblWdgStatus.clearContents()
        self.tblWdgStatus.setHorizontalHeaderLabels(['SSH Method', 'Target Host', 'Target Port', 'Local Port', 'Proxy Host', 'Proxy Port', 'Proxy User'])
        for idx, each_tunnel in enumerate(self.tunnel_start_status):
            self.tblWdgStatus.insertRow(int(self.tblWdgStatus.rowCount()))
            target_host_item = QTableWidgetItem(str(each_tunnel["Target_Host"]))
            target_host_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置内容居中显示
            target_port_item = QTableWidgetItem(str(each_tunnel["Target_Port"]))
            target_port_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            local_port_item = QTableWidgetItem(str(each_tunnel["Local_Port"]))
            local_port_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            local_method_item = QTableWidgetItem('UserName@localhost:'+str(each_tunnel["Local_Port"]))
            local_method_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            proxy_host_item = QTableWidgetItem(str(each_tunnel["Proxy_Host"]))
            proxy_host_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            proxy_port_item = QTableWidgetItem(str(each_tunnel["Proxy_Port"]))
            proxy_port_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            proxy_user_item = QTableWidgetItem(str(each_tunnel["Proxy_User"]))
            proxy_user_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tblWdgStatus.setItem(idx, 0, local_method_item)
            self.tblWdgStatus.setItem(idx, 1, target_host_item)
            self.tblWdgStatus.setItem(idx, 2, target_port_item)
            self.tblWdgStatus.setItem(idx, 3, local_port_item)
            self.tblWdgStatus.setItem(idx, 4, proxy_host_item)
            self.tblWdgStatus.setItem(idx, 5, proxy_port_item)
            self.tblWdgStatus.setItem(idx, 6, proxy_user_item)

            self.tblWdgStatus.update()

    def fun_set_tunnel_to_each_target(self, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd):
        # 同一个Host，只允许建立一个连接
        # client_port = self.lineEditLocalPort.text().rstrip().lstrip()
        # client_port = int(client_port[:client_port.find('[')])
        al_estab_host_count = 0
        al_estab_port_count = 0
        al_estab_username_count = 0
        for each_tunnel in self.tunnel_start_status:
            if target_host == each_tunnel["Target_Host"]:
                if client_port == each_tunnel["Local_Port"]:
                    al_estab_host_count += 1

        if al_estab_host_count == 0:
            self.txtBrowerLog.append("------------Establish Tunnel to {} Server------------".format(str(target_host)))
            self.txtBrowerLog.append(
                "Target Server: {} : {}".format(str(target_host), str(target_port)))
            self.txtBrowerLog.append(
                "Proxy Server: {} @ {} : {}".format(str(proxy_username), str(proxy_host), str(proxy_port)))
            self.txtBrowerLog.append("Local Port: {}".format(str(client_port)))
            tunnel = self.operate_sshtunnel(proxy_host, proxy_port, proxy_username, proxy_userpasswd, target_host,
                                            target_port, client_port)
            if tunnel is not None:
                try:
                    tunnel.start()
                    self.txtBrowerLog.append("<font color='green'> Start Successful <font>")
                    current_tunnel_dict = {"Target_Host": target_host, "Target_Port": target_port, "Local_Port": client_port, "Proxy_Host": proxy_host, "Proxy_Port": proxy_port, "Proxy_User": proxy_username, "Tunnel": tunnel}
                    self.tunnel_start_status.append(current_tunnel_dict)

                except Exception as e:
                    self.txtBrowerLog.append(e.args[0])
                    self.txtBrowerLog.append("<font color='red'> Start Unsuccessful <font>")
        else:
            self.txtBrowerLog.append(
                "------------Already Established Tunnel to {} Server from Local Port {}------------".format(str(target_host), str(client_port)))


    def fun_btn_start(self):

        current_select_data = self.current_select(self.serverListBox, self.proxyListBox)
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = current_select_data
        self.fun_set_tunnel_to_each_target(target_host, target_port, client_port, proxy_host,
                                           proxy_port, proxy_username, proxy_userpasswd)
        self.update_connect_status()

    def fun_btn_stop(self):
        current_select_data = self.current_select(self.serverListBox, self.proxyListBox)
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = current_select_data

        count = 0
        stop_idx = None
        for idx, each_tunnel in enumerate(self.tunnel_start_status):
            if target_host == each_tunnel["Target_Host"]:
                stop_idx = idx
                tunnel = each_tunnel["Tunnel"]
                count += 1

        if count == 1:
            self.txtBrowerLog.append(
                "------------Close Tunnel to {} Server------------".format(str(target_host)))
            try:
                tunnel.stop()
            except Exception as e:
                self.txtBrowerLog.append(e.args[0])
                self.txtBrowerLog.append("<font color='red'> Stop Unsuccessful <font>")
            self.txtBrowerLog.append("<font color='green'> Stop Successful <font>")
            self.tunnel_start_status.pop(stop_idx)

        if count == 0:
            self.txtBrowerLog.append(
                "------------No Establish Tunnel to {} Server------------".format(str(target_host)))
        # if len(self.tunnel_start_status) == 0:
        #     self.txtBrowerLog.append("------------No Establish Tunnel to Any one Server------------")
        self.update_connect_status()

    def fun_btn_all_start(self):
        server_data, target_info, proxy_info = self.load_server_json()
        for each_proxy in server_data['Proxy'].items():
            if 'Default' in each_proxy[1]["Name"]:
                proxy_host = each_proxy[1]["Host"]
                proxy_port = each_proxy[1]["Port"]
                proxy_username = each_proxy[1]["UserName"]
                proxy_userpasswd = each_proxy[1]["UserPass"]

        try:
            proxy_userpasswd = cryptocode.decrypt(cryptocode.decrypt(proxy_userpasswd, self.pass_key),
                                                  self.other_key)
            proxy_host = cryptocode.decrypt(proxy_host, self.other_key)
        except Exception as e:
            self.txtBrowerLog.append(e.args[0])
            self.txtBrowerLog.append("<font color='red'> Get Wrong Proxy Password or Port <font>")

        for each_target in server_data['Target_Server'].items():
            target_host = each_target[1]["Host"]
            target_port = each_target[1]["Port"]
            # target_username = each_target[1]["UserName"]
            client_port = each_target[1]["LocalPort"]

            try:
                target_host = cryptocode.decrypt(target_host, self.other_key)
                self.fun_set_tunnel_to_each_target(target_host, target_port, client_port, proxy_host,
                                                   proxy_port, proxy_username, proxy_userpasswd)
            except Exception as e:
                self.txtBrowerLog.append(e.args[0])
                self.txtBrowerLog.append("<font color='red'> Get Wrong Target Port <font>")

        self.update_connect_status()


    def fun_btn_all_stop(self):
        if len(self.tunnel_start_status) == 0:
            self.txtBrowerLog.append("------------No Establish Tunnel to Any one Server------------")
        for each_tunnel in self.tunnel_start_status:
            self.txtBrowerLog.append(
                "------------Close Tunnel to {} Server------------".format(str(each_tunnel["Target_Host"])))
            try:
                each_tunnel["Tunnel"].stop()
                self.txtBrowerLog.append("<font color='green'> Close Successful <font>")
            except Exception as e:
                self.txtBrowerLog.append(e.args[0])
                self.txtBrowerLog.append("<font color='red'> Close Unsuccessful <font>")


        self.tunnel_start_status.clear()
        self.update_connect_status()

    def fun_page_autoset(self):
        self.stackedWidget.setCurrentIndex(0)
        self.serverListBox.clear()
        self.proxyListBox.clear()
        server_data, target_info, proxy_info = self.load_server_json()
        self.serverListBox.addItems([each_target[1]["Name"] for each_target in target_info.items()])
        self.proxyListBox.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])
        self.update_connect_status()

    def fun_page_add(self):
        self.stackedWidget.setCurrentIndex(1)
        self.txtEditTargetName.clear()
        self.txtEditTargetHost.clear()
        self.txtEditTargetPort.clear()
        # self.txtEditTargetUserName.clear()
        self.txtEditTargetLocalPort.clear()
        self.txtBrowerAddTargetStatus.clear()
        self.txtEditProxyName.clear()
        self.txtEditProxyHost.clear()
        self.txtEditProxyPort.clear()
        self.txtEditProxyUserName.clear()
        self.txtEditProxyUserPass.clear()
        self.txtBrowerAddProxyStatus.clear()

    def fun_page_revise(self):
        self.stackedWidget.setCurrentIndex(2)

        self.comboBoxReviseTarget.clear()
        self.txtEditReviseTargetName.clear()
        self.txtEditReviseTargetHost.clear()
        self.txtEditReviseTargetPort.clear()
        self.txtEditTargetReviseLocalPort.clear()
        self.txtBrowerReviseTargetStatus.clear()

        self.comboBoxReviseProxy.clear()
        self.txtEditReviseProxyName.clear()
        self.txtEditReviseProxyHost.clear()
        self.txtEditReviseProxyPort.clear()
        self.txtEditReviseProxyUserName.clear()
        self.txtEditReviseProxyUserPass.clear()
        self.txtBrowerReviseProxyStatus.clear()

        server_data, target_info, proxy_info = self.load_server_json()
        self.comboBoxReviseTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])
        self.comboBoxReviseProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

        self.fun_revise_show_select_target()
        self.fun_revise_show_select_proxy()


    def fun_page_del(self):
        self.stackedWidget.setCurrentIndex(3)

        self.comboBoxDelTarget.clear()
        self.txtEditDelTargetName.clear()
        self.txtEditDelTargetHost.clear()
        self.txtEditDelTargetPort.clear()
        self.txtEditTargetDelLocalPort.clear()
        self.txtBrowerDelTargetStatus.clear()

        self.comboBoxDelProxy.clear()
        self.txtEditDelProxyName.clear()
        self.txtEditDelProxyHost.clear()
        self.txtEditDelProxyPort.clear()
        self.txtEditDelProxyUserName.clear()
        self.txtEditDelProxyUserPass.clear()
        self.txtBrowerDelProxyStatus.clear()

        server_data, target_info, proxy_info = self.load_server_json()
        self.comboBoxDelTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])
        self.comboBoxDelProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

        self.fun_del_show_select_target()
        self.fun_del_show_select_proxy()

    def fun_page_ende(self):
        self.stackedWidget.setCurrentIndex(4)
        self.txtEnPassInput.clear()
        self.txtBrowerEnPassOutput.clear()
        self.txtDePassInput.clear()
        self.txtBrowerDePassOutput.clear()
        self.txtEnOtherInput.clear()
        self.txtBrowerEnOtherOutput.clear()
        self.txtDeOtherInput.clear()
        self.txtBrowerDeOtherOutput.clear()


    def fun_pass_encode(self):
        self.txtBrowerEnPassOutput.clear()
        pass_encode_input = self.txtEnPassInput.toPlainText().rstrip().lstrip()
        if len(pass_encode_input) == 0:
            self.txtBrowerEnPassOutput.setText("<font color='red'> 不能为空  <font>")
        else:
            try:
                pass_encode_output = cryptocode.encrypt(cryptocode.encrypt(pass_encode_input, self.other_key), self.pass_key)
                self.txtBrowerEnPassOutput.setText(pass_encode_output)
            except Exception as e:
                self.txtBrowerEnPassOutput.append(e.args[0])
                self.txtBrowerEnPassOutput.append("<font color='red'> 编码失败 <font>")


    def fun_pass_decode(self):
        self.txtBrowerDePassOutput.clear()
        pass_decode_input = self.txtDePassInput.toPlainText().rstrip().lstrip()
        if len(pass_decode_input) == 0:
            self.txtBrowerDePassOutput.setText("<font color='red'> 不能为空  <font>")
        else:
            try:
                pass_decode_output = cryptocode.decrypt(cryptocode.decrypt(pass_decode_input, self.pass_key), self.other_key)
                self.txtBrowerDePassOutput.setText(pass_decode_output)
            except Exception as e:
                self.txtBrowerDePassOutput.append(e.args[0])
                self.txtBrowerDePassOutput.append("<font color='red'> 解码失败 <font>")


    def fun_other_encode(self):
        self.txtBrowerEnOtherOutput.clear()
        other_encode_input = self.txtEnOtherInput.toPlainText().rstrip().lstrip()
        if len(other_encode_input) == 0:
            self.txtBrowerEnOtherOutput.setText("<font color='red'> 不能为空  <font>")
        else:
            try:
                other_encode_output = cryptocode.encrypt(other_encode_input, self.other_key),
                self.txtBrowerEnOtherOutput.setText(other_encode_output[0])
            except Exception as e:
                self.txtBrowerEnOtherOutput.append(e.args[0])
                self.txtBrowerEnOtherOutput.append("<font color='red'> 编码失败 <font>")

    def fun_other_decode(self):
        self.txtBrowerDeOtherOutput.clear()
        other_decode_input = self.txtDeOtherInput.toPlainText().rstrip().lstrip()
        if len(other_decode_input) == 0:
            self.txtBrowerDeOtherOutput.setText("<font color='red'> 不能为空  <font>")
        else:
            try:
                other_decode_output = cryptocode.decrypt(other_decode_input, self.other_key),
                self.txtBrowerDeOtherOutput.setText(other_decode_output[0])
            except Exception as e:
                self.txtBrowerDeOtherOutput.append(e.args[0])
                self.txtBrowerDeOtherOutput.append("<font color='red'> 解码失败 <font>")

    def fun_add_target(self):
        name = self.txtEditTargetName.toPlainText().rstrip().lstrip()
        host = self.txtEditTargetHost.toPlainText().rstrip().lstrip()
        port = self.txtEditTargetPort.toPlainText().rstrip().lstrip()
        # username = self.txtEditTargetUserName.toPlainText().rstrip().lstrip()
        localport = self.txtEditTargetLocalPort.toPlainText().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(localport) == 0:
            self.txtBrowerAddTargetStatus.setText(
                "<font color='red'> 不能为空, 添加失败 <font>")
        else:
            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_target in target_info.items():
                if name == each_target[1]["Name"] or int(localport) == int(each_target[1]["LocalPort"]):
                    al_count += 1
                if (host == cryptocode.decrypt(each_target[1]["Host"], self.other_key)):
                    if port == each_target[1]["Port"]:
                        al_count += 1

            if al_count > 0:
                self.txtBrowerAddTargetStatus.setText(
                    "<font color='red'> 存在相同的'Name'或者'LocalPort'或者同一个'Port'的'Host', 添加失败 <font>")
            else:
                try:
                    add_target_server = {
                        "Server_" + name.replace(" ", ""):
                                 {"Name": name,
                                  "Host": cryptocode.encrypt(host, self.other_key),
                                  "Port": int(port),
                                  "LocalPort": int(localport)}}
                    server_data['Target_Server'].update(add_target_server)
                    with open(self.json_file_pth, 'w') as f:
                        json.dump(server_data, f)
                    self.txtBrowerAddTargetStatus.setText(
                        "<font color='green'> 添加成功 <font>")
                except Exception as e:
                    self.txtBrowerAddTargetStatus.append(e.args[0])
                    self.txtBrowerAddTargetStatus.setText(
                        "<font color='red'> 添加失败 <font>")

    def fun_add_proxy(self):
        name = self.txtEditProxyName.toPlainText().rstrip().lstrip()
        host = self.txtEditProxyHost.toPlainText().rstrip().lstrip()
        port = self.txtEditProxyPort.toPlainText().rstrip().lstrip()
        username = self.txtEditProxyUserName.toPlainText().rstrip().lstrip()
        userpass = self.txtEditProxyUserPass.toPlainText().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(username) == 0 or len(userpass) == 0:
            self.txtBrowerAddProxyStatus.setText(
                "<font color='red'> 不能为空, Add Unsuccessful <font>")
        else:

            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_proxy in proxy_info.items():
                if name == each_proxy[1]["Name"]:
                    al_count += 1
                if host == cryptocode.decrypt(each_proxy[1]["Host"], self.other_key):
                    if int(port) == int(each_proxy[1]["Port"]) and str(username) == str(each_proxy[1]["UserName"]):
                        al_count += 1

            if al_count > 0:
                self.txtBrowerAddProxyStatus.setText(
                    "<font color='red'> 存在相同的'Name'或者同一个'Port'和'UserName'的'Host', 添加失败 <font>")
            else:
                try:
                    add_proxy_server = {
                        "Server_" + name.replace(" ", ""):
                            {"Name": name,
                             "Host": cryptocode.encrypt(host, self.other_key),
                             "Port": int(port),
                             "UserName": username,
                             "UserPass": cryptocode.encrypt(cryptocode.encrypt(userpass, self.other_key), self.pass_key)}}
                    server_data['Proxy'].update(add_proxy_server)
                    with open(self.json_file_pth, 'w') as f:
                        json.dump(server_data, f)
                    self.txtBrowerAddProxyStatus.setText(
                        "<font color='green'> 添加成功 <font>")
                except Exception as e:
                    self.txtBrowerAddProxyStatus.append(e.args[0])
                    self.txtBrowerAddProxyStatus.setText(
                        "<font color='red'> 添加失败 <font>")

    def fun_revise_target(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)
        name = self.txtEditReviseTargetName.toPlainText().rstrip().lstrip()
        host = self.txtEditReviseTargetHost.toPlainText().rstrip().lstrip()
        port = self.txtEditReviseTargetPort.toPlainText().rstrip().lstrip()
        # username = self.txtEditTargetUserName.toPlainText().rstrip().lstrip()
        localport = self.txtEditTargetReviseLocalPort.toPlainText().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(localport) == 0:
            self.txtBrowerReviseTargetStatus.setText(
                "<font color='red'> 不能为空, 修改失败 <font>")
        else:
            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_target in target_info.items():
                if name == each_target[1]["Name"] or int(localport) == int(each_target[1]["LocalPort"]):
                    al_count += 1
                if (host == cryptocode.decrypt(each_target[1]["Host"], self.other_key)):
                    if port == each_target[1]["Port"]:
                        al_count += 1

            if al_count > 0:
                self.txtBrowerReviseTargetStatus.setText(
                    "<font color='red'> 存在相同的'Name'或者'LocalPort'或者同一个'Port'的'Host', 修改失败 <font>")
            else:
                reply = QtWidgets.QMessageBox.question(self, '警告',
                                                       "确定修改 [ 'Name':{} 'Host':{} 'LocalPort':{} ] Target Server 为 [ 'Name':{} 'Host':{} 'LocalPort':{} ]吗?".format(
                                                           str(select_target),
                                                           str(target_host),
                                                           str(client_port),
                                                           str(name),
                                                           str(host),
                                                           str(localport)),
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    try:
                        revise_target_server = {
                            "Name": name,
                            "Host": cryptocode.encrypt(host, self.other_key),
                            "Port": int(port),
                            "LocalPort": int(localport)}
                        # 修改内容
                        server_data['Target_Server']["Server_" + select_target.replace(" ", "")].update(
                            revise_target_server)
                        # 修改Key，但是会改变顺序
                        server_data['Target_Server']["Server_" + name.replace(" ", "")] = server_data[
                            'Target_Server'].pop("Server_" + select_target.replace(" ", ""))
                        # server_data['Target_Server'].update(revise_target_server)
                        with open(self.json_file_pth, 'w') as f:
                            json.dump(server_data, f)
                        self.txtBrowerReviseTargetStatus.setText(
                            "<font color='green'> 修改成功 <font>")

                        self.comboBoxReviseTarget.clear()
                        self.txtEditReviseTargetName.clear()
                        self.txtEditReviseTargetHost.clear()
                        self.txtEditReviseTargetPort.clear()
                        self.txtEditTargetReviseLocalPort.clear()

                        server_data, target_info, proxy_info = self.load_server_json()
                        self.comboBoxReviseTarget.addItems(
                            [each_target[1]["Name"] for each_target in target_info.items()])

                        self.fun_revise_show_select_target()
                    except Exception as e:
                        self.txtBrowerReviseTargetStatus.append(e.args[0])
                        self.txtBrowerReviseTargetStatus.setText(
                            "<font color='red'> 修改失败 <font>")
                else:
                    self.txtBrowerReviseTargetStatus.setText(
                        "<font color='red'> 修改失败 <font>")


    def fun_revise_proxy(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)
        name = self.txtEditReviseProxyName.toPlainText().rstrip().lstrip()
        host = self.txtEditReviseProxyHost.toPlainText().rstrip().lstrip()
        port = self.txtEditReviseProxyPort.toPlainText().rstrip().lstrip()
        username = self.txtEditReviseProxyUserName.toPlainText().rstrip().lstrip()
        userpass = self.txtEditReviseProxyUserPass.toPlainText().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(username) == 0 or len(userpass) == 0:
            self.txtBrowerReviseProxyStatus.setText(
                "<font color='red'> 不能为空, 修改失败 <font>")
        else:
            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_proxy in proxy_info.items():
                if name == each_proxy[1]["Name"]:
                    al_count += 1
                if host == cryptocode.decrypt(each_proxy[1]["Host"], self.other_key):
                    if int(port) == int(each_proxy[1]["Port"]) and str(username) == str(each_proxy[1]["UserName"]):
                        al_count += 1

            if al_count > 0:
                self.txtBrowerReviseProxyStatus.setText(
                    "<font color='red'> 存在相同的'Name'或者同一个'Port'和'UserName'的'Host', 添加失败 <font>")
            else:
                reply = QtWidgets.QMessageBox.question(self, '警告',
                                                       "确定修改 [ 'Name':{} {} @ {} : {} ] Proxy Server 为 [ 'Name':{} {} @ {} : {} ]吗?".format(
                                                           str(select_proxy),
                                                           str(proxy_username),
                                                           str(proxy_host),
                                                           str(proxy_port),
                                                           str(name),
                                                           str(username),
                                                           str(host),
                                                           str(port)),
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    try:
                        revise_proxy_server = {
                            "Name": name,
                            "Host": cryptocode.encrypt(host, self.other_key),
                            "Port": int(port),
                            "UserName": username,
                            "UserPass": cryptocode.encrypt(cryptocode.encrypt(userpass, self.other_key),
                                                                self.pass_key)}
                        # 修改内容
                        server_data['Proxy']["Server_" + select_proxy.replace(" ", "")].update(
                            revise_proxy_server)
                        # 修改Key，但是会改变顺序
                        server_data['Proxy']["Server_" + name.replace(" ", "")] = server_data[
                            'Proxy'].pop("Server_" + select_proxy.replace(" ", ""))
                        with open(self.json_file_pth, 'w') as f:
                            json.dump(server_data, f)
                        self.txtBrowerReviseProxyStatus.setText(
                            "<font color='green'> 修改成功 <font>")

                        self.comboBoxReviseProxy.clear()
                        self.txtEditReviseProxyName.clear()
                        self.txtEditReviseProxyHost.clear()
                        self.txtEditReviseProxyPort.clear()
                        self.txtEditReviseProxyUserName.clear()
                        self.txtEditReviseProxyUserPass.clear()

                        server_data, target_info, proxy_info = self.load_server_json()
                        self.comboBoxReviseProxy.addItems(
                            [each_target[1]["Name"] for each_target in target_info.items()])

                        self.fun_revise_show_select_proxy()
                    except Exception as e:
                        self.txtBrowerReviseProxyStatus.append(e.args[0])
                        self.txtBrowerReviseProxyStatus.setText(
                            "<font color='red'> 修改失败 <font>")
                else:
                    self.txtBrowerReviseProxyStatus.setText(
                        "<font color='red'> 修改失败 <font>")

    def fun_del_target(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)
        reply = QtWidgets.QMessageBox.question(self, '警告',
                                               "确定删除 [ 'Name':{} 'Host':{} 'LocalPort':{} ] Target Server吗?".format(str(select_target), str(target_host), str(client_port)),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            server_data, target_info, proxy_info = self.load_server_json()
            try:
                del server_data["Target_Server"]["Server_" + select_target.replace(" ", "")]
                with open(self.json_file_pth, 'w') as f:
                    json.dump(server_data, f)
                self.txtBrowerDelTargetStatus.setText("<font color='green'> 删除成功 <font>")
                self.comboBoxDelTarget.clear()
                self.txtEditDelTargetName.clear()
                self.txtEditDelTargetHost.clear()
                self.txtEditDelTargetPort.clear()
                self.txtEditTargetDelLocalPort.clear()

                server_data, target_info, proxy_info = self.load_server_json()
                self.comboBoxDelTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])

                self.fun_del_show_select_target()
            except Exception as e:
                self.txtBrowerDelTargetStatus.append(e.args[0])
                self.txtBrowerDelTargetStatus.setText("<font color='red'> 删除失败 <font>")
        else:
            self.txtBrowerDelTargetStatus.setText("<font color='red'> 删除失败 <font>")

    def fun_del_proxy(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)
        reply = QtWidgets.QMessageBox.question(self, '警告',
                                               "确定删除 [ 'Name':{} {} @ {} : {} ] Proxy Server吗?".format(str(select_proxy), str(proxy_username), str(proxy_host), str(proxy_port)),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            server_data, target_info, proxy_info = self.load_server_json()
            try:
                del server_data["Proxy"]["Server_" + select_proxy.replace(" ", "")]
                with open(self.json_file_pth, 'w') as f:
                    json.dump(server_data, f)
                self.txtBrowerDelProxyStatus.setText("<font color='green'> 删除成功 <font>")
                self.comboBoxDelProxy.clear()
                self.txtEditDelProxyName.clear()
                self.txtEditDelProxyHost.clear()
                self.txtEditDelProxyPort.clear()
                self.txtEditDelProxyUserName.clear()
                self.txtEditDelProxyUserPass.clear()

                server_data, target_info, proxy_info = self.load_server_json()
                self.comboBoxDelProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

                self.fun_del_show_select_proxy()
            except Exception as e:
                self.txtBrowerDelProxyStatus.append(e.args[0])
                self.txtBrowerDelProxyStatus.setText("<font color='red'> 删除失败 <font>")
        else:
            self.txtBrowerDelProxyStatus.setText("<font color='red'> 删除失败 <font>")

    def fun_del_show_select_target(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)
        self.txtEditDelTargetName.setText(str(select_target))
        self.txtEditDelTargetHost.setText(str(target_host))
        self.txtEditDelTargetPort.setText(str(target_port))
        self.txtEditTargetDelLocalPort.setText(str(client_port))

    def fun_del_show_select_proxy(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)
        self.txtEditDelProxyName.setText(str(select_proxy))
        self.txtEditDelProxyHost.setText(str(proxy_host))
        self.txtEditDelProxyPort.setText(str(proxy_port))
        self.txtEditDelProxyUserName.setText(str(proxy_username))
        self.txtEditDelProxyUserPass.setText(str(proxy_userpasswd))

    def fun_revise_show_select_target(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)
        self.txtEditReviseTargetName.setText(str(select_target))
        self.txtEditReviseTargetHost.setText(str(target_host))
        self.txtEditReviseTargetPort.setText(str(target_port))
        self.txtEditTargetReviseLocalPort.setText(str(client_port))

    def fun_revise_show_select_proxy(self):
        select_target, select_proxy, target_host, target_port, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)
        self.txtEditReviseProxyName.setText(str(select_proxy))
        self.txtEditReviseProxyHost.setText(str(proxy_host))
        self.txtEditReviseProxyPort.setText(str(proxy_port))
        self.txtEditReviseProxyUserName.setText(str(proxy_username))
        self.txtEditReviseProxyUserPass.setText(str(proxy_userpasswd))

    def statusShowTime(self):
        self.Timer = QTimer()  # 自定义QTimer类
        self.Timer.start(1000)  # 每1s运行一次
        self.Timer.timeout.connect(self.updateTime)  # 与updateTime函数连接

    def updateTime(self):
        time = QDateTime.currentDateTime()  # 获取现在的时间
        timeplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')  # 设置显示时间的格式
        self.lblTime.setText(timeplay)  # 设置timeLabel控件显示的内容

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, '警告', "确定关闭当前窗口，如关闭当前窗口，将断开所有隧道连接?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            for each_tunnel in self.tunnel_start_status:
                each_tunnel["Tunnel"].stop()
            self.tunnel_start_status.clear()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = setTunnel()
#
#     window.show()
#     sys.exit(app.exec_())
