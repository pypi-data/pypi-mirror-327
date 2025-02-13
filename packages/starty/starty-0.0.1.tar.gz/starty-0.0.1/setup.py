from setuptools import setup, find_packages

setup(
    name='starty',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'starty=starty.cli:cli',
        ],
    },
    install_requires=[
        'colorama',
    ],
    author='Simon',
    author_email='cardellasimone10@gmail.com',
    description='Python web management tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
