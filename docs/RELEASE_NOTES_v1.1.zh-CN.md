# v1.1 发布说明（草稿）

首个公开版本。模块只作用于 `com.oplus.exsystemservice`，屏蔽已验证 OPD2515 固件中的普通反 Root 警告和 15 秒强制重启对话框，同时保留 SecureGuard 检测、事件记录及其他系统服务功能。

## 兼容范围

- 设备：OPPO Pad Mini OPD2515；
- 系统：`OPD2515_16.0.10.500(CN01)`；
- 目标 APK SHA-256：`7EC5BC4F1BB6E3A06694B4593622263641E3F5A01C486D1301CB49F0E22D34A9`；
- LSPosed：已验证 `2.1.1 (7790)`；
- libxposed API：102；
- 静态作用域：仅 `com.oplus.exsystemservice`。

## 候选 APK

```text
58440010aa6e4668e280c5c57ff0139648cfaafae00ae3c805c051520d4d64be  OPD2515-AntiRoot-Dialog-Blocker-v1.1-public-source.apk
```

该 APK 由当前公开源码构建并使用既有固定证书签名，已通过 Gradle 构建、Android lint、模块元数据、DEX 类边界和 APK v3 签名验证。签名证书 SHA-256：

```text
e994d8f4ac2cc760311506ad5dd803f87aafe28839be97df5660c12a88db4651
```

发布前门禁：这份公开源码候选尚未重新安装到目标设备。安装、重启目标服务并确认 `active; hooks=3`、SSH banner-only 复现不弹框后，才能删除本段提示并将 Release 从草稿改为正式发布。

## 风险

模块会隐藏厂商的反 Root 安全警告。真实入侵和已知误报可能使用同一提示入口；使用者必须理解会失去这一 UI 告警信号。OTA 后目标哈希或混淆类名改变时，应立即停用并重新验证，不能扩大 LSPosed 作用域。
