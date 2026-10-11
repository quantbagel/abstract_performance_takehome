# Thin runnable starting point, not a from-source LLMD build.
# Keep in sync with baseline/lock.json. Hardware compatibility still needs a pilot.
ARG BASE_IMAGE=docker.io/zmlai/llmd@sha256:0a2cd01a2e53c78934a8cfef66f8668da7666be4954a5d18b72df089c54ea34f
FROM --platform=linux/amd64 ${BASE_IMAGE}
LABEL org.opencontainers.image.title="Abstract LLMD take-home baseline"
# Preserve the inspected upstream ENTRYPOINT; no shell or Python in the serving path.
CMD ["--io-impl=zio"]
