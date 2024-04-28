FROM python:3.12-slim
WORKDIR /app
COPY ./flask-app-requirements.txt /app
RUN pip install -r flask-app-requirements.txt
COPY ./templates ./templates
COPY ./static ./static
COPY ./api.py ./api.py
EXPOSE 5000
ENV FLASK_APP=api.py
CMD ["flask", "run", "--host", "0.0.0.0"]