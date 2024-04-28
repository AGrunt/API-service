FROM python:3.9-slim
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY ./templates ./templates
COPY ./static ./static
COPY ./api.py ./api.py
EXPOSE 5000
ENV FLASK_APP=api.py
CMD ["flask", "run", "--host", "0.0.0.0"]