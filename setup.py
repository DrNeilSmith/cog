from setuptools import setup


setup(name='cogdb',
      version='3.0.1',
      description='Persistent Embedded Graph Database',
      url='https://github.com/DrNeilSmith/cog/',
      author='Arun Mahendra',
      author_email='arunm3.141@gmail.com',
      license='MIT',
      packages=['cog'],
      install_requires=['xxhash==2.0.2'],
      zip_safe=False)
