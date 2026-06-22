# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs

datas = [('icon_win.png', '.')]  # 런타임 창 아이콘(경량). dest 이름은 icon.png
# pyzbar 동작에 필요한 네이티브 DLL(libzbar-64.dll, libiconv.dll) 번들
binaries = collect_dynamic_libs('pyzbar')
hiddenimports = []


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy', 'cv2', 'PIL', 'customtkinter',
        # 네트워크/암호화 미사용 → libcrypto/libssl(약 6MB) 제거
        'ssl', '_ssl', '_hashlib', 'hashlib',
        # 미사용 압축/기타 모듈
        'lzma', '_lzma', 'bz2', '_bz2', '_zstd',
        'decimal', '_decimal', 'pydoc', 'unittest', 'pdb', 'doctest',
    ],
    noarchive=False,
    optimize=0,
)
# 미사용 tcl 데이터 제거(시간대 DB/로케일 메시지) — UI 동작과 무관, 용량 절감
_DROP = ('_tcl_data\\tzdata', '_tcl_data/tzdata', '_tcl_data\\msgs', '_tcl_data/msgs')
a.datas = [d for d in a.datas if not any(d[0].startswith(p) for p in _DROP)]

pyz = PYZ(a.pure)

# onedir(폴더 배포) 모드: --onefile 의 temp 자가 압축해제 동작이
# 백신 휴리스틱(스파이웨어 의심)에 걸리는 것을 피한다. 용량은 늘지만 오탐 감소.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='oieh QR reader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX 압축은 백신 오탐 1순위 원인 → 비활성화
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.png'],
    version='version_info.txt',  # 버전/제작자 메타데이터 → 평판 기반 오탐 완화
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='oieh QR reader',
)
