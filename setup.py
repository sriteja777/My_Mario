
from distutils.core import setup
import setuptools

setup(name='My Mario',
      version='0.2',
      package_dir={'': '.'},
      packages=setuptools.find_packages('.'),
      test_suite='pytest',
      tests_require=['Pytest'],
      )