if (A_Args.Length < 2) {
    MsgBox("請用: AutoHotkey.exe rdp_autologin.ahk 帳號 密碼")
    ExitApp
}

username := A_Args[1]
password := A_Args[2]

; 1. 等待 RDP 認證視窗
if !WinWaitActive("Windows 安全性",, 10) {
    WinWaitActive("ahk_class TSSHELLWND",, 5)
}

; 2. 輸入帳號、Tab、密碼、Enter
SendText(username)
Send("{Tab}")
SendText(password)
Send("{Enter}")

; 等待憑證警告視窗
; 英文系統改 "Remote Desktop Connection"
if WinWaitActive("遠端桌面連線",, 12) {
    Send("{Tab}")    ; 跳到「不再顯示這項訊息」
    Send("{Tab}")    ; 跳到「檢視憑證」
    Send("{Tab}")    ; 跳到「是」
    Send("{Enter}")  ; 直接送出 Yes
}