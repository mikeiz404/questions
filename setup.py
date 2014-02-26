from setuptools import setup, find_packages

requires = ['pyramid', 'pyramid_chameleon', 'WebError', 'pymongo', 'elasticsearch', 'pyramid_mako']

setup(name='project',
      version='0.0',
      description='project',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="Niall O'Higgins",
      author_email='nialljohiggins@gmail.com',
      url='https://github.com/niallo/pyramid_mongodb',
      keywords='web pyramid pylons mongodb',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="project",
      entry_points = """\
      [paste.app_factory]
      main = project:main
      """,
      paster_plugins=['pyramid'],
      )

