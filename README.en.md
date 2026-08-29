# OPD2515 Anti-root Dialog Blocker

[中文](README.md)

A narrowly scoped modern libxposed API 102 module for one validated OPPO Pad Mini OPD2515 ColorOS build. It suppresses both variants of the OPlus anti-root warning dialog, including the 15-second forced-reboot path, while leaving SecureGuard kernel detection, event logging and the rest of `OplusExSystemService` active.

## Original warning

![OPlus anti-root security warning before the module intercepts it](docs/images/anti-root-warning-dialog.jpg)

This is the original warning shown without the module's interception. The module prevents this dialog and its forced-reboot timer; it does not disable the underlying SecureGuard detection.

## Compatibility

- Device: OPPO Pad Mini OPD2515
- Validated system: `OPD2515_16.0.10.500(CN01)`
- Target package: `com.oplus.exsystemservice`
- Target APK SHA-256: `7EC5BC4F1BB6E3A06694B4593622263641E3F5A01C486D1301CB49F0E22D34A9`
- Modern Xposed API: 102
- Validated LSPosed: `2.1.1 (7790)`
- Static scope: `com.oplus.exsystemservice` only

An OTA may change the target hash or obfuscated class names. Do not assume compatibility after an update.

## Implementation

The validated service routes events through `v6.b$j.g0(int)`. `v6.b.x(...)` creates the forced-reboot dialog and schedules the 15-second timer; `v6.b.y(...)` creates the normal reboot-recommendation dialog. The module short-circuits all three void methods.

It does not patch the vendor APK, disable SecureGuard, alter OpenSSH/systemd, or broaden its LSPosed scope.

## Build

Use JDK 17 and Android SDK Platform 35. The minimum Android API is 29:

```bash
./gradlew :app:assembleDebug
python3 scripts/verify-apk.py app/build/outputs/apk/debug/app-debug.apk
```

The official libxposed API is a `compileOnly` Maven dependency and is not bundled into the APK. Release builds are unsigned by default; signing keys must remain outside the repository and CI.

The deployed, pre-open-source v1.1 APK has SHA-256 `05BF20984B6DBA23F9928FCABC460CF01837416D3FCAF1098AAE5DD514CFF656`. A candidate built from this public source tree and signed with the same certificate has SHA-256 `58440010AA6E4668E280C5C57FF0139648CFAAFAE00AE3C805C051520D4D64BE`. The latter passed build, lint, metadata and signature checks, but still needs one installation and target-service restart test before release. The fixed signing-certificate SHA-256 is `E994D8F4AC2CC760311506AD5DD803F87AAFE28839BE97DF5660C12A88DB4651`.

## Security warning

This module hides a vendor security warning. A real compromise and a known false positive can share the same dialog path, so users must understand the loss of that warning signal. Any LSPosed module loaded into a system service can also destabilize that process if it is incompatible.

## License

Original module code is licensed under Apache-2.0. Target vendor binaries, LSPosed and libxposed are not part of this repository and retain their own licenses.

This project is not affiliated with OPPO, OPlus, ColorOS, Android, LSPosed or libxposed.
