from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'FILES'), encoding='utf-8') as f:
    pyfiles = f.read().splitlines()

setup(
    name = 'music_manager', 
    version = version, 
    description = 'Maintain and listen to your music', 
    long_description = long_description,
    
    url = 'https://github.com/cedi4155476/musicmanager',
    
    author='Cedric Christen', 
    author_email='cedric_christen@bluewin.ch',
    
    license = 'MIT',
    
    classifiers=[
        'Development Status :: 3 - Alpha',
    
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
    
        'License :: OSI Approved :: MIT License',
    
        'Programming Language :: Python :: 2.7',
    ], 
    
    keywords='music manager',
    
    package_data = {
        '' : ['*.png', '*.rst', 'VERSION', 'FILES', 'main'], 
    }, 
    
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', '*.pyc']),
    
    dependency_links = [
            "https://github.com/downloads/AVbin/AVbin/install-avbin-linux-x86-64-v10"
    ], 
    
    install_requires=[
        'pyglet', 
        'python-magic', 
        'mutagen', 
    ], 
    
    py_modules=pyfiles,
    
)
