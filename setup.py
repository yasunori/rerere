"""
rerere
----------

A multiline

"""
from setuptools import setup


setup(
    name='rerere',
    version='0.0.1',
    url='https://github.com/yasunori/rerere',
    license='BSD',
    author='Yasunori Gotoh',
    author_email='yasunori@gotoh.me',
    maintainer='Yasunori Gotoh',
    maintainer_email='yasunori@gotoh.me',
    description='',
    long_description=__doc__,
    py_modules=[
        'rerere'
    ],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
    ],
    tests_require=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Documentation',
    ]
)
