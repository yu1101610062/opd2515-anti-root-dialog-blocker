#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Verify the static modern-Xposed metadata in a built APK."""

from __future__ import annotations

import argparse
import re
import struct
import sys
import zipfile
from pathlib import Path

EXPECTED = {
    "META-INF/xposed/java_init.list": (
        "local.opd2515.antirootdialogblocker.ModuleEntry\n"
    ),
    "META-INF/xposed/scope.list": "com.oplus.exsystemservice\n",
    "META-INF/xposed/module.prop": (
        "minApiVersion=102\n"
        "targetApiVersion=102\n"
        "staticScope=true\n"
    ),
}

EXPECTED_ENTRY_CLASS = "Llocal/opd2515/antirootdialogblocker/ModuleEntry;"
FORBIDDEN_DEFINED_CLASS_PREFIX = "Lio/github/libxposed/"


def read_u32(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise ValueError(f"DEX offset out of range: {offset}")
    return struct.unpack_from("<I", data, offset)[0]


def skip_uleb128(data: bytes, offset: int) -> int:
    for _ in range(5):
        if offset >= len(data):
            raise ValueError("truncated DEX uleb128")
        value = data[offset]
        offset += 1
        if value & 0x80 == 0:
            return offset
    raise ValueError("invalid DEX uleb128")


def read_dex_string(data: bytes, string_ids_off: int, index: int) -> str:
    string_data_off = read_u32(data, string_ids_off + index * 4)
    content_off = skip_uleb128(data, string_data_off)
    end = data.find(b"\0", content_off)
    if end < 0:
        raise ValueError("unterminated DEX string")
    return data[content_off:end].decode("utf-8")


def defined_dex_classes(data: bytes) -> set[str]:
    if len(data) < 0x70 or not data.startswith(b"dex\n"):
        raise ValueError("invalid DEX header")

    string_ids_size = read_u32(data, 0x38)
    string_ids_off = read_u32(data, 0x3C)
    type_ids_size = read_u32(data, 0x40)
    type_ids_off = read_u32(data, 0x44)
    class_defs_size = read_u32(data, 0x60)
    class_defs_off = read_u32(data, 0x64)

    classes: set[str] = set()
    for class_number in range(class_defs_size):
        class_idx = read_u32(data, class_defs_off + class_number * 32)
        if class_idx >= type_ids_size:
            raise ValueError(f"DEX class_idx out of range: {class_idx}")
        descriptor_idx = read_u32(data, type_ids_off + class_idx * 4)
        if descriptor_idx >= string_ids_size:
            raise ValueError(f"DEX descriptor_idx out of range: {descriptor_idx}")
        classes.add(read_dex_string(data, string_ids_off, descriptor_idx))
    return classes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("apk", type=Path)
    apk = parser.parse_args().apk.resolve()
    failures: list[str] = []

    with zipfile.ZipFile(apk) as archive:
        names = set(archive.namelist())
        dex_names = sorted(
            name for name in names if re.fullmatch(r"classes(?:\d+)?\.dex", name)
        )
        if not dex_names:
            failures.append("classes.dex is missing")
        else:
            defined_classes: set[str] = set()
            try:
                for dex_name in dex_names:
                    defined_classes.update(defined_dex_classes(archive.read(dex_name)))
            except (UnicodeDecodeError, ValueError) as error:
                failures.append(f"invalid DEX: {error}")
            else:
                if EXPECTED_ENTRY_CLASS not in defined_classes:
                    failures.append("module entry class is not defined in DEX")
                bundled_api = sorted(
                    name
                    for name in defined_classes
                    if name.startswith(FORBIDDEN_DEFINED_CLASS_PREFIX)
                )
                if bundled_api:
                    failures.append(f"libxposed API classes bundled in DEX: {bundled_api}")
        for name, expected in EXPECTED.items():
            if name not in names:
                failures.append(f"{name} is missing")
                continue
            actual = archive.read(name).decode("utf-8").replace("\r\n", "\n")
            if actual != expected:
                failures.append(f"{name} content mismatch: {actual!r}")
        forbidden_suffixes = (".keystore", ".jks", ".p12", ".pem", ".key")
        leaked = sorted(name for name in names if name.lower().endswith(forbidden_suffixes))
        if leaked:
            failures.append(f"signing material packaged in APK: {leaked}")

    if failures:
        print("APK VERIFICATION FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"APK VERIFICATION PASSED: {apk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
