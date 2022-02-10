FROM python:3.6-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY . /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt

# Run the application:
ENTRYPOINT ["tail", "-f", "/dev/null"]