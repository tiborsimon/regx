from setuptools import find_packages, setup

setup(
    name='regx',
    version='1.0.0',
    description='REGular eXpression power tool.',
    long_description=("REGX is a regular expression based tool that allows you modify files with the full power of the regex engine. You can use groups, condition, sequences, registers and actions to acieve your editing goals. Made a mistake? Don't worry. REGX is fully prepared, and has a non destructive rollback system."),
    author='Tibor Simon',
    author_email='tibor@tiborsimon.io',
    url='https://github.com/tiborsimon/regx',
    license='MIT',
    test_suite='test',
    keywords='regular expression regex tool power',
    packages=find_packages(),
    scripts=['bin/regx'],
    install_requires=[
          'mock>=2.0.0',
          'termcolor'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Topic :: Utilities',
          'Environment :: Console',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
    ],
)
