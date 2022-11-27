import shutil
import requests

"""
# OPEN BROWSER AND GET IMAGE LINK TO BE DOWNLOADED
"""

imagePath = "https://edumilestones.com/blog/images/What-after-12th.png"

response = requests.get(imagePath, stream = True)
with open(imagePath.split("/")[-1], 'wb') as f:
    shutil.copyfileobj(response.raw, f)
