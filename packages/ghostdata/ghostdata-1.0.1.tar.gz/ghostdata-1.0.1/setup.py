from setuptools import setup, find_packages

setup(
    name="ghostdata",  # The package name on PyPI
    version="1.0.1",  # Start with version 1.0.0
    packages=find_packages(),
    install_requires=[
        "pillow",
        "pypdf",
        "mutagen",
        "imageio[ffmpeg]",
        "ffmpeg-python",
    ],
    author="Oxde",
    author_email="your-email@example.com",
    description="GhostData: Securely remove metadata from images, PDFs, videos, and audio files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oxde/ghostdata",
    license="CC BY-NC 4.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
