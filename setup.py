from setuptools import find_packages
from setuptools import setup
import os


version = '0.5.dev0'
shortdesc = 'Poptraces'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name='chronotope',
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
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pyOpenSSL',
        'html2text',
        'Whoosh',
        'lxml',
        'hurry.filesize',
        'zope.sqlalchemy',
        'node.ext.ugm',
        'repoze.tm2',
        'repoze.retry',
        'cone.app',
        'cone.sql',
        'yafowil.yaml',
        'yafowil.widget.autocomplete',
        'yafowil.widget.datetime',
        'yafowil.widget.image',
        'yafowil.widget.location',
        'yafowil.widget.select2',
        'yafowil.widget.wysihtml5',
        'yafowil.widget.recaptcha',
    ],
    extras_require=dict(
        test=[
              'interlude',
        ]
    ),
    tests_require=[
        'interlude',
    ],
    test_suite="chronotope.tests.test_suite"
)
