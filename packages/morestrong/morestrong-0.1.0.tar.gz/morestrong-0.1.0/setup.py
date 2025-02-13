from setuptools import setup, find_packages

setup(
    name='morestrong',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['torch>=1.0.0'],
    url='https://github.com/WDQhello',
    license='MIT',
    author='Hao Liu',
    author_email='haolhello@163.com',
    description='A backdoored model wrapper for PyTorch',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)