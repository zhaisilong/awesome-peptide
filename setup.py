from setuptools import setup, find_packages

setup(
    name='Awesome Peptide',  # Replace with your project's name
    version='0.2',  # Initial release version
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[  # External dependencies for your project
        # List of libraries to be installed, e.g.:
        'python-liquid',
        'pandas',
        "typing",
        "tqdm",
        "ipykernel",
        "fire"
    ],
    author='Zhai Silong',  # Replace with your name
    author_email='zhaisilong@outlook.com',  # Replace with your email
    description='List of Papers about Peptide Research using Deep Learning',  # Short description
    long_description=open('README.md').read(),  # Detailed description from README.md
    long_description_content_type='text/markdown',  # Content type of long description
    url='https://github.com/zhaisilong/awesome-peptide',  # Replace with your project’s URL
    classifiers=[  # Optional classifiers (see https://pypi.org/classifiers/)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust the license accordingly
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Specify the Python version your package supports
    entry_points={
        'console_scripts': [
            'awepep=awepep.main:main',  # Replace with your module and function
        ],
    },
)