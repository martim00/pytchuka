from setuptools import setup

setup(
    name="pytchuka",
    version="0.0.7",
    author="",
    author_email="",
    install_requires=["marshmallow", "falcon", "falcon-multipart"],
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
