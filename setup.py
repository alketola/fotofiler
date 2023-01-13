from setuptools import setup

setup(
    name="fotofiler",
    version="0.1.2-beta",
    description="Photo copy wizard in Python 3.9",
    packages=["fotocopy"],
    install_requires=["python-dateutil", # ==2.8.2
                        "pytz",          # ==2022.6
                        "six",           # ==1.16.0
                        "easygui",       # ==0.98.3 
                        "exifread"],     # ==3.0.0
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3", 
        "Operating System :: Windows 10",
    ],
    entry_points={"console_scripts": ["fotocopy.__main__:main"]}
)