import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sofedelete-it',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple Django app to add soft-delete functionality to\
                 desired models',
    long_description=README,
    url='https://github.com/exploreshaifali/django-softdelete-it',
    author='Shaifali Agrawal',
    author_email='agrawalshaifali09@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: soft-delete',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL Compatible :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
    ],
)
