from distutils.core import setup

setup(name='planetpred',
      version='0.1.2',
      description='A planet prediction algorithm based on stellar abundances, as referenced in Hinkel et al. 2019, ' +
                  'created by Dr Natalie Hinkel',
      author='Natalie Hinkel, Richard Galvez',
      author_email='natalie.hinkel@gmail.com',
      packages=['planetpred'],
      requires=['numpy', "pandas", "PyYaml", "xgboost", "matplotlib", "scipy", "sklearn"]
      )
