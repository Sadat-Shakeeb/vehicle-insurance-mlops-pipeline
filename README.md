# vehicle-insurance-mlops-pipeline
A complete Production-ready MLOps pipeline for vehicle insurance prediction including data ingestion from MongoDB, data validation, feature engineering, model training, S3 model registry, and CI/CD deployment using Docker, GitHub Actions, and AWS EC2.

## Retraining the Model 🔁
If you need to update the preprocessing or the model, run the training pipeline:

```powershell
# from the repository root
C:/Users/sadat/.conda/envs/vehicle/python.exe -c "from src.pipline.training_pipeline import TrainPipeline; TrainPipeline().run_pipeline()"
```

This will:
1. ingest data (from MongoDB or a cached CSV),
2. validate, transform and train a new model,
3. save the preprocessing object and trained model under `artifact/<timestamp>/`.

### Offline mode
If you do **not** have a MongoDB connection available, the pipeline now
automatically reuses the most recent exported CSV located under
`artifact/*/data_ingestion/feature_store/data.csv`. This makes it easy to
retrain locally without network access.

> **Note:** the model and preprocessor no longer expect an `id` column. Any
> identifier field will be stripped during prediction and is never included in
> the training data.  Keep your feature inputs limited to the fields defined
> in the `VehicleData` class (Gender, Age, etc.).

Make sure to set the following environment variables when deploying to
cloud services:

- `MONGODB_URL` – MongoDB connection string for ingestion.
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` – credentials for
  pushing models to S3 (used during evaluation and model pusher stages).
