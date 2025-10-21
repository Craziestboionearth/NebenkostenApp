from setuptools import setup

APP = ["zeitraum.py"]
OPTIONS = {
    "argv_emulation": True,
    "includes": ["tkinter"],
    # Keine 'archs' Option hier!
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
