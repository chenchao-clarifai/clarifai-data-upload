# Data Upload Clarified
Upload datasets in bulk to Clarifai apps as smooth as butter


```python
import src as upload

prod = upload.engine.TextClassification('prod', 'YOUR_API_KEY')
print(prod)

with prod:
    for item in python_dataset:
        prod(text=item['text'], labels=[str(item['label'])])

print(prod.info())
```