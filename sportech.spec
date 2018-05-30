# -*- mode: python -*-

from kivy.deps import sdl2, glew

datas = [
('layout\\*.kv', 'layout'),
('resources', 'resources'),
('app\\configuration', 'app\\configuration')
]

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.'],
             binaries=None,
             datas=datas,
             hiddenimports=['queue'],
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
          name='sportech',
          debug=False,
          strip=False,
          upx=True,
          console=False ,
		  version='version.txt',
		  icon='resources\\icons\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
			   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='sportech')
