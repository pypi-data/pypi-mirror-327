from setuptools import setup, find_packages

setup(
    name="my-ml-toolkit",  # New unique package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy"
    ],
    author="Your Name",
    author_email="your_email@example.com",
    description="A custom ML package with NumPy, Pandas, Scikit-learn, and SciPy.",
    url="https://github.com/yourusername/my_ml_toolkit",  # Update if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
