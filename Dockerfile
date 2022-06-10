#####################
### Builder image ###
#####################
# using ubuntu LTS version
FROM ubuntu:22.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install python
RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.10 -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

####################
### Runner image ###
####################
FROM ubuntu:22.04 AS runner-image

# DEFAULT ARGS that can be changed
ARG APP_NAME="Flask App"
ARG LOG_LEVEL="4"
# specify WORKERS to match the number of CPU cores allocated to your container
ARG WORKERS="2"
# specify WORKER_CONNECTIONS to the number determined by (client_count/workers)*2
ARG WORKER_CONNECTIONS="1000"

# set environment variables
ENV APP_NAME=$APP_NAME
ENV LOG_LEVEL=$LOG_LEVEL
ENV WORKERS=$WORKERS
ENV WORKER_CONNECTIONS=$WORKER_CONNECTIONS

# install python
RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create unprivileged user and virtual environment
RUN useradd --create-home myuser
COPY --from=builder-image /home/myuser/venv /home/myuser/venv

# create directory for runtime and switch to user
RUN mkdir -p /opt/flask
WORKDIR /opt/flask
COPY . .
RUN chown -R myuser:myuser /opt/flask
USER myuser

# expose port
EXPOSE 5000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# /dev/shm is mapped to shared memory and is used to improve gunicorn heartbeat performance
CMD ["gunicorn","-b","0.0.0.0:5000", \
	 			"--workers","${WORKERS}", \
				"--worker_connections","${WORKER_CONNECTIONS}", \
				"--worker_class","gevent", \
				"--worker-tmp-dir","/dev/shm", \
				"--preload", \
				"api:app"]
