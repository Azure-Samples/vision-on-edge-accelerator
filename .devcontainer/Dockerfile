# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.217.4/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.9-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
# libgeos-dev is required Mac M1
RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libgeos-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# install files for Azure
# RUN apt-get install -y libasound2

# [Optional] Uncomment this line to install global node packages.
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g mega-linter-runner" 2>&1

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales && update-locale LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US
RUN ["/bin/bash", "-c", "source /etc/default/locale"]

RUN pip3 --disable-pip-version-check --no-cache-dir install \
    opencv-python-headless==4.5.5.62 \
    Shapely==1.8.1.post1 \
    onnxruntime==1.12.1 \
    Pillow==9.2.0

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
RUN pip3 --no-cache-dir install iotedgehubdev==0.14.14
RUN pip3 --no-cache-dir install iotedgedev==3.3.4
RUN pip3 --no-cache-dir install azure-cli==2.39.0
## Azure Bicep Install does not work on M1 Mac, hence doing it manually
# RUN su vscode -c "az bicep install" 2>&1
ARG TARGETARCH
RUN if [ "$TARGETARCH" = "arm64" ]; then ARCHITECTURE=arm64; elif [ "$TARGETARCH" = "amd64" ]; then ARCHITECTURE=x64; fi \
    && curl -Lo bicep "https://github.com/Azure/bicep/releases/latest/download/bicep-linux-${ARCHITECTURE}" \
    && chmod +x ./bicep \
    && mv ./bicep /usr/local/bin/bicep \
    && su vscode -c "mkdir -p /home/vscode/.azure/bin && cp -f /usr/local/bin/bicep /home/vscode/.azure/bin/bicep" 2>&1
RUN su vscode -c "az extension add --name azure-iot" 2>&1
COPY label-reader/modules/label_extraction/requirements.txt /tmp/pip-tmp/requirements.label_extraction.txt
COPY label-reader/modules/web_app_api/requirements.txt /tmp/pip-tmp/requirements.web_app_api.txt
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.label_extraction.txt
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.web_app_api.txt
RUN rm -rf /tmp/pip-tmp

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
#   need to add user to group video to access GPU
RUN usermod -a -G video $USERNAME