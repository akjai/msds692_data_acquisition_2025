# Use continuumio/miniconda3 as a base image 
FROM continuumio/miniconda3:latest

# Set /HW3Assigned/streamlit as a working directory
WORKDIR /HW3Assigned/streamlit

# Copy environment.yml
COPY * .

# create environment and install pip packages (including Streamlit)
RUN conda env create -f environment.yml -n msds692_hw \
    && conda run -n msds692_hw pip install streamlit

# expose port 8501
EXPOSE 8501

# run the main.py as streamlit app.
CMD ["conda", "run", "--no-capture-output", "-n", "msds692_hw", "streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
