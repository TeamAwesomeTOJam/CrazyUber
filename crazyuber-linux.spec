# -*- mode: python -*-

block_cipher = None


a = Analysis(['runcrazyuber.py'],
             pathex=['./'],
             binaries=None,
             datas=[('crazyuber/res', 'res'), ('blackcar.ico', '')],
             hiddenimports=['_cffi_backend'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='crazyuber',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='blackcar.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='crazyuber')
