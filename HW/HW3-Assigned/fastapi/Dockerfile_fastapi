FROM continuumio/miniconda3

WORKDIR /HW3Assigned/fastapi

COPY environment.yml .

RUN apt-get update && apt-get install -y gcc libffi-dev \
    && conda env create -f environment.yml \
    && conda clean --all -y

COPY . .

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "msds692_hw", "uvicorn", "extract_save_data:app", "--host", "0.0.0.0", "--port", "8000"]
