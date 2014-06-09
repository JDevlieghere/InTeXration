from distutils.core import setup
from pip.req import parse_requirements

install_requirements = parse_requirements('requirements.txt')
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='InTeXration',
    version='1.4.0dev',
    packages=['intexration'],
    package_data={'': ['config/*.cfg', 'views/*.tpl', 'static/*/*']},
    include_package_data=True,
    url='https://github.com/JDevlieghere/InTeXration',
    license='Apache License, Version 2.0',
    author='Jonas Devlieghere',
    author_email='info@jonasdevlieghere.com',
    description='LaTeX Integration Service',
    install_requires=requirements
)