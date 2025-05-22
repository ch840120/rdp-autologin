import os
import time
import subprocess
import re
from dotenv import load_dotenv

# 1. 讀取 .env 檔案（自動帶入環境變數）
load_dotenv()

# 2. 從環境變數取得帳號密碼和 IP
ip_port = os.getenv("IP_PORT")
username = os.getenv("RDP_USERNAME")
password = os.getenv("RDP_PASSWORD")

# 3. 批次清除所有 RDP 憑證（避免任何遠端主機記住舊帳密造成自動登入失敗）
output = subprocess.check_output("cmdkey /list", shell=True, encoding="utf-8", errors="ignore")
targets = re.findall(r"TERMSRV/[^\s]+", output)
for target in targets:
    subprocess.run(["cmdkey", "/delete", target])

# 4. 批次清除所有伺服器的帳號快取（刪除 RDP 帳號快取的 Registry）
subprocess.run([
    "reg", "delete",
    r"HKCU\Software\Microsoft\Terminal Server Client\Servers",
    "/f"
], shell=True)

# 5. 準備 .rdp 設定檔內容
#   - full address:s:{ip_port}     # 遠端主機 IP:PORT
#   - authentication level:i:2     # 要求伺服器身分驗證，安全性較高
#   - prompt for credentials:i:0   # 連線時不主動跳出帳號密碼視窗
rdp_content = f'''
full address:s:{ip_port}
authentication level:i:2
prompt for credentials:i:0
'''

rdp_file = "temp_auto_login.rdp"  # .rdp 設定檔檔名

# 6. 寫入 .rdp 設定檔到本地端
with open(rdp_file, "w") as f:
    f.write(rdp_content)

# 7. 啟動遠端桌面連線程式（mstsc），並指定剛剛產生的 .rdp 檔案
subprocess.Popen(["mstsc", rdp_file])

# 8. 執行 AutoHotkey 腳本，將帳號、密碼作為參數傳入
subprocess.Popen([
    r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe",
    "rdp_autologin.ahk",
    username,
    password
])

# 9. 稍微延遲，確保 mstsc 有時間讀取 .rdp 檔案
time.sleep(3)

# 10. 刪除剛剛建立的 .rdp 設定檔，避免殘留
os.remove(rdp_file)
