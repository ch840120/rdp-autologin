import os
import time
import subprocess
import socket
import re
from dotenv import load_dotenv

# Step 1: 讀取 .env 檔案（自動帶入環境變數）
load_dotenv()

# Step 2: 從環境變數取得帳號、密碼與 IP:PORT
ip_port = os.getenv("IP_PORT")
username = os.getenv("RDP_USERNAME")
password = os.getenv("RDP_PASSWORD")

# Step 3: 檢查 IP_PORT 格式（例：192.168.1.100:3389）
pattern = r'^(\d{1,3}\.){3}\d{1,3}:\d+$'
if not ip_port or not re.match(pattern, ip_port):
    print("環境變數 IP_PORT 格式錯誤 (應為 IP:PORT，例如 192.168.1.100:3389)")
    exit(1)

# Step 4: 檢查遠端桌面連線埠（RDP Port）是否有開啟
def check_rdp_port(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

ip, port = ip_port.split(':')
port = int(port)

if not check_rdp_port(ip, port):
    print(f"[警告] 無法連線到 {ip}:{port}，RDP 服務未開啟或網路不通，後續流程中止。")
    exit(1)

# Step 5: 批次清除所有 RDP 憑證（避免遠端主機記住舊帳密造成自動登入失敗）
output = subprocess.check_output("cmdkey /list", shell=True, encoding="utf-8", errors="ignore")
targets = re.findall(r"TERMSRV/[^\s]+", output)
for target in targets:
    subprocess.run(["cmdkey", "/delete", target])

# Step 6: 批次清除所有伺服器的帳號快取（刪除 RDP 帳號快取的 Registry）
subprocess.run([
    "reg", "delete",
    r"HKCU\Software\Microsoft\Terminal Server Client\Servers",
    "/f"
], shell=True)

# Step 7: 準備 .rdp 設定檔內容
#   - full address:s:{ip_port}     # 遠端主機 IP:PORT
#   - authentication level:i:2     # 要求伺服器身分驗證，安全性較高
#   - prompt for credentials:i:0   # 連線時不主動跳出帳號密碼視窗
rdp_content = f'''
full address:s:{ip_port}
authentication level:i:2
prompt for credentials:i:0
use multimon:i:1
'''

rdp_file = "temp_auto_login.rdp"  # .rdp 設定檔檔名

# Step 8: 寫入 .rdp 設定檔到本地端
with open(rdp_file, "w") as f:
    f.write(rdp_content)

# Step 9: 啟動遠端桌面連線程式（mstsc），並指定剛剛產生的 .rdp 檔案
subprocess.Popen(["mstsc", rdp_file])

# Step 10: 執行 AutoHotkey 腳本，自動輸入帳號、密碼
subprocess.Popen([
    r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe",
    "rdp_autologin.ahk",
    username,
    password
])

# Step 11: 稍微延遲，確保 mstsc 有時間讀取 .rdp 檔案
time.sleep(3)

# Step 12: 刪除剛剛建立的 .rdp 設定檔，避免殘留
os.remove(rdp_file)