FROM ghcr.io/anomalyco/opencode:1.18.25

# Create the opencode user with proper UID/GID and home directory
RUN groupadd --gid 1000 opencode && \
    useradd --uid 1000 --gid 1000 --home /home/opencode --shell /bin/bash opencode && \
    mkdir -p /home/opencode/.config /home/opencode/.local /home/opencode/.cache /home/opencode/.local/share/opencode && \
    chown -R 1000:1000 /home/opencode

# Set the working directory to the user's home
WORKDIR /home/opencode

# Switch to the opencode user
USER 1000:1000