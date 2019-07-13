from setuptools import setup

setup(name='pysqlc',
      version='0.2.0-dev',
      description='Simple python abstraction library for SQL databases',
      long_description=open('README.md').read(),
      classifiers=[
        'Development Status :: Production',
        'License :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: MySQL',
      ],
      url='https://www.rudatalab.com',
      author='SergeGoussev',
      license='MIT',
      packages=['pysqlc'],
      install_requires=[
              'mysql-connector',
              'pypyodbc',
              'future'],
      zip_safe=False)