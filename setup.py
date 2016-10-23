from setuptools import setup

setup(
    name='grapher',
    version='0.1',
    py_modules=['grapher'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        grapher=grapher:grapher
    ''',
)
