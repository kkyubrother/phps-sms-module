import setuptools


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="php_school_sms_module",  # Replace with your own username
    version="0.0.2",
    author="kkyubrother",
    author_email="kkyubrother.0@gmail.com",
    description="PHP School SMS module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkyubrother/phps_sms_module",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
