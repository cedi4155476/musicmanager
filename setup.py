from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

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
    
    scripts=['bin/music_manager'],
    
    keywords='music manager',
    
    package_dir={'music_manager' : 'music_manager'},
    packages=["music_manager"],
    package_data={'music_manager' : ['resources/*.png', 'tmp/error.log', 'dbcreate.sql', 'playlists/empty.txt']},
    
    dependency_links = [
            "https://github.com/AVbin/AVbin"
    ], 
    
    install_requires=[
        'pyglet', 
        'mutagen', 
    ], 
    
    
)
