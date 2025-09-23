# Use continuumio/miniconda3 as a base image 
FROM continuumio/miniconda3:latest

# Set /HW3Assigned 2/crontab as a working directory
WORKDIR /HW3Assigned/crontab

# Copy environment.yml
COPY * .

# install cron
RUN apt-get update && apt-get -y install cron

# create a log file
RUN touch /var/log/cron.log

# Add crontab file
COPY api-cron /etc/cron.d/api-cron

# Apply cron job 
RUN chmod 0644 /etc/cron.d/api-cron

CMD ["cron", "-f"]