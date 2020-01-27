from setuptools import setup

setup(
    name="pytchuka",
    version="0.0.8",
    author="",
    author_email="",
    install_requires=["marshmallow==3.3.0", "falcon==2.0.0", "falcon-multipart==0.2.0", "deepdiff==4.0.9"],
    description="A very simple http mock server",
    license="MIT",
    keywords="mock server http",
    url="",
    packages=['pytchuka'],
    entry_points={
        'console_scripts': [
            'pytchuka = pytchuka.pytchuka:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
