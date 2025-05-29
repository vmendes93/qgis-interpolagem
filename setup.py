from setuptools import find_packages, setup

setup(
    name="qgis_interpolador",
    version="0.1.0",
    description="Ferramenta de interpolação espacial com IDW e Krigagem para uso com QGIS ou Python puro",
    author="Vinicius Mendes",
    author_email="vmendes@vmendes.xyz",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "matplotlib"
        "pykrige",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
