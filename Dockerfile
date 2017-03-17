FROM python:3.6-alpine

RUN apk add --no-cache bash

# Set Python-related environment variables to reduce annoying-ness
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PORT=5000

CMD ["./run.sh"]
EXPOSE 5000
WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./
