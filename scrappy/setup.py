from setuptools import setup

setup(
   name='scrappy',
   version='1.0',
   description='Scrape the planet!',
   author="Chepe's Crew",
   author_email='foomail@foo.com',
   packages=['scrappy'],
   install_requires=['requests', 'requests[socks]', 'bs4', 'exrex', 'lxml', 'dnspython'],
)
