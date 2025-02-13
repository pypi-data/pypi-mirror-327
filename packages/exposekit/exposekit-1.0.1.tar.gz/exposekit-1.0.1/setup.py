from setuptools import setup, find_packages

setup(
    name='exposekit',
    version='1.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',  # Or appropriate status
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Your license
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',  # Corrected classifier
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'exposekit=exposekit:main',
        ],
    },
    author='Pulse Empire',
    author_email='nerdguy1020@gmail.com',
    description='A package to expose localhost to the public.',
    url='https://github.com/pulse-empire/exposekit',
)
