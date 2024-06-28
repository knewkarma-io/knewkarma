# Installation Guide for Knew Karma

Get started with Knew Karma through the simple installation process, whether you prefer using a CLI, Python library,
Docker, or GUI for Windows. Follow these steps to get up and running.

## PyPI Package

Ensure you have Python 3.10 or later on your system to use Knew Karma. You can install the CLI and Python library
directly from PyPI.

```commandline
pip install knewkarma
```

## Snap Package

If you prefer installing the snap package instead, you can either run `snap install knewkarma`, or Open the Ubuntu
Software desktop app (assuming snap is already installed), and search for "Knew Karma", and proceed to install the
package.

## Building a Docker Image

If you prefer containerising Knew Karma, you can build the Docker image with the following steps:

1. **Clone the repository** to your system

```
git clone https://github.com/bellingcat/knewkarma.git
``` 

2. **Navigate to the cloned *knewkarma* directory**

```
cd knewkarma
```

3. **Build the Docker image**

```
docker build -t knewkarma .
```