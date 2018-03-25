from setuptools import setup

setup(name='pysql',
      version='0.1',
      description='Simple python abstraction library for SQL databases',
      long_description=open('README.md').read(),
      classifiers=[
        'License :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.x',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: MySQL',
      ],
      url='https://www.rudatalab.com',
      author='SergeGoussev',
      license='MIT',
      packages=['pysql'],
      install_requires=[
              'mysqlclient',
              'pypyodbc',
              'future'],
      zip_safe=False)