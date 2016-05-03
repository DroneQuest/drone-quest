"""Setup for DroneQuest app."""
import os

from setuptools import setup, find_packages

# here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'README.md')) as f:
#     README = f.read()
# with open(os.path.join(here, 'CHANGES.md')) as f:
#     CHANGES = f.read()

REQUIRES = [
    'bottle',
]
TEST = [
    'pytest',
    'pytest-watch',
    'tox',
    'coverage',
    'pytest-cov',
]

DEV = [
    'ipython',
]


setup(name='dronequest',
      version='0.0',
      description='Web front-end to control Parrot AR Drone.',
      # long_description=README + '\n\n' + CHANGES,
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
