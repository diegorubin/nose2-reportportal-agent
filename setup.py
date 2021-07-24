from setuptools import find_packages, setup

setup(
    name="nose2-reportportal-agent",
    version="0.0.1",
    url="https://github.com/diegorubin/nose2-reportportal-agent",
    author="Diego Rubin",
    author_email="contact@diegorubin.dev",
    license="GPL2",
    include_package_data=True,
    description="Report Portal integration with nose2",
    install_requires=["nose2", "reportportal-client"],
    classifiers=["Development Status :: 3 - Alpha"],
    packages=find_packages(),
)
