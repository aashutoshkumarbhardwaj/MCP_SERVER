FROM python:3.11-slim

WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all your project files (main.py, serv.py, etc.)
COPY . .

# Expose the mandatory Hugging Face port
EXPOSE 7860

# Execute your server script
CMD ["python", "serv.py"]
