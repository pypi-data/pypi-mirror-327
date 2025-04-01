from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gmk_utils",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.21.0",
    ],
    data_files=[
        ("gmk_utils/solrs", ["Z:/pypi/gmk_utils/src/gmk_utils/solr/solr-8.9.0.zip"])
    ],
    tests_require=["pytest"],
    test_suite="tests/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmk-dev/gmk_utils",
    license="MIT",
)