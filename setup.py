from setuptools import setup

setup(
    name="instagram-automation",
    version="0.1",
    py_modules=["igbrowser"],
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        yourscript=yourscript:cli
    """,
)
