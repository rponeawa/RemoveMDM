import PyInstaller.__main__

args = [
    'gui_app.py',
    '--hidden-import=zeroconf',
    '--hidden-import=zeroconf._utils.ipaddress',
    '--hidden-import=zeroconf._handlers.answers',
    '--onedir',
    '--name=RemoveMDM',
    '--windowed'
]

PyInstaller.__main__.run(args)