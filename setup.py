from setuptools import find_packages, setup


setup(
    name='toybox',
    version='1.0.0',
    description='This is the core library for the project toys-story',
    url='https://github.com/toys-story/toybox',
    author='chulmin.chae',
    author_email='ccm2800@naver.com',
    license='MIT',
    packages=find_packages(where="src"),
    package_dir={"", "src"}
)