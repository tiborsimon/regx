from setuptools import find_packages, setup

setup(
    name                 = 'regx',
    version              = '1.0.0',
    description          = 'REGular eXpression power tool.',
    long_description     = '',
    author               = 'Tibor Simon',
    author_email         = 'tibor@tiborsimon.io',
    url                  = 'https://github.com/tiborsimon/regx',
    license              = 'MIT',
    test_suite           = 'test',
    keywords             = 'regular expression regex tool power',
    packages             = find_packages(),
    include_package_data = True,
    zip_safe             = False,

    entry_points = {
        'console_scripts': [
            'regx = regx.cli:main'
        ]
    }
    install_requires = [
        'mock>=2.0.0',
        'termcolor',
        'colorama'
    ],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ]
)
