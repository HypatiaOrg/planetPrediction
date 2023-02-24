from distutils.core import setup

setup(name='planetpred',
      version='0.1.3',
      description='A planet prediction algorithm based on stellar abundances, as referenced in Hinkel et al. 2019, ' +
                  'created by Dr Natalie Hinkel',
      author='Natalie Hinkel, Amílcar R. Torres-Quijano, Caleb Wheeler, Richard Galvez',
      author_email='natalie.hinkel@gmail.com',
      packages=['planetpred'],
      install_requires=['numpy', "pandas", "PyYaml", "xgboost", "matplotlib", "scipy", "sklearn"]
      )
