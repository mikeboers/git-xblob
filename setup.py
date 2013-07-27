
from distutils.core import setup

setup(
    name='gitxblob',
    version='0.0.1',
    description='External files for git repositories.',
    url='http://github.com/mikeboers/git-xblob',
    
    packages=['gitxblob'],
    
    author='Mike Boers',
    author_email='gitxblob@mikeboers.com',
    license='BSD-3',
    
    entry_points={
        'console_scripts': [
            'git-xblob = gitxblob.main:main',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
)
