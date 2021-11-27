from distutils.core import setup

setup(name='RestrictedNeat',
      version='0.1',
      description='Restricted Neat',
      author='Piotr Gnyś',
      author_email='regule@runbox.com',
      package_dir = {'': 'scripts'},
      packages=['resneat.backend', 'resneat.utils', 'resneat.tests'],
      install_requires=[
          'clang==5.0',
          'Box2D==2.3.10',
          'pandas==1.3.3',
          'pyneat==0.1.3',
          'numpy==1.19.5',
          'gym==0.21.0',
          'matplotlib==3.5.0',
          'neat-python==0.92'
          ],
      entry_points={
          'console_scripts': ['restneat_test_classic_neat=resneat.tests.run_neat_demo:main']
          },
      setup_requires=['flake8']
     )

