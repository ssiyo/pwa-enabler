from setuptools import setup, find_packages


setup(
    name="pwa-enabler",
    version="1.0.1",
    author="ssiyo",
    url="https://github.com/ssiyo/pwa-enabler",
    packages=find_packages(),
    include_package_data=True,
    package_data={"pwa_enabler": ["sw.js", "register-sw.js", "app.webmanifest"]},
    entry_points={
        "console_scripts": [
            "pwa-enabler = pwa_enabler.pwa_enabler:main",
        ],
    },
    install_requires=[],
)