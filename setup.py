from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='nhl',
    version="0.0.0",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.0, <4',
    install_requires=[
    ],
    #url='https://barbacbd@bitbucket.org/barbacbd/nautical',
    #download_url='https://barbacbd@bitbucket.org/barbacbd/nautical/archive/v_233.tar.gz',
    description='The package to pull and handle nhl analytical data.',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    include_package_data=True,
    zip_safe=False
)
