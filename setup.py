#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Tt bot setup.py
#
##
import os, sys,contextlib,pip

try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup, find_packages


name = "CryptoKitties TG Bot"

rootdir = os.path.abspath(os.path.dirname(__file__))

links=[]
requires=[]

#Python 3.4 and above
if sys.version_info < (3, 6, 0, 'final', 0):
	raise SystemExit ('Only Python 3.6 or later is supported!')

#Opening requirements.txt to obtain a list of libraries needed

	# new versions of pip requires a session
requirements = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

for item in requirements:
	# we want to handle package names and also repo urls
	if getattr(item, 'url', None):  # older pip has url
		links.append(str(item.url))
	if getattr(item, 'link', None): # newer pip has link
		links.append(str(item.link))
	if item.req:
		requires.append(str(item.req))

setup(
		name='Cronus',
		version='2.0.0',
		url='https://github.com/xlanor/SIM-UoW-Timetable-bot-v2',
		license='AGPL v3',
		author='xlanor',
		author_email='contact@jingk.ai',
		description='An unoffical bot for SIMConnect',
		long_description='Scraping timetables since 2017.',
		packages=find_packages(),
		include_package_data=True,
		zip_safe=False,
		platforms='any',
		install_requires=requires,
		dependency_links=links
	)