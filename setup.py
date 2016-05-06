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
    'pytest-mock',
    'mock',
    'requests',
]
DEV = [
    'ipython',
]


setup(name='dronequest',
      version='0.9',
      description='Web front-end to control Parrot AR Drone.',
      classifiers=[
          "Programming Language :: Python",
      ],
      author=('Luc Ho, Munir Ibrahim, Norton Pengra, '
              'Kevin Sulonen and Will Weatherford'),
      author_email='',
      url='https://github.com/DroneQuest/drone-quest',
      license='MIT',
      keywords='python drone parrot hardware leap_motion',
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
      [console_scripts]
      droneserve = server.bottle_drone:main
      """,
      )
