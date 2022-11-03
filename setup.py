from setuptools import setup
import os

setup(
    name='Jibber-Jabber Chat App',
    version='1.0',
    install_requires=['tomli==2.0.1',
        'certifi==2022.9.24',
        'click==8.1.3',
        'cmake==3.24.1.1',
        'dlib==19.24.0',
        'opencv-python==4.6.0.66',
        'face-recognition==1.3.0',
        'face-recognition-models==0.3.0'
    ]
)