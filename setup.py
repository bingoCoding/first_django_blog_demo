from idna.idnadata import scripts
from setuptools import setup, find_packages
setup(
    name='django_blog_program',
    version='0.1',
    description='A simple blog program based on Django',
    author='supsky',
    author_email='',
    url='',
    license='MIT',
    packages=find_packages('django_blog_program'),
    package_dir={'': 'django_blog_program'},
    package_data={ # 打包方式一
        '': [
            'themes/*/*/*/*', # 需要按目录层级匹配
        ]
    },
    #include_package_data=True, # 打包方式二，配合MANIFEST.in
    install_requires=[
        'Django==4.2.27',
        'mistune==3.2.0',
        'django-autocomplete-light~=3.12.1',
        'django-ckeditor~=6.7.3',
        'pillow~=10.4.0',
        'djangorestframework~=3.15.2',
        'coreapi~=2.3.3',
        'django-debug-toolbar~=4.4.6',
        # 'mysqlclient~=2.2.7'
        'django-redis~=5.4.0',
        'hiredis~=3.3.0',
    ],
    extras_require={
        'ipython': ['ipython==4.2.27']
    },
    scripts=[
        'django_blog_program/manage.py',
    ],
    entry_points={
        'console_scripts': [
            'django_blog_program = manage:main',
        ]
    },
    classifiers=[
        # 项目状态 3-Alpha 4-Beta 5-Production/Stable
        'Development Status :: 4 - Beta',
        # 项目受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # 许可
        'License :: OSI Approved :: MIT License',

        # 支持的Python版本
        'Programming Language :: Python :: 3.9',

    ]
)

