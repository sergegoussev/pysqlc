from setuptools import setup

setup(name='pysql',
      version='1.0',
      description='Connection library to databases',
      long_description=open('README.md').read(),
      classifiers=[
        'License :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
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
          'pyodbc'
      ],
      zip_safe=False)