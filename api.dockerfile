FROM python:3.9-slim
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY ./templates ./templates
COPY ./static ./static
COPY ./api.py ./api.py
COPY ./model_trainer_group.py ./model_trainer_group.py
COPY ./model_trainer_kmeans.py ./model_trainer_kmeans.py
COPY ./model_trainer_user.py ./model_trainer_user.py
COPY ./user_group_updater.py ./user_group_updater.py
COPY ./training_pipeline.py ./training_pipeline.py

EXPOSE 5000
ENV FLASK_APP=api.py
CMD ["flask", "run", "--host", "0.0.0.0"]