FROM python:3.10

# Set the working directory
WORKDIR /app

# Add the src directory to the PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PYTHONPATH "${PYTHONPATH}:/app/modules"

# Copy the Python script and the configuration folder to the container
COPY requirements.txt /app/

# Copy the rest of the application code into the container
COPY /modules /app/modules

# Install python3-venv package
RUN apt-get update && apt-get install -y python3-venv

# Create a virtual environment
RUN python3 -m venv /venv

RUN . /venv/bin/activate \
    && pip install -r requirements.txt

CMD ["/bin/bash", "-c", "source /venv/bin/activate && python3 modules/main_loop.py"]

