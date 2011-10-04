# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import distribute_setup
distribute_setup.use_setuptools('0.6.10')

from setuptools import setup, find_packages

try:
    README = open('README.md').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements/apps.txt').read()
except:
    REQUIREMENTS = None

setup(
    name = 'django-openportfolio',
    version = "0.1.0",
    description = 'Django app for managing personal finances',
    long_description = README,
    install_requires=REQUIREMENTS,
    author = 'Evan Davey',
    author_email = 'evan.j.davey@gmail.com',
    url = 'http://github.com/evandavey/OpenPortfolio/',
    packages = find_packages(),
    include_package_data = True,
    classifiers = ['Development Status :: 1 - Planning',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)
