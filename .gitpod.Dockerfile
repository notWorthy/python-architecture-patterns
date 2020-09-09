FROM gitpod/workspace-postgres

ENV FLASK_APP=entrypoints/flask_app
ENV FLASK_ENV=development

ENV API_HOST=0.0.0.0
ENV API_PORT=3000

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/
