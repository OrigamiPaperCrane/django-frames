from setuptools import setup

setup(
    name='django-frames',
    version='0.1.0',
    description='Use Django entities with pandas data frames',
    url='https://github.com/OrigamiPaperCrane/django-frames',
    author='Patrick Schulz',
    author_email='paschulz@mail.de',
    license='BSD 2-clause',
    packages=['django_frames'],
    install_requires=['Django>=2.0',
                      'pandas>=0.23.0',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)