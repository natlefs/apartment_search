import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finn_apartment_search",
    version="2.01",
    author="Natalie L. J.",
    author_email="natalie@jkbn.no",
    description="A project for searching Finn.no apartments and intersecting their info with other data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natlefs/apartment_search/",
    project_urls={},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3",
        "aiosignal>=1",
        "async-timeout>=4",
        "attrs>=21",
        "certifi>=2022.5.18.1",
        "charset-normalizer>=2",
        "cssselect>=1",
        "frozenlist==1.3.0"
        "gql>=3",
        "graphql-core>=3",
        "idna>=3",
        "lxml>=4",
        "multidict>=6",
        "requests>=2",
        "urllib3>=1.2",
        "yarl>=1.7",
        
    ]
)