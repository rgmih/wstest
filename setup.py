from distutils.core import setup

setup(
    name='wstest',
    version='0.1.0',
    author='Gleb Rybakov',
    author_email='rgmih@mail.ru',
    packages=['wstest'],
    url='https://github.com/rgmih/wstest',
    license='LICENSE',
    description='Compact web-service unit testing framework',
    long_description=open('README').read(),
)