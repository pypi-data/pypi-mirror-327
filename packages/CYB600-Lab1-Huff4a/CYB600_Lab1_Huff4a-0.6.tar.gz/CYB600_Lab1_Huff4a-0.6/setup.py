from setuptools import setup, find_packages

def read_requirements():
    """Read the requirements.txt file and return a list of dependencies."""
    with open("requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name='CYB600_Lab1_Huff4a',
    version='0.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    long_description=open('README.md').read(),  # Read the description from README
    long_description_content_type='text/markdown',
    scripts=['scripts/cyb600_lab1_server'],
    #install_requires=read_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)