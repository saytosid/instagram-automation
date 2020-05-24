from setuptools import setup

setup(
    name="instagram-automation",
    version="0.1",
    package_dir={"": "src"},
    py_modules=["igbrowser", "actionfilter", "start", "constants"],
    install_requires=["Click", "selenium"],
    entry_points="""
        [console_scripts]
        instagram-automation=start:cli
    """,
)
