# ==============================================================================
#  SETUP_HACK_ENV: Containerized Ethical Hacking & Pentesting Environment Suite
#  Base: Official Kali Linux Rolling Release
# ==============================================================================

FROM kalilinux/kali-rolling:latest

LABEL maintainer="Karthik Lal <https://karthiklal.in>"
LABEL description="Setup Hack Env - Complete Automated Ethical Hacking & Red Team Suite"
LABEL version="4.0.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /opt/setup_hack_env

# 1. Update APT indices and install foundational build toolchain, Python, Go, and network utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    golang-go \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    p7zip-full \
    net-tools \
    dnsutils \
    whois \
    nmap \
    tcpdump \
    tor \
    proxychains4 \
    htop \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy the entire repository into /opt/setup_hack_env
COPY . /opt/setup_hack_env/

# 3. Create persistent tools storage mount directory
RUN mkdir -p /tools && chmod 777 /tools

ENV TOOLS_DIR=/tools
WORKDIR /opt/setup_hack_env

# Default entrypoint runs setup-hack targeting the persistent container volume
ENTRYPOINT ["python3", "setup-hack.py", "--dir", "/tools"]
CMD []
