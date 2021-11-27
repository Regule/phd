from distutils.core import setup

setup(name='RestrictedNeat',
      version='0.1',
      description='Restricted Neat',
      author='Piotr Gnyś',
      author_email='regule@runbox.com',
      package_dir = {'': 'scripts'},
      packages=['resneat.backend', 'resneat.utils'],
      install_requires=[
          'clang==5.0',
          'Box2D==2.3.10',
          'pandas==1.3.3',
          'pyneat==0.1.3',
          'numpy==1.19.5'
          ]
     )

