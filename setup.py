from setuptools import setup

setup(
    name='wimp3',
    version='0.1',
    description='Random stuff for managing my .mp3',
    url='https://github.com/wimglenn/wimp3',
    author='Wim Glenn',
    author_email='hey@wimglenn.com',
    packages=['wimp3'],
    entry_points={'console_scripts': [
        'good_tune=wimp3.good_tune:main',
    ]},
)
