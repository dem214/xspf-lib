import setuptools

with open("README.rst", 'r') as readme:
    long_desc = readme.read()

setuptools.setup(
    name="xspf-lib",
    version="0.1.3",
    author="Dzmitry Izaitka",
    author_email="dem214overlord@gmail.com",
    description="Library for work with xspf format",
    long_description=long_desc,
    long_description_content_type="text/x-rst",
    url="https://github.com/dem214/xspf-lib",
    packages=["xspf_lib"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
    ],
    keywords='xspf playlist',
    python_requires='>=3.8',
)
