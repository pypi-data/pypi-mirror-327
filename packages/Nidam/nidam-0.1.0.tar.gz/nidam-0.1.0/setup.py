from setuptools import setup, find_packages

setup(
    name="nidam",
    version="0.1.0",
    author="JILE",
    author_email="y.dideh@yahoo.com",
    description="Run any open-source LLMs, such as DeepSeek and Llama, in the terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ydideh810/nidamllm",
    packages=find_packages(),
    install_requires=[
  "bentoml",
  "typer",
  "questionary",
  "pyaml",
  "psutil",
  "pathlib",
  "pip_requirements_parser",
  "nvidia-ml-py",
  "dulwich",
  "tabulate",
  "uv",
  "openai==1.61.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
