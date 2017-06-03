import os
from setuptools import setup, find_packages
from imp import find_module, load_module

found = find_module('_version', ['agorawebdeploy'])
_version = load_module('_version', *found)


def _find_package_data(package_list=None):
    """find all non-python files for package inclusion"""
    exclusions = ['.py', '.pyc']
    ret = []
    if not package_list:
        package_list = find_packages()
    for package in package_list:
        for root, dirs, files in os.walk(package):
            for filename in files:
                for exclusion in exclusions:
                    if not filename.endswith(exclusion):
                        ret.append(
                            os.path.join(root, filename).replace('{0}/'.format(package), ''))
    return ret


setup(
    name='agora-webdeploy',
    version=_version.__version__,
    description='client to automate deployment of web artifacts to s3 for Agora web apps',
    author='Agora',
    author_email='dl-agora-support@veracode.com',
    url='https://gitlab.laputa.veracode.io/agora',
    license='MIT',
    packages=['agorawebdeploy'],
    package_data={'': _find_package_data()},
    entry_points={'console_scripts': ['agorawebdeploy = agorawebdeploy.cli:main']},
    install_requires=[
        'docopt>=0.6.2,<1.0',
        'funcy>=1.4.4,<2.0',
        'boto3==1.4.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ],
)
