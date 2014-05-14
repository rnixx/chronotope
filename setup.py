import os
from setuptools import (
    setup,
    find_packages,
)


version = '0.1.dev0'
shortdesc = 'Chronotope - **Time has come today**'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(name='chronotope',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='',
      author='Squarewave Computing',
      author_email='rnix@squarewave.at',
      url=u'http://github.com/rnixx/chronotope',
      license='GPL2',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'hurry.filesize',
          'zope.sqlalchemy',
          'node.ext.ugm',
          'repoze.tm2',
          'repoze.retry',
          'cone.app',
          'yafowil.widget.autocomplete',
          'yafowil.widget.datetime',
          'yafowil.widget.wysihtml5',
      ],
      extras_require = dict(
          test=[
                'interlude',
          ]
      ),
      tests_require=[
          'interlude',
      ],
      test_suite = "chronotope.tests.test_suite",
      message_extractors = {
          '.': [
              ('**.py', 'lingua_python', None),
              ('**.pt', 'lingua_xml', None),
          ]
      },
      entry_points = """\
      [paste.filter_app_factory]
      session = chronotope.sql:make_app
      """
      )
