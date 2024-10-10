# syntax=docker/dockerfile:1

FROM python:slim

LABEL maintainer="Richard Mwewa <https://gravatar.com/rly0nheart>"
LABEL description="A Reddit data analysis toolkit."

WORKDIR /app

# Create a non-root user 'knewkarmauser' without prompting for password or user info
RUN adduser --disabled-password --gecos "" knewkarmauser

# Switch to the newly created non-root user for security best practices
USER knewkarmauser

# Change working directory to the non-root user's home directory
WORKDIR /home/knewkarmauser

# Copy all project files into the container, and set ownership to the non-root user
COPY --chown=knewkarmauser:knewkarmauser . .

# Set environment variable to indicate the app is running in a Docker container
ENV IS_DOCKER_CONTAINER=1

# Disable pip's version check to avoid seeing upgrade notices during container builds
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Add the non-root user's local binary directory to the PATH so locally installed packages can be run directly
ENV PATH="/home/knewkarmauser/.local/bin:${PATH}"

# Upgrade pip and install Poetry in the non-root user's local environment using --user
RUN pip install --user --upgrade pip poetry

# Install project dependencies via Poetry as the non-root user
RUN poetry install --extras core

ENTRYPOINT ["poetry", "run", "knewkarma"]
