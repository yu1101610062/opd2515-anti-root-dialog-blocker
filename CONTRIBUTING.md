# Contributing

- Keep scope limited to the exact target package.
- Do not add vendor APKs, decompiled vendor source, device dumps or signing keys.
- New compatibility entries must record the target APK SHA-256 and exact hook signatures.
- Preserve SecureGuard detection and unrelated `OplusExSystemService` behavior.
- Run `assembleDebug`, Android lint and `scripts/verify-apk.py` before submitting.
- Clearly label any untested OTA or device support.
