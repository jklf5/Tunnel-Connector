import time

import paramiko
from PyQt5.Qt import QApplication, QTimer, QTableWidgetItem, Qt, QFileDialog, QDateTime
from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtWidgets import QHeaderView

from .setTunnelUI import Ui_MainWin
from sshtunnel import SSHTunnelForwarder
import json
import cryptocode


# import os
# import sys
#
# if hasattr(sys, 'frozen'):
#     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']


class setTunnel(QtWidgets.QMainWindow, Ui_MainWin):

    def __init__(self, parent=None, *args, **kwargs):
        # TODO 刷新SSH STATUS，取消每次切换到autoset页面刷新一次already established，而是在设定的刷新时间和点击连接断开等按钮后刷新一次。
        super().__init__(parent, *args, **kwargs)
        # self.setWindowTitle("test")
        # self.resize(600, 500)
        self.setupUi(self)
        self.statusShowTime()
        # self.setWindowIcon(QtGui.QIcon('./tunnel_logo_default.png'))
        # self.btnStart.setStyleSheet(
        #     'background-color: rgb(192, 192, 192);border-radius: 10px; border: 1px groove gray;border-style: outset;')
        # self.json_file_pth = './serverList2_test.json'
        self.config_settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
        # self.config_settings.setValue("CONFIG/Json_File_Path", self.json_file_pth)
        self.json_file_pth = self.config_settings.value("CONFIG/Json_File_Path")
        self.refresh_ssh_is_alive_time = self.config_settings.value("CONFIG/Refresh_SSH_Is_Alive_Time")
        if self.json_file_pth is None:
            QtWidgets.QMessageBox.warning(self, "警告", "CONFIG文件文件已经损坏，无法继续打开应用")
            exit()
        self.tunnel_start_status = []
        self.other_key = "EjdsB27ciQMK2LHf"
        self.pass_key = "F1jgDu5trCyxmUqC"
        # 设置TableWidget不可编辑
        self.tblWdgStatus.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblWdgAvailableTargetServer.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblWdgAvailableProxyServer.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置TableWidget根据内容调整列和行，需要在更新了数据后再操作
        # https://blog.csdn.net/qq_45769063/article/details/122097738
        # https://blog.csdn.net/yl_best/article/details/84070231
        # QHeaderView.Stretch设置TableWidget表头根据窗口平均分配，限制了其他操作
        # self.tblWdgAvailableTargetServer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tblWdgAvailableProxyServer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tblWdgStatus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tblWdgStatus.horizontalHeader().setCascadingSectionResizes(True)
        # self.tblWdgAvailableTargetServer.horizontalHeader().setCascadingSectionResizes(True)
        # self.tblWdgAvailableProxyServer.horizontalHeader().setCascadingSectionResizes(True)

        # 伸展最后一列，实验发现设置stretchLastSection更有效，其允许手动调整所有列宽。
        # self.tblWdgStatus.horizontalHeader().stretchLastSection()
        self.tblWdgStatus.horizontalHeader().setStretchLastSection(True)
        self.tblWdgAvailableTargetServer.horizontalHeader().setStretchLastSection(True)
        self.tblWdgAvailableProxyServer.horizontalHeader().setStretchLastSection(True)
        # self.tblWdgAvailableTargetServer.horizontalHeader().stretchLastSection()
        # self.tblWdgAvailableProxyServer.horizontalHeader().stretchLastSection()
        # 设置第0，4列列宽可以手动调节
        # self.tblWdgStatus.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        # self.tblWdgStatus.horizontalHeader().setSectionResizeMode(4, QHeaderView.Interactive)

        # 设置密码框显示圆点。
        # self.lineEditProxyUserPass.setEchoMode(QLineEdit.Password)
        # self.lineEditReviseProxyUserPass.setEchoMode(QLineEdit.Password)

        # self.pushButton()
        if self.json_is_null() != 0:
            # self.fun_page_add()
            self.fun_page_ende()
            self.fun_page_del()
            self.fun_page_revise()
            self.fun_page_add()
            self.fun_page_autoset()

        # self.serverListBox.setCurrentIndex(0)
        # self.proxyListBox.setCurrentIndex(0)

        self.fun_refresh_tunnel()

        self.btnStart.clicked.connect(self.fun_btn_start)
        self.btnStop.clicked.connect(self.fun_btn_stop)
        self.btnAllStart.clicked.connect(self.fun_btn_all_start)
        self.btnAllStop.clicked.connect(self.fun_btn_all_stop)

        self.actionAutoSet.triggered.connect(self.fun_page_autoset)
        self.actionAdd.triggered.connect(self.fun_page_add)
        self.actionEnDe.triggered.connect(self.fun_page_ende)
        self.actionRevise.triggered.connect(self.fun_page_revise)
        self.actionDel.triggered.connect(self.fun_page_del)
        self.actionSelectJsonFile.triggered.connect(self.fun_select_json_file)

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
        self.btnClearLog.clicked.connect(self.fun_clear_log)
        self.btnReviseRefreshTime.clicked.connect(self.fun_revise_refresh_time)
        # self.btnSelectJsonFile.clicked.connect(self.fun_select_json_file)

        self.comboBoxReviseTarget.activated.connect(self.fun_revise_show_select_target)
        self.comboBoxReviseProxy.activated.connect(self.fun_revise_show_select_proxy)
        self.comboBoxDelTarget.activated.connect(self.fun_del_show_select_target)
        self.comboBoxDelProxy.activated.connect(self.fun_del_show_select_proxy)

        # self.serverListBox.currentIndexChanged.connect(self.fun_connect_show_target_info)

        # self.fun_connect_show_target_info()

    def fun_clear_log(self):
        self.txtBrowerLog.clear()

    def load_server_json(self):
        try:
            with open(self.json_file_pth, "r") as f:
                server_data = json.load(f)
            target_info = server_data["Target_Server"]
            proxy_info = server_data["Proxy"]
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "警告", "Json 文件：[" + self.json_file_pth + "] 文件已经损坏，无法继续打开应用")
            exit()

        if len(server_data) == 0:
            QtWidgets.QMessageBox.warning(self, "警告", "Json 文件：[" + self.json_file_pth + "] 文件已经损坏，无法继续打开应用")
            exit()

        return server_data, target_info, proxy_info

    def json_is_null(self):
        server_data, target_info, proxy_info = self.load_server_json()
        if len(target_info) == 0:
            reply = QtWidgets.QMessageBox.question(self, '警告', "Target Server 一个都没有，你只能留在这",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.fun_page_add()
                # self.stackedWidget.setCurrentIndex(1)
                return 0
            else:
                exit()

        if len(proxy_info) == 0:
            reply = QtWidgets.QMessageBox.question(self, '警告', "Proxy Server 一个都没有，你只能留在这",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                # self.stackedWidget.setCurrentIndex(1)
                self.fun_page_add()
                return 0
            else:
                exit()

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
            self.txtBrowerLog.append("<font color='red'> 设置隧道失败！ <font>")
            return

    def current_select(self, target_combox, proxy_combox):
        # select_target = self.serverListBox.currentText()
        # select_proxy = self.proxyListBox.currentText()

        if self.json_is_null() != 0:
            select_target = target_combox.currentText()
            select_proxy = proxy_combox.currentText()
            server_data, target_info, proxy_info = self.load_server_json()

            for each_target in server_data['Target_Server'].items():
                if select_target == each_target[1]["Name"]:
                    target_host = each_target[1]["Host"]
                    target_port = each_target[1]["Port"]
                    target_username = each_target[1]["UserName"]
                    target_userpass = each_target[1]["UserPass"]
                    client_port = each_target[1]["LocalPort"]
            for each_proxy in server_data['Proxy'].items():
                if select_proxy == each_proxy[1]["Name"]:
                    proxy_host = each_proxy[1]["Host"]
                    proxy_port = each_proxy[1]["Port"]
                    proxy_username = each_proxy[1]["UserName"]
                    proxy_userpasswd = each_proxy[1]["UserPass"]
            try:
                target_userpass = cryptocode.decrypt(cryptocode.decrypt(target_userpass, self.pass_key),
                                                      self.other_key)
                proxy_userpasswd = cryptocode.decrypt(cryptocode.decrypt(proxy_userpasswd, self.pass_key),
                                                      self.other_key)
                target_host = cryptocode.decrypt(target_host, self.other_key)
                proxy_host = cryptocode.decrypt(proxy_host, self.other_key)
            except Exception as e:
                self.txtBrowerLog.append(e.args[0])
                self.txtBrowerLog.append("<font color='red'> 解码出错 <font>")

            return [select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port,
                    proxy_username, proxy_userpasswd]

    # def fun_connect_show_target_info(self):
    #     select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port,
    #     #                     proxy_username, proxy_userpasswd = self.current_select()
    #     self.lineEditLocalPort.setText(str(client_port) + "[可临时修改(不会修改文件)，不修改则默认]")
    # self.lineEditUserName.setText(str(target_username) + "[可临时修改(不会修改文件)，不修改则默认]")

    def update_available_server(self):
        self.tblWdgAvailableTargetServer.clear()
        self.tblWdgAvailableTargetServer.setRowCount(0)
        self.tblWdgAvailableTargetServer.clearContents()
        # self.tblWdgStatus.setHorizontalHeaderLabels(['Local Port', 'SSH Method', 'Target Host', 'Target Port', 'Proxy Host', 'Proxy Port', 'Proxy User'])
        self.tblWdgAvailableTargetServer.setHorizontalHeaderLabels(['Name', 'Target UserName', 'Target Host:Port', 'Local Port'])
        server_data, target_info, proxy_info = self.load_server_json()
        try:
            for idx, each_target in enumerate(target_info.items()):
                self.tblWdgAvailableTargetServer.insertRow(int(self.tblWdgAvailableTargetServer.rowCount()))
                target_name_item = QTableWidgetItem(str(each_target[1]["Name"]))
                target_name_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置内容居中显示
                target_username_item = QTableWidgetItem(str(each_target[1]["UserName"]))
                target_username_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                target_server_item = QTableWidgetItem(
                    "{}:{}".format(str(cryptocode.decrypt(each_target[1]["Host"], self.other_key)),
                                   str(each_target[1]["Port"])))
                target_server_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                local_port_item = QTableWidgetItem(str(each_target[1]["LocalPort"]))
                local_port_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tblWdgAvailableTargetServer.setItem(idx, 0, target_name_item)
                self.tblWdgAvailableTargetServer.setItem(idx, 1, target_username_item)
                self.tblWdgAvailableTargetServer.setItem(idx, 2, target_server_item)
                self.tblWdgAvailableTargetServer.setItem(idx, 3, local_port_item)

                self.tblWdgAvailableTargetServer.update()
        except Exception as e:
            self.txtBrowerLog.append(e.args[0])
            self.txtBrowerLog.append("<font color='red'> 检索可用Target Server出错 <font>")

        self.tblWdgAvailableProxyServer.clear()
        self.tblWdgAvailableProxyServer.setRowCount(0)
        self.tblWdgAvailableProxyServer.clearContents()
        # self.tblWdgStatus.setHorizontalHeaderLabels(['Local Port', 'SSH Method', 'Target Host', 'Target Port', 'Proxy Host', 'Proxy Port', 'Proxy User'])
        self.tblWdgAvailableProxyServer.setHorizontalHeaderLabels(['Name', 'Proxy UserName', 'Proxy Host:Port'])

        server_data, target_info, proxy_info = self.load_server_json()
        try:
            for idx, each_proxy in enumerate(proxy_info.items()):
                self.tblWdgAvailableProxyServer.insertRow(int(self.tblWdgAvailableProxyServer.rowCount()))
                proxy_name_item = QTableWidgetItem(str(each_proxy[1]["Name"]))
                proxy_name_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置内容居中显示
                proxy_username_item = QTableWidgetItem(str(each_proxy[1]["UserName"]))
                proxy_username_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                proxy_server_item = QTableWidgetItem(
                    "{}:{}".format(str(cryptocode.decrypt(each_proxy[1]["Host"], self.other_key)),
                                   str(each_proxy[1]["Port"])))
                proxy_server_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tblWdgAvailableProxyServer.setItem(idx, 0, proxy_name_item)
                self.tblWdgAvailableProxyServer.setItem(idx, 1, proxy_username_item)
                self.tblWdgAvailableProxyServer.setItem(idx, 2, proxy_server_item)

                self.tblWdgAvailableProxyServer.update()
        except Exception as e:
            self.txtBrowerLog.append(e.args[0])
            self.txtBrowerLog.append("<font color='red'> 检索 可用Proxy Server出错 <font>")

        # 设置TableWidget根据内容调整列和行
        # self.tblWdgAvailableTargetServer.resizeRowsToContents()
        # self.tblWdgAvailableProxyServer.resizeRowsToContents()
        
        # 在刷新页面时，resizeColumnsToContents会和horizontalHeader().setStretchLastSection(True)产生冲突
        # self.tblWdgAvailableTargetServer.resizeColumnsToContents()
        # self.tblWdgAvailableProxyServer.resizeColumnsToContents()
        
        # self.tblWdgAvailableProxyServer.horizontalHeader().setStretchLastSection(True)
        # 但是setSectionResizeMode和setStretchLastSection不会产生冲突
        self.tblWdgAvailableTargetServer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tblWdgAvailableTargetServer.horizontalHeader().setStretchLastSection(True)
        self.tblWdgAvailableProxyServer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tblWdgAvailableProxyServer.horizontalHeader().setStretchLastSection(True)


    def update_connect_status(self):
        self.tblWdgStatus.clear()
        # self.tblWdgStatus.horizontalHeader().stretchLastSection()
        self.tblWdgStatus.setRowCount(0)
        self.tblWdgStatus.clearContents()
        # self.tblWdgStatus.setHorizontalHeaderLabels(['Local Port', 'SSH Method', 'Target Host', 'Target Port', 'Proxy Host', 'Proxy Port', 'Proxy User'])
        self.tblWdgStatus.setHorizontalHeaderLabels(['Local Port', 'SSH Method', 'Target Server', 'Proxy Server', 'SSH Status'])

        for idx, each_tunnel in enumerate(self.tunnel_start_status):
            self.tblWdgStatus.insertRow(int(self.tblWdgStatus.rowCount()))
            local_port_item = QTableWidgetItem(str(each_tunnel["Local_Port"]))
            local_port_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置内容居中显示
            local_method_item = QTableWidgetItem('UserName@localhost:' + str(each_tunnel["Local_Port"]))
            local_method_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            target_server_item = QTableWidgetItem(
                '{}:{}'.format(str(each_tunnel["Target_Host"]), str(each_tunnel["Target_Port"])))
            target_server_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            proxy_server_item = QTableWidgetItem(
                '{}@{}:{}'.format(str(each_tunnel["Proxy_User"]), str(each_tunnel["Proxy_Host"]),
                                  str(each_tunnel["Proxy_Port"])))
            proxy_server_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tblWdgStatus.setItem(idx, 0, local_port_item)
            self.tblWdgStatus.setItem(idx, 1, local_method_item)
            self.tblWdgStatus.setItem(idx, 2, target_server_item)
            self.tblWdgStatus.setItem(idx, 3, proxy_server_item)

            self.tblWdgStatus.update()

        # 设置TableWidget根据内容调整列和行
        # self.tblWdgStatus.resizeColumnsToContents()
        # self.tblWdgStatus.resizeRowsToContents()
        # 或者
        # self.tblWdgStatus.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # self.tblWdgStatusverticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.tblWdgStatus.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tblWdgStatus.horizontalHeader().setStretchLastSection(True)

        # self.tblWdgStatus.horizontalHeader().setCascadingSectionResizes(True)
        # self.tblWdgStatus.horizontalHeader().stretchLastSection()
        # self.tblWdgStatus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def fun_set_tunnel_to_each_target(self, target_host, target_port, client_port, proxy_host, proxy_port,
                                      proxy_username, proxy_userpasswd):
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
            self.txtBrowerLog.append("--------Establish Tunnel to {} Server--------".format(str(target_host)))
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
                    current_tunnel_dict = {"Target_Host": target_host, "Target_Port": target_port,
                                           "Local_Port": client_port, "Proxy_Host": proxy_host,
                                           "Proxy_Port": proxy_port, "Proxy_User": proxy_username, "Tunnel": tunnel}
                    self.tunnel_start_status.append(current_tunnel_dict)

                except Exception as e:
                    self.txtBrowerLog.append(e.args[0])
                    self.txtBrowerLog.append("<font color='red'> Start Unsuccessful <font>")
        else:
            self.txtBrowerLog.append(
                "<font color='red'> --------Already Established Tunnel to {} Server from Local Port {}-------- <font>".format(str(target_host),
                                                                                                    str(client_port)))

    def fun_btn_start(self):

        current_select_data = self.current_select(self.serverListBox, self.proxyListBox)
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = current_select_data
        self.fun_set_tunnel_to_each_target(target_host, target_port, client_port, proxy_host,
                                           proxy_port, proxy_username, proxy_userpasswd)
        self.update_connect_status()

    def fun_btn_stop(self):
        current_select_data = self.current_select(self.serverListBox, self.proxyListBox)
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = current_select_data

        count = 0
        stop_idx = None
        for idx, each_tunnel in enumerate(self.tunnel_start_status):
            if target_host == each_tunnel["Target_Host"]:
                stop_idx = idx
                tunnel = each_tunnel["Tunnel"]
                count += 1

        if count == 1:
            self.txtBrowerLog.append(
                "--------Close Tunnel to {} Server--------".format(str(target_host)))
            try:
                tunnel.stop()
            except Exception as e:
                self.txtBrowerLog.append(e.args[0])
                self.txtBrowerLog.append("<font color='red'> Stop Unsuccessful <font>")
            self.txtBrowerLog.append("<font color='green'> Stop Successful <font>")
            self.tunnel_start_status.pop(stop_idx)

        if count == 0:
            self.txtBrowerLog.append(
                "<font color='red'> --------No Establish Tunnel to {} Server-------- <font>".format(str(target_host)))
        # if len(self.tunnel_start_status) == 0:
        #     self.txtBrowerLog.append("--------No Establish Tunnel to Any one Server--------")
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
            self.txtBrowerLog.append("<font color='red'> --------No Establish Tunnel to Any one Server-------- <font>")
        for each_tunnel in self.tunnel_start_status:
            self.txtBrowerLog.append(
                "--------Close Tunnel to {} Server--------".format(str(each_tunnel["Target_Host"])))
            try:
                each_tunnel["Tunnel"].stop()
                self.txtBrowerLog.append("<font color='green'> Close Successful <font>")
            except Exception as e:
                self.txtBrowerLog.append(e.args[0])
                self.txtBrowerLog.append("<font color='red'> Close Unsuccessful <font>")

        self.tunnel_start_status.clear()
        self.update_connect_status()

    def fun_page_autoset(self):
        if self.json_is_null() != 0:
            self.serverListBox.clear()
            self.proxyListBox.clear()
            self.lblSelectJson.clear()
            self.lineEditRefreshTime.clear()
            self.lblSelectJson.setText(str(self.json_file_pth))  # .split('/')[-1]
            server_data, target_info, proxy_info = self.load_server_json()
            self.serverListBox.addItems([each_target[1]["Name"] for each_target in target_info.items()])
            self.proxyListBox.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])
            self.lineEditRefreshTime.setText(str(self.refresh_ssh_is_alive_time))
            self.update_connect_status()
            self.update_available_server()

            self.stackedWidget.setCurrentIndex(0)


    def fun_page_add(self):
        self.txtEditTargetName.clear()
        self.txtEditTargetHost.clear()
        self.txtEditTargetPort.clear()
        self.txtEditTargetUserName.clear()
        self.lineEditTargetUserPass.clear()
        self.txtEditTargetLocalPort.clear()
        self.txtBrowerAddTargetStatus.clear()
        self.txtEditProxyName.clear()
        self.txtEditProxyHost.clear()
        self.txtEditProxyPort.clear()
        self.txtEditProxyUserName.clear()
        # self.txtEditProxyUserPass.clear()
        self.lineEditProxyUserPass.clear()
        self.txtBrowerAddProxyStatus.clear()
        self.stackedWidget.setCurrentIndex(1)

    def fun_page_revise(self):
        if self.json_is_null() != 0:

            self.txtBrowerReviseTargetStatus.clear()

            self.txtBrowerReviseProxyStatus.clear()

            self.comboBoxReviseTarget.clear()
            self.comboBoxReviseProxy.clear()
            server_data, target_info, proxy_info = self.load_server_json()
            self.comboBoxReviseTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])
            self.comboBoxReviseProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

            self.fun_revise_show_select_target()
            self.fun_revise_show_select_proxy()
            self.stackedWidget.setCurrentIndex(2)

    def fun_page_del(self):
        if self.json_is_null() != 0:

            self.txtBrowerDelTargetStatus.clear()
            self.txtBrowerDelProxyStatus.clear()

            self.comboBoxDelTarget.clear()
            self.comboBoxDelProxy.clear()
            server_data, target_info, proxy_info = self.load_server_json()
            self.comboBoxDelTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])
            self.comboBoxDelProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

            self.fun_del_show_select_target()
            self.fun_del_show_select_proxy()
            self.stackedWidget.setCurrentIndex(3)

    def fun_page_ende(self):
        self.txtEnPassInput.clear()
        self.txtBrowerEnPassOutput.clear()
        self.txtDePassInput.clear()
        self.txtBrowerDePassOutput.clear()
        self.txtEnOtherInput.clear()
        self.txtBrowerEnOtherOutput.clear()
        self.txtDeOtherInput.clear()
        self.txtBrowerDeOtherOutput.clear()
        self.stackedWidget.setCurrentIndex(4)

    def fun_pass_encode(self):
        self.txtBrowerEnPassOutput.clear()
        pass_encode_input = self.txtEnPassInput.toPlainText().rstrip().lstrip()
        if len(pass_encode_input) == 0:
            self.txtBrowerEnPassOutput.setText("<font color='red'> 不能为空  <font>")
        else:
            try:
                pass_encode_output = cryptocode.encrypt(cryptocode.encrypt(pass_encode_input, self.other_key),
                                                        self.pass_key)
                self.txtBrowerEnPassOutput.setText(pass_encode_output)
            except Exception as e:
                self.txtBrowerEnPassOutput.append(e.args[0])
                self.txtBrowerEnPassOutput.append("<font color='red'> 编码失败！ <font>")

    def fun_pass_decode(self):
        self.txtBrowerDePassOutput.clear()
        pass_decode_input = self.txtDePassInput.toPlainText().rstrip().lstrip()
        if len(pass_decode_input) == 0:
            self.txtBrowerDePassOutput.setText("<font color='red'> 不能为空  <font>")
        else:
            try:
                pass_decode_output = cryptocode.decrypt(cryptocode.decrypt(pass_decode_input, self.pass_key),
                                                        self.other_key)
                self.txtBrowerDePassOutput.setText(pass_decode_output)
            except Exception as e:
                self.txtBrowerDePassOutput.append(e.args[0])
                self.txtBrowerDePassOutput.append("<font color='red'> 解码失败！ <font>")

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
                self.txtBrowerEnOtherOutput.append("<font color='red'> 编码失败！ <font>")

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
                self.txtBrowerDeOtherOutput.append("<font color='red'> 解码失败！ <font>")

    def fun_add_target(self):
        name = self.txtEditTargetName.toPlainText().rstrip().lstrip()
        host = self.txtEditTargetHost.toPlainText().rstrip().lstrip()
        port = self.txtEditTargetPort.toPlainText().rstrip().lstrip()
        username = self.txtEditTargetUserName.toPlainText().rstrip().lstrip()
        userpass = self.lineEditTargetUserPass.text().rstrip().lstrip()
        localport = self.txtEditTargetLocalPort.toPlainText().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(localport) == 0:
            self.txtBrowerAddTargetStatus.setText(
                "<font color='red'> 不能为空, 添加失败！ <font>")
        else:
            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_target in target_info.items():
                if name == each_target[1]["Name"] or int(localport) == int(each_target[1]["LocalPort"]):
                    # 不允许相同的’Name‘或者’LocalPort‘
                    al_count += 1
                if host == cryptocode.decrypt(each_target[1]["Host"], self.other_key):
                    if int(port) == int(each_target[1]["Port"]) and str(username) == str(each_target[1]["UserName"]):
                        # 不允许同一个 Host:Port 或者 UserName@Host
                        al_count += 1

            if al_count > 0:
                self.txtBrowerAddTargetStatus.setText(
                    "<font color='red'> 存在相同的'Name'或者'LocalPort'。存在同一个'Port'或'UserName'的'Host'。添加失败！ <font>")
            else:
                try:
                    add_target_server = {
                        "Server_" + name.replace(" ", ""):
                            {"Name": name,
                             "Host": cryptocode.encrypt(host, self.other_key),
                             "Port": int(port),
                             "UserName": username,
                             "UserPass": cryptocode.encrypt(cryptocode.encrypt(userpass, self.other_key),
                                                            self.pass_key),
                             "LocalPort": int(localport)}}
                    server_data['Target_Server'].update(add_target_server)
                    with open(self.json_file_pth, 'w') as f:
                        json.dump(server_data, f)
                    self.txtBrowerAddTargetStatus.setText(
                        "<font color='green'> 添加 [ 'Name':{} 'Host':{} 'Port':{} 'UserNmae':{} 'LocalPort':{} 成功 ] <font>".format(str(name), str(host), str(port), str(username), str(localport)))
                except Exception as e:
                    self.txtBrowerAddTargetStatus.setText(e.args[0])
                    self.txtBrowerAddTargetStatus.append(
                        "<font color='red'> 存储出错，添加失败！ <font>")

    def fun_add_proxy(self):
        name = self.txtEditProxyName.toPlainText().rstrip().lstrip()
        host = self.txtEditProxyHost.toPlainText().rstrip().lstrip()
        port = self.txtEditProxyPort.toPlainText().rstrip().lstrip()
        username = self.txtEditProxyUserName.toPlainText().rstrip().lstrip()
        # userpass = self.txtEditProxyUserPass.toPlainText().rstrip().lstrip()
        userpass = self.lineEditProxyUserPass.text().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(username) == 0 or len(userpass) == 0:
            self.txtBrowerAddProxyStatus.setText(
                "<font color='red'> 不能为空, Add Unsuccessful <font>")
        else:

            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_proxy in proxy_info.items():
                if name == each_proxy[1]["Name"]:
                    # 不允许同名
                    al_count += 1
                if host == cryptocode.decrypt(each_proxy[1]["Host"], self.other_key):
                    if int(port) == int(each_proxy[1]["Port"]) and str(username) == str(each_proxy[1]["UserName"]):
                        # 不允许同一个 Host:Port 或者 UserName@Host
                        al_count += 1

            if al_count > 0:
                self.txtBrowerAddProxyStatus.setText(
                    "<font color='red'> 存在相同的'Name'，或者同一个'Port'或'UserName'的'Host', 添加失败！ <font>")
            else:
                try:
                    add_proxy_server = {
                        "Server_" + name.replace(" ", ""):
                            {"Name": name,
                             "Host": cryptocode.encrypt(host, self.other_key),
                             "Port": int(port),
                             "UserName": username,
                             "UserPass": cryptocode.encrypt(cryptocode.encrypt(userpass, self.other_key),
                                                            self.pass_key)}}
                    server_data['Proxy'].update(add_proxy_server)
                    with open(self.json_file_pth, 'w') as f:
                        json.dump(server_data, f)
                    self.txtBrowerAddProxyStatus.setText(
                        "<font color='green'> 添加 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} ] 成功 <font>".format(str(name), str(host), str(port), str(username)))
                except Exception as e:
                    self.txtBrowerAddProxyStatus.setText(e.args[0])
                    self.txtBrowerAddProxyStatus.append(
                        "<font color='red'> 存储出错，添加失败！ <font>")

    def fun_revise_target(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)
        name = self.txtEditReviseTargetName.toPlainText().rstrip().lstrip()
        host = self.txtEditReviseTargetHost.toPlainText().rstrip().lstrip()
        port = self.txtEditReviseTargetPort.toPlainText().rstrip().lstrip()
        username = self.txtEditReviseTargetUserName.toPlainText().rstrip().lstrip()
        userpass = self.lineEditReviseTargetUserPass.text().rstrip().lstrip()
        localport = self.txtEditTargetReviseLocalPort.toPlainText().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(localport) == 0:
            self.txtBrowerReviseTargetStatus.setText(
                "<font color='red'> 不能为空, 修改失败！ <font>")
        else:
            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_target in target_info.items():
                if select_target == each_target[1]["Name"]:
                    # 绕过当前选项自己，可能会出bug
                    continue
                else:
                    if name == each_target[1]["Name"] or int(localport) == int(each_target[1]["LocalPort"]):
                        # 不允许相同的’Name‘或者’LocalPort‘
                        al_count += 1
                    if host == cryptocode.decrypt(each_target[1]["Host"], self.other_key):
                        if int(port) == int(each_target[1]["Port"]) and str(username) == str(
                                each_target[1]["UserName"]):
                            # 不允许同一个 Host:Port 或者 UserName@Host
                            al_count += 1

            if al_count > 0:
                self.txtBrowerReviseTargetStatus.setText(
                    "<font color='red'> 存在相同的'LocalPort'或和其他'Name'冲突。存在同一个'Port'或'UserName'的'Host'。 修改失败！ <font>")
            else:
                reply = QtWidgets.QMessageBox.question(self, '警告',
                                                       "确定修改 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} 'LocalPort':{} ] Target Server 为 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} 'LocalPort':{} ]吗?".format(
                                                           str(select_target),
                                                           str(target_host),
                                                           str(target_port),
                                                           str(target_username),
                                                           str(client_port),
                                                           str(name),
                                                           str(host),
                                                           str(port),
                                                           str(username),
                                                           str(localport)),
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    try:
                        revise_target_server = {
                            "Name": name,
                            "Host": cryptocode.encrypt(host, self.other_key),
                            "Port": int(port),
                            "UserName": username,
                            "UserPass": cryptocode.encrypt(cryptocode.encrypt(userpass, self.other_key),
                                                           self.pass_key),
                            "LocalPort": int(localport)}
                        # 修改内容
                        server_data['Target_Server']["Server_" + select_target.replace(" ", "")].update(
                            revise_target_server)
                        if not name == select_target:
                            # 修改Key，但是会改变顺序
                            server_data['Target_Server']["Server_" + name.replace(" ", "")] = server_data[
                                'Target_Server'].pop("Server_" + select_target.replace(" ", ""))

                        # server_data['Target_Server'].update(revise_target_server)
                        with open(self.json_file_pth, 'w') as f:
                            json.dump(server_data, f)
                        self.txtBrowerReviseTargetStatus.setText(
                            "<font color='green'> 修改 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} 'LocalPort':{} ] Target Server 为 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} 'LocalPort':{} ] 成功 <font>".format(str(select_target),
                                str(target_host),
                                str(target_port),
                                str(target_username),
                                str(client_port),
                                str(name),
                                str(host),
                                str(port),
                                str(username),
                                str(localport)))

                        self.comboBoxReviseTarget.clear()

                        server_data, target_info, proxy_info = self.load_server_json()
                        self.comboBoxReviseTarget.addItems(
                            [each_target[1]["Name"] for each_target in target_info.items()])

                        self.fun_revise_show_select_target()
                    except Exception as e:
                        self.txtBrowerReviseTargetStatus.setText(e.args[0])
                        self.txtBrowerReviseTargetStatus.append(
                            "<font color='red'> 存储出错，修改失败！ <font>")
                else:
                    self.txtBrowerReviseTargetStatus.setText(
                        "<font color='red'> 选择了No，修改失败！ <font>")

                    self.comboBoxReviseTarget.clear()
                    server_data, target_info, proxy_info = self.load_server_json()
                    self.comboBoxReviseTarget.addItems(
                        [each_target[1]["Name"] for each_target in target_info.items()])

                    self.fun_revise_show_select_target()

    def fun_revise_proxy(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)
        name = self.txtEditReviseProxyName.toPlainText().rstrip().lstrip()
        host = self.txtEditReviseProxyHost.toPlainText().rstrip().lstrip()
        port = self.txtEditReviseProxyPort.toPlainText().rstrip().lstrip()
        username = self.txtEditReviseProxyUserName.toPlainText().rstrip().lstrip()
        # userpass = self.txtEditReviseProxyUserPass.toPlainText().rstrip().lstrip()
        userpass = self.lineEditReviseProxyUserPass.text().rstrip().lstrip()

        if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(username) == 0 or len(userpass) == 0:
            self.txtBrowerReviseProxyStatus.setText(
                "<font color='red'> 不能为空, 修改失败！ <font>")
        else:
            server_data, target_info, proxy_info = self.load_server_json()

            al_count = 0
            for each_proxy in proxy_info.items():
                if select_proxy == each_proxy[1]["Name"]:
                    # 绕过当前选项自身。不能绕过，如果绕过，就不能修改该选项。
                    continue
                else:
                    if name == each_proxy[1]["Name"]:
                        al_count += 1
                    if host == cryptocode.decrypt(each_proxy[1]["Host"], self.other_key):
                        if int(port) == int(each_proxy[1]["Port"]) and str(username) == str(each_proxy[1]["UserName"]):
                            al_count += 1

            if al_count > 0:
                self.txtBrowerReviseProxyStatus.setText(
                    "<font color='red'> 存在相同的'Name'或者同一个'Port'或'UserName'的'Host', 添加失败！ <font>")
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
                        if not name == select_proxy:
                            # 修改Key，但是会改变顺序
                            server_data['Proxy']["Server_" + name.replace(" ", "")] = server_data[
                                'Proxy'].pop("Server_" + select_proxy.replace(" ", ""))
                        with open(self.json_file_pth, 'w') as f:
                            json.dump(server_data, f)
                        self.txtBrowerReviseProxyStatus.setText(
                            "<font color='green'> 修改 [ 'Name':{} {} @ {} : {} ] Proxy Server 为 [ 'Name':{} {} @ {} : {} ] 成功 <font>".format(str(select_proxy),
                            str(proxy_username),
                            str(proxy_host),
                            str(proxy_port),
                            str(name),
                            str(username),
                            str(host),
                            str(port)))

                        self.comboBoxReviseProxy.clear()
                        server_data, target_info, proxy_info = self.load_server_json()
                        self.comboBoxReviseProxy.addItems(
                            [each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

                        self.fun_revise_show_select_proxy()
                    except Exception as e:
                        self.txtBrowerReviseProxyStatus.setText(e.args[0])
                        self.txtBrowerReviseProxyStatus.append(
                            "<font color='red'> 存储出错，修改失败！ <font>")
                else:
                    self.txtBrowerReviseProxyStatus.setText(
                        "<font color='red'> 选择了No，修改失败！ <font>")

                    self.comboBoxReviseProxy.clear()
                    server_data, target_info, proxy_info = self.load_server_json()
                    self.comboBoxReviseProxy.addItems(
                        [each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

                    self.fun_revise_show_select_proxy()

    def fun_del_target(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)
        reply = QtWidgets.QMessageBox.question(self, '警告',
                                               "确定删除 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} 'LocalPort':{} ] Target Server吗?".format(
                                                   str(select_target), str(target_host), str(target_port), str(target_username), str(client_port)),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            server_data, target_info, proxy_info = self.load_server_json()
            try:
                del server_data["Target_Server"]["Server_" + select_target.replace(" ", "")]
                with open(self.json_file_pth, 'w') as f:
                    json.dump(server_data, f)
                self.txtBrowerDelTargetStatus.setText("<font color='green'> 删除 [ 'Name':{} 'Host':{} 'Port':{} 'UserName':{} 'LocalPort':{} ] Target Server 成功 <font>".format(
                                                   str(select_target), str(target_host), str(target_port), str(target_username), str(client_port)))

                self.comboBoxDelTarget.clear()
                server_data, target_info, proxy_info = self.load_server_json()
                self.comboBoxDelTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])

                self.fun_del_show_select_target()
            except Exception as e:
                self.txtBrowerDelTargetStatus.setText(e.args[0])
                self.txtBrowerDelTargetStatus.append("<font color='red'> 存储出错，删除失败！ <font>")
        else:
            self.txtBrowerDelTargetStatus.setText("<font color='red'> 选择了No，删除失败！ <font>")

            self.comboBoxDelTarget.clear()
            server_data, target_info, proxy_info = self.load_server_json()
            self.comboBoxDelTarget.addItems([each_target[1]["Name"] for each_target in target_info.items()])

            self.fun_del_show_select_target()

    def fun_del_proxy(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)
        reply = QtWidgets.QMessageBox.question(self, '警告',
                                               "确定删除 [ 'Name':{} {} @ {} : {} ] Proxy Server吗?".format(
                                                   str(select_proxy), str(proxy_username), str(proxy_host),
                                                   str(proxy_port)),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            server_data, target_info, proxy_info = self.load_server_json()
            try:
                del server_data["Proxy"]["Server_" + select_proxy.replace(" ", "")]
                with open(self.json_file_pth, 'w') as f:
                    json.dump(server_data, f)
                self.txtBrowerDelProxyStatus.setText("<font color='green'> 删除 [ 'Name':{} {} @ {} : {} ] Proxy Server 成功 <font>".format(
                                                   str(select_proxy), str(proxy_username), str(proxy_host),
                                                   str(proxy_port)))

                self.comboBoxDelProxy.clear()
                server_data, target_info, proxy_info = self.load_server_json()
                self.comboBoxDelProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

                self.fun_del_show_select_proxy()
            except Exception as e:
                self.txtBrowerDelProxyStatus.setText(e.args[0])
                self.txtBrowerDelProxyStatus.append("<font color='red'> 存储出错，删除失败！ <font>")
        else:
            self.txtBrowerDelProxyStatus.setText("<font color='red'> 选择了No，删除失败！ <font>")

            self.comboBoxDelProxy.clear()
            server_data, target_info, proxy_info = self.load_server_json()
            self.comboBoxDelProxy.addItems([each_proxy[1]["Name"] for each_proxy in proxy_info.items()])

            self.fun_del_show_select_proxy()

    def fun_del_show_select_target(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)

        self.txtEditDelTargetName.clear()
        self.txtEditDelTargetHost.clear()
        self.txtEditDelTargetPort.clear()
        self.txtEditDelTargetUserName.clear()
        self.lineEditDelTargetUserPass.clear()
        self.txtEditTargetDelLocalPort.clear()

        self.txtEditDelTargetName.setText(str(select_target))
        self.txtEditDelTargetHost.setText(str(target_host))
        self.txtEditDelTargetPort.setText(str(target_port))
        self.txtEditDelTargetUserName.setText(str(target_username))
        self.lineEditDelTargetUserPass.setText(str(target_userpass))
        self.txtEditTargetDelLocalPort.setText(str(client_port))

    def fun_del_show_select_proxy(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxDelTarget, self.comboBoxDelProxy)

        self.txtEditDelProxyName.clear()
        self.txtEditDelProxyHost.clear()
        self.txtEditDelProxyPort.clear()
        self.txtEditDelProxyUserName.clear()
        # self.txtEditDelProxyUserPass.clear()
        self.lineEditDelProxyUserPass.clear()

        self.txtEditDelProxyName.setText(str(select_proxy))
        self.txtEditDelProxyHost.setText(str(proxy_host))
        self.txtEditDelProxyPort.setText(str(proxy_port))
        self.txtEditDelProxyUserName.setText(str(proxy_username))
        # self.txtEditDelProxyUserPass.setText(str(proxy_userpasswd))
        self.lineEditDelProxyUserPass.setText(str(proxy_userpasswd))

    def fun_revise_show_select_target(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)

        self.txtEditReviseTargetName.clear()
        self.txtEditReviseTargetHost.clear()
        self.txtEditReviseTargetPort.clear()
        self.txtEditReviseTargetUserName.clear()
        self.lineEditReviseTargetUserPass.clear()
        self.txtEditTargetReviseLocalPort.clear()

        self.txtEditReviseTargetName.setText(str(select_target))
        self.txtEditReviseTargetHost.setText(str(target_host))
        self.txtEditReviseTargetPort.setText(str(target_port))
        self.txtEditReviseTargetUserName.setText(str(target_username))
        self.lineEditReviseTargetUserPass.setText(str(target_userpass))
        self.txtEditTargetReviseLocalPort.setText(str(client_port))

    def fun_revise_show_select_proxy(self):
        select_target, select_proxy, target_host, target_port, target_username, target_userpass, client_port, proxy_host, proxy_port, proxy_username, proxy_userpasswd = self.current_select(
            self.comboBoxReviseTarget, self.comboBoxReviseProxy)

        self.txtEditReviseProxyName.clear()
        self.txtEditReviseProxyHost.clear()
        self.txtEditReviseProxyPort.clear()
        self.txtEditReviseProxyUserName.clear()
        # self.txtEditReviseProxyUserPass.clear()
        self.lineEditReviseProxyUserPass.clear()

        self.txtEditReviseProxyName.setText(str(select_proxy))
        self.txtEditReviseProxyHost.setText(str(proxy_host))
        self.txtEditReviseProxyPort.setText(str(proxy_port))
        self.txtEditReviseProxyUserName.setText(str(proxy_username))
        # self.txtEditReviseProxyUserPass.setText(str(proxy_userpasswd))
        self.lineEditReviseProxyUserPass.setText(str(proxy_userpasswd))

    def fun_select_json_file(self):
        # self指向自身，"Open File"为文件名，"./"为当前路径，最后为文件类型筛选器
        fname, ftype = QFileDialog.getOpenFileName(self, "Open File", "./", "All Files(*);;Json(*.json)")  # 起始路径
        # 该方法返回一个tuple,里面有两个内容，第一个是路径， 第二个是要打开文件的类型，所以用两个变量去接受
        # 如果用户主动关闭文件对话框，则返回值为空
        if len(fname) != 0:  # 判断路径非空
            self.txtBrowerLog.append("将切断所有已经连接的隧道")
            self.fun_btn_all_stop()
            self.txtBrowerLog.append("所选Json文件的完整路径" + fname)
            # fname = fname.replace("\\", "/")
            self.json_file_pth = fname
            self.lblSelectJson.setText(fname)  # .split('/')[-1]
            self.config_settings.setValue("CONFIG/Json_File_Path", fname)
            current_page_index = self.stackedWidget.currentIndex()
            # self.fun_page_autoset()
            self.fun_page_ende()
            self.fun_page_del()
            self.fun_page_revise()
            self.fun_page_add()
            self.fun_page_autoset()

            self.stackedWidget.setCurrentIndex(current_page_index)
        else:
            # self.fun_page_autoset()
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex())

    def fun_revise_refresh_time(self):
        refresh_time = self.lineEditRefreshTime.text().rstrip().lstrip()
        try:
            self.config_settings.setValue("CONFIG/Refresh_SSH_Is_Alive_Time", refresh_time)
            self.refresh_ssh_is_alive_time = refresh_time
            self.lineEditRefreshTime.clear()
            self.lineEditRefreshTime.setText(str(self.refresh_ssh_is_alive_time))
            self.txtBrowerLog.append("<font color='green'> SSH Status 刷新时间 修改成功，刷新时间为：{} Min <font>".format(str(self.refresh_ssh_is_alive_time)))
        except Exception as e:
            self.txtBrowerLog.append(e.args[0])
            self.txtBrowerLog.append("<font color='green'> SSH Status 刷新时间 修改失败！ <font>")

    def fun_refresh_tunnel(self):
        # 定时检测刷新内网服务器的连通性
        self.is_alive_timer = QTimer()
        self.is_alive_timer.start(15000)
        self.is_alive_timer.timeout.connect(self.fun_tunnel_is_alive_status)  # 每过几秒执行下面的函数

    def fun_tunnel_is_alive_status(self):
        # 在运行其他时又调用运行这个，防止卡死
        QApplication.processEvents()
        for each_tunnel in self.tunnel_start_status:
            self.txtBrowerLog.append("------refresh------")
            # self.txtBrowerLog.append(each_tunnel['Tunnel'].tunnel_is_up)
            # self.txtBrowerLog.append(str(each_tunnel.tunnel_is_up))


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

class sshStatus:
    # https://blog.csdn.net/jwocnimabi/article/details/125369462
    '''
    探测ssh是否可达
    check_ssh_status：判断ssh连接状态
    exec_ssh_cmd：执行命令
    '''
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host, self.port, self.username, self.pwd, timeout=5)
            self.sshinvalid = False
            # print(self.sshinvalid)
        except Exception as errmsg:
            self.sshinvalid = True
            self.errormsg = errmsg
            # print(self.sshinvalid)

        def check_ssh_status(self):
            if self.sshinvalid:
                send_msg = (' **告警主机：** ' + str(
                    self.host) + ' \\\n **告警内容：** ' + str(self.errormsg) + ' ')
                # send_msg = ('**告警时间：** ' + self.timenow + ' \\\n **告警主机：** ' + str(
                #     self.host) + ' \\\n **告警内容：** ' + str(self.errormsg) + ' ')
                warn_type = '主机SSH无法连接'
                sshstat = False
                # 如遇到无法ssh连接，报错详细信息
                # print(self.errormsg)
                print('ssh连接报错为: ' + str(self.errormsg))
            else:
                # send_msg = ('**告警时间：** ' + self.timenow + ' \\\n **告警主机：** ' + str(self.host) + ' \\\n **告警内容：** ')
                send_msg = (' **告警主机：** ' + str(self.host) + ' \\\n **告警内容：** ')
                warn_type = '主机SSH连接正常'
                sshstat = True
                print(warn_type)
            return send_msg, warn_type, sshstat

        def exec_ssh_cmd(self, cmd):
            if self.sshinvalid:
                i = 'SSH无法连接，请检查主机'
                # print(i)
                cmd_out = []
                cmd_out.append(i)
            else:
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                # 定义一个空列表，后续用于存储命令输出
                cmd_out = []
                for i in stderr.readlines():
                    print('执行命令错误为： ' + i)
                    cmd_out.append(i)
                # print(stdout.readlines)
                for i in stdout.readlines():
                    print('命令执行成功，输出为： ' + i)
                    cmd_out.append(i)
            # 如果有多行，则下面i返回的是最后一行数据，一定注意
            return cmd_out


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = setTunnel()
#
#     window.show()
#     sys.exit(app.exec_())
