- This dataset is under this license: https://creativecommons.org/licenses/by/4.0/
- The original dataset is found here: https://www.kaggle.com/datasets/rmisra/news-category-dataset/data
- Dataset creator: Rishabh Misra
- The dataset was changed by doing the following:
  - removing rows with the following CLASSES: 'IMPACT','TASTE','WEIRD NEWS','U.S. NEWS','GOOD NEWS','LATINO VOICES','BLACK VOICES','FIFTY','CRIME','MEDIA','WOMEN','COMEDY','BUSINESS','MONEY'
  - combining some classes using this logic: 
  ```{python}
    if category in ['ARTS & CULTURE', 'CULTURE & ARTS', 'ARTS', 'ENTERTAINMENT']:
        return 'ARTS, CULTURE, & ENTERTAINMENT'
    if category in ['STYLE & BEAUTY', 'STYLE']:
        return 'STYLE & BEAUTY'
    if category in ['WELLNESS', 'HEALTHY LIVING']:
        return 'WELLNESS'
    if category in ['EDUCATION', 'COLLEGE']:
        return 'EDUCATION'
    if category in ['THE WORLDPOST', 'WORLD NEWS', 'WORLDPOST']:
        return 'INTERNATIONAL NEWS'
    if category in ['GREEN', 'ENVIRONMENT']:
        return 'ENVIRONMENT'
    if category in ['PARENTING', 'PARENTS']:
        return 'PARENTING'
  ```
  - downsampling and splitting into a training and test set.
