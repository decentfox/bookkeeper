import setuptools

setuptools.setup(
    name="bookkeeper",
    version="0.1.0",
    url="http://decentfox.com",

    author="DecentFoX Studio",
    author_email="support@decentfox.com",

    description="A bookkeeping web application",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    # namespace_packages=['bookkeeper'],
    include_package_data=True,
    package_data={
        # 'sample': ['package_data.dat'],
    },
    data_files=[
        # ('etc', ['conf/sentinel-example.conf'])
    ],

    install_requires=[
        'decent-web==0.1.0',
        'Flask-Admin==1.4.0',
        'Flask-Security==1.7.5',
        'psycopg2==2.6.1',
        'SQLAlchemy-Utils==0.31.4',
    ],

    entry_points={
        'console_scripts': [
            'import-account-title=bookkeeper.utils:import_account_titles',
        ],
    },

    license='LGPL',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
