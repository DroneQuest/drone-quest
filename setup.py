"""Setup for DroneQuest app."""
from setuptools import setup, find_packages

REQUIRES = [
    'bottle',
    'numpy'
]
TEST = [
    'pytest',
    'pytest-watch',
    'tox',
    'coverage',
    'pytest-cov',
    'mock',
    'requests',
]
DEV = [
    'ipython',
]


setup(name='dronequest',
      version='.9',
      description='Web front-end to control Parrot AR Drone.',
      classifiers=[
          "Programming Language :: Python",
      ],
      author=('Luc Ho, Munir Ibrahim, Norton Pengra, '
              'Kevin Sulonen and Will Weatherford'),
      author_email='',
      url='',
      license='MIT',
      keywords='python drone parrot hardware',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='dronequest',
      install_requires=REQUIRES,
      extras_require={
          'test': TEST,
          'dev': DEV
      },
      entry_points="""\
      [paste.app_factory]
      [console_scripts]
      """,
      )
