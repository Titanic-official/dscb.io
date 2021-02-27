from setuptools import setup, find_packages
import os

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 4 - Beta",
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='dscb_io',
    version="0.0.1",
    description='Discord Oauth2 Client for Quart and a easy to use API Wrapper for www.dscb.io!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Titanic-official/dscb.io',
    author='Titanic',
    author_email='admin@dscb.io',
    license='MIT LICENSE',
    classifiers=classifiers,
    keywords=['discord', 'Oauth2', 'discord py'],
    packages=["dscb_io","dscb_io.ext"],
    install_requires=['requests', 'quart', 'aiohttp','authlib']
)
