# baikal-sentiment

This repo contains the code to go into Tencent GPU instance for nightly/weekly prediction of text sentiments.

The intended flow of the process is:
1. Check and install any missing dependencies
2. load_data.py: Download data daily data from Aion MongoDB into data directory
3. preprocess.py: Preprocess downloaded data 
4. predict.py: Download and configure the model from HuggingFace, construct dataloader object, and perform prediction
5. aggregate.py: Aggregate sentiment labels for any texts that were split up due to length constraint
6. upload.py: upload to Aion MongoDB to the collection named user_posts_temp with 'schema' identical to user_posts
7. Clean up data directory