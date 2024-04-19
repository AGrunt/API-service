FROM python:3.12-slim
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY ./templates ./templates
COPY ./static ./static
COPY ./api-app.py ./api-app.py
EXPOSE 5000
ENV FLASK_APP=api-app.py
CMD ["flask", "run", "--host", "0.0.0.0"]