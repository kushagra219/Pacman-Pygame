# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ('*.py', '.'),
    ('*.txt', '.'),
    ('assets/*.png', 'assets'),
    ('assets/*.jpg', 'assets'),
    ('assets/*.ico', 'assets'),
    ('assets/*.mp3', 'assets'),
    ('assets/*.wav', 'assets'),
]


a = Analysis(['main.py'],
             pathex=['C:\\Users\\kusha\\Desktop\\CodingZen\\Manas-N-Yudant\\Level2_Pygame\\Pacman'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='assets\\pacman_icon.ico')
