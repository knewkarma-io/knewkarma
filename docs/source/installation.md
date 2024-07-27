# Installation

Get started with Knew Karma through the simple installation process, whether you prefer using a CLI, Python library,
or Docker. Follow these steps to get up and running.

## PyPI

You'll need to have Python 3.10 or later installed on your system in order to install Knew Karma from PyPI. You can
install it by running the following command:

```commandline
pip install knewkarma
```

## Snap Store

If you prefer installing Knew Karma from the Snap Store instead, you can either run `snap install knewkarma`, or Open
the Ubuntu
Software desktop app (assuming snap is already installed), and search for "Knew Karma", then proceed to install the
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