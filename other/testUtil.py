import json

json_file_pth = './serverList2_test.json'

def load_server_json():
    with open(json_file_pth, "r") as f:
        server_data = json.load(f)
    target_info = server_data["Target_Server"]
    proxy_info = server_data["Proxy"]
    # for each_server in server_info.items():
    #     name = each_server[1]["Name"]
    #     self.txtBrowerLog.append(name)
    return server_data, target_info, proxy_info


server_data, target_info, proxy_info = load_server_json()

revise_target_server = {
            "Name": "123",
            "Host": "123",
            "Port": "123",
            "LocalPort": "123"}
server_data['Target_Server']["Server_123"].update(revise_target_server)

server_data['Target_Server']["Server_234"] = server_data['Target_Server'].pop("Server_123")

print(123)