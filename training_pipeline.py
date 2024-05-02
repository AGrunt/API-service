from model_trainer_kmeans import train_kmeans_model
from user_group_updater import update_user_groups_using_kmeans_model
from model_trainer_group import train_group_model
from model_trainer_user import train_user_model

def run_model_training_pipeline():
    print('Running model training pipeline...')
    train_kmeans_model()
    update_user_groups_using_kmeans_model()
    train_group_model()
    train_user_model()
    print('Model training pipeline complete.')