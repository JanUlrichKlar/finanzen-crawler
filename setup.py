import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finanzen-fundamentals", # Replace with your own username
    version="0.0.21",
    author="Joshua Hruzik",
    author_email="joshua.hruzik@gmail.com",
    description="API to fetch stock data fundamentals from finanzen.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jhruzik/Finanzen-Fundamentals",
    packages=setuptools.find_packages(),
    package_data={'finanzen-fundamentals': ['finanzen_fundamentals/*.csv']},
    install_requires=["requests", "bs4", "lxml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	"Intended Audience :: Financial and Insurance Industry",
	"Intended Audience :: Science/Research",
	"Topic :: Office/Business :: Financial",
	"Topic :: Office/Business :: Financial :: Investment"
	
    ],
    python_requires='>=3.6',
)
