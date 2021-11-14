from distutils.core import setup

setup(name='RestrictedNeat',
      version='0.1',
      description='Restricted Neat',
      author='Piotr Gnyś',
      author_email='regule@runbox.com',
      package_dir = {'': 'scripts'},
      packages=['resneat.backend'],
     )

