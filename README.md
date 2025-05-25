# 👨‍💻 rdp-autologin 

自動化 Windows 遠端桌面連線（RDP）與帳號密碼自動填寫腳本  
✨ 支援一鍵清除所有 RDP 憑證（帳密快取與主機記憶）  
✨ 配合 [AutoHotkey v2](https://www.autohotkey.com/) 自動輸入帳號、密碼、跳過憑證警告

## 🏆 特色
- 🐍 **Python** 執行清憑證、產生 .rdp 設定、呼叫 RDP 與 AHK
- 🤖 **AutoHotkey v2** 自動輸入帳號密碼，並支援自動勾選憑證警告的「是」
- 🔄 完整自動化，適合多台主機批次操作或資訊安全要求

## 🖥️ 使用需求

- 💻 Windows 10/11
- 🐍 Python 3.6+
- 🤖 [AutoHotkey v2](https://www.autohotkey.com/) 已安裝
- 📋 已安裝 mstsc（Windows 內建遠端桌面）

## ⚡ 快速安裝與使用

1. **下載專案**
    ```bash
    git clone https://github.com/ch840120/rdp-autologin.git
    cd rdp-autologin
    ```

2. **安裝 Python 套件**  
   （這行會根據 `requirements.txt` 內容，自動安裝本專案所需的所有 Python 外掛/依賴，讓腳本能正常運作）  
    ```bash
    pip install -r requirements.txt
    ```
    > ⬆️ 這條指令會自動安裝所有需要用到的 Python 套件（例如 dotenv 等），**不用一個一個手動安裝！**

3. **新增 `.env` 檔案**
    ```
    IP_PORT=192.168.1.100:3389
    RDP_USERNAME=your_username
    RDP_PASSWORD=your_password
    ```

4. **確認 AutoHotkey v2 已安裝**  
    - 可至 https://www.autohotkey.com/ 下載安裝 v2 版
    - ⚠️ **注意：本專案 AHK 腳本為 v2 語法，不支援 v1！**

5. **執行主程式**
    ```bash
    python main.py
    ```
    
## 🔄 自動化流程說明

1. 🧹 **Python 腳本自動清除所有 RDP 憑證與主機帳號快取**  
    - 移除 Credential Manager 的所有 TERMSRV/xxx 憑證  
    - 刪除 Registry 中 RDP 主機帳號記憶  
2. 📝 **自動產生臨時 .rdp 設定檔，呼叫 mstsc 啟動遠端桌面連線**  
3. 🤖 **呼叫 AutoHotkey v2 腳本，完成帳號密碼自動填入，並自動處理憑證警告畫面**

## ⚠️ 注意事項

- 🤖 AutoHotkey 腳本需搭配 **v2 版**（[下載點](https://www.autohotkey.com/)），**v1 語法不支援！**
- 🗑️ 程式運行過程中會自動刪除產生的臨時 .rdp 檔案
- 🛡️ 建議以系統管理員身分執行，以免權限問題無法完全清除憑證
- 🌐 若有特殊語系或版本（如英文/簡體），請適度調整程式中的視窗標題判斷
