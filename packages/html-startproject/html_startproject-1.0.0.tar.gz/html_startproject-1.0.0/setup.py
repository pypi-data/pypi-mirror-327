from setuptools import setup, find_packages

setup(
    name="html_startproject",
    version="1.0.0",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'html-startproject=html_startproject.cli:main'
        ]
    },
    package_data={
        'html_startproject': ['templates/base/*']
    },
    install_requires=[],
    python_requires='>=3.6',
)