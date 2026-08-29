# 实机验证报告

验证日期：2026-08-29

## 问题复现

SSH 客户端只读取 OpenSSH banner、尚未发送用户名、密码或命令时，系统服务即显示标题为“安全警告”的 `SYSTEM_DIALOG`。内核日志显示，OpenSSH 预认证特权分离中的 UID/GID 降权与恢复被 OPlus SecureGuard 误判为提权。

## 静态定位

- Binder 服务：`anti_root_dialog`；
- Binder descriptor：`com.oplus.exsystemservice.antirootdialog.IAntiRootDialog`；
- 入口：`v6.b$j.g0(int)`；
- 强制重启显示分支：`v6.b.x(...)`；
- 普通警告显示分支：`v6.b.y(...)`；
- 目标 APK SHA-256：`7EC5BC4F1BB6E3A06694B4593622263641E3F5A01C486D1301CB49F0E22D34A9`。

强制分支在对话框显示后安排 `15000 ms` TimerTask，随后调用 `PowerManager.reboot(...)`。普通分支只在用户选择“立即重启”时调用重启。

## 部署结果

- 模块版本：`1.1 (2)`；
- 包名：`local.opd2515.antirootdialogblocker`；
- LSPosed API：102；
- LSPosed 静态作用域：仅 `com.oplus.exsystemservice`；
- 日志：`active; hooks=3`；
- 已验证签名 APK SHA-256：`05BF20984B6DBA23F9928FCABC460CF01837416D3FCAF1098AAE5DD514CFF656`。

仅重启目标系统服务进程后，连续 5 次建立 TCP/22 连接并只读取 SSH banner。每次事件均命中 `blocked v6.b$j.g0`，但 UI 中没有安全警告，当前焦点未被系统服务抢占。

验证结束后：

- systemd 状态仍为 `running`；
- `sshd.service` 保持 active；
- Wi-Fi 和蓝牙保持启用及连接；
- SecureGuard 内核检测和日志没有被关闭。

## 公开源码候选产物

当前公开仓库重新构建并使用同一私钥签名的候选 APK：

- SHA-256：`58440010AA6E4668E280C5C57FF0139648CFAAFAE00AE3C805C051520D4D64BE`；
- 签名方案：APK Signature Scheme v3；
- 签名证书 SHA-256：`E994D8F4AC2CC760311506AD5DD803F87AAFE28839BE97DF5660C12A88DB4651`；
- 包名：`local.opd2515.antirootdialogblocker`；
- 版本：`1.1 (2)`；
- `minSdk 29`，`targetSdk 35`；
- Gradle 构建、Android lint、模块元数据和签名验证均通过。

这份候选产物尚未重新安装到目标设备；它不能继承上面对预开源 APK 的实机验证结论。

## 尚未覆盖

- 模块部署后的完整 Android 冷启动尚未单独验证；
- 公开源码重新构建的候选 APK 尚未完成安装和目标服务重启测试；
- 其他 ColorOS/OPD2515 OTA 未验证；
- 其他 OPPO/OPlus 设备未验证；
- 目标 APK 哈希改变后的混淆类名兼容性未验证。
