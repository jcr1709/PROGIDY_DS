import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

train_df = pd.read_csv('/content/train.csv')
test_df = pd.read_csv('/content/test.csv')
submission = pd.read_csv('/content/gender_submission.csv')

train_df.head()

train_df.tail()

train_df.sample(10)

train_df.isna().sum()

train_df.shape

train_df.dtypes

test_df.isna().sum()

train_df = train_df.fillna(train_df.median())

for column in train_df.columns:
    if train_df[column].dtype == 'object':  # Check if the column contains categorical data
        mode_val = train_df[column].mode()[0]  # Calculate the mode for categorical columns
        train_df[column].fillna(mode_val, inplace=True)

test_df = test_df.fillna(test_df.median())

for column in test_df.columns:
    if test_df[column].dtype == 'object':  # Check if the column contains categorical data
        mode_val = test_df[column].mode()[0]  # Calculate the mode for categorical columns
        test_df[column].fillna(mode_val, inplace=True)

train_df.isna().sum()

train_df['Sex'].value_counts()

train_df['SibSp'].value_counts()

train_df['Parch'].value_counts()

train_df['Embarked'].value_counts()

train_df.describe()

surv_train_df = train_df[train_df['Survived'] == 1]
surv_train_df.describe()

train_df.corr()

corr=train_df.corr()
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(corr, annot=True, ax=ax, cmap = 'coolwarm')

pclass_list = train_df['Pclass'].value_counts().index.to_list()
pclass_list.sort()
surv_rate_pclass = [1, 1, 1]
for i, pclass in enumerate(pclass_list):
    surv_rate_pclass[i] = len(train_df['Pclass'][train_df['Survived'] == 1][train_df['Pclass'] == pclass]) / len(train_df['Pclass'][train_df['Pclass'] == pclass])
surv_rate_pclass = pd.DataFrame({'Pclass' : pclass_list, 'Survival Rate' : surv_rate_pclass})
surv_rate_pclass

fare_surv = train_df['Fare'][train_df['Survived'] == 1].median()
fare_cas = train_df['Fare'][train_df['Survived'] == 0].median()
fare_desc = pd.DataFrame({'surv' : [0,1], 'median_fare' : [fare_cas,fare_surv]}, index = [0, 1])
fare_desc

fem_surv_rate = len(train_df.loc[(train_df['Survived'] == 1) & (train_df['Sex'] == 'female')]) / len(train_df.loc[train_df['Sex'] == 'female'])
mal_surv_rate = len(train_df.loc[(train_df['Survived'] == 1) & (train_df['Sex'] == 'male')]) / len(train_df.loc[train_df['Sex'] == 'male'])
print('Female Survival Rate: ', fem_surv_rate)
print('Male Survival Rate: ', mal_surv_rate)

embarked_values = train_df['Embarked'].value_counts().index.to_list()
embarked_survival = [1, 1, 1]
for i in range(len(embarked_values)):
    surv_rate = len(train_df[(train_df['Embarked'] == embarked_values[i]) & (train_df['Survived'] == 1)]) / len(train_df[train_df['Embarked'] == embarked_values[i]])
    embarked_survival[i] = surv_rate
result = pd.DataFrame({'port': embarked_values, 'surv_rate' : embarked_survival})
print(result)

fare_s = train_df['Fare'][train_df['Embarked'] == 'S'].median()
fare_c = train_df['Fare'][train_df['Embarked'] == 'C'].median()
fare_q = train_df['Fare'][train_df['Embarked'] == 'Q'].median()
fare_port_data = pd.DataFrame({'med_fare' : [fare_s, fare_c, fare_q],
                              'port' : ['S', 'C', 'Q']})
order = ['S', 'C', 'Q']
sns.barplot(data = fare_port_data, x = 'port', y = 'med_fare', hue = 'port')

sns.histplot(data = train_df, x = 'Pclass', hue = 'Embarked', multiple = 'stack')

sns.histplot(data = train_df, x = 'Age', hue = 'Survived', kde = True, label = 'all_data')

age_means = train_df.groupby(['Pclass', 'Sex'])['Age'].mean()
age_means

split_name = train_df['Name'].str.split(', ', expand = True)
title = split_name[1].str.split(". ", n = 1).str[0]
train_df['title'] = title
split_name = test_df['Name'].str.split(', ', expand = True)
title_test = split_name[1].str.split(". ", n = 1).str[0]
test_df['title'] = title_test
histplot = sns.histplot(data = train_df, y = 'title', hue = 'Survived', multiple = 'stack')

train_df['title'] = train_df['title'].replace(['Dr', 'Rev', 'Major', 'Col', 'th', 'Capt', 'Sir', 'Don', 'Jonkheer'], 'Rare')
test_df['title'] = test_df['title'].replace(['Dr', 'Rev', 'Major', 'Col', 'th', 'Capt', 'Sir', 'Don', 'Jonkheer'], 'Rare')
train_df['title'] = train_df['title'].replace(['Mlle', 'Ms', 'Lady', 'Mme', 'Dona'], 'Miss')
test_df['title'] = test_df['title'].replace(['Mlle', 'Ms', 'Lady', 'Mme', 'Dona'], 'Miss')
histplot = sns.histplot(data = train_df, y = 'title', hue = 'Survived', multiple = 'stack')

y = train_df['Survived']
x_train_df = train_df.drop(labels = 'Survived', axis = 1)
num_features = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
cat_features = ['Sex', 'Embarked', 'title']
X_cat = pd.get_dummies(x_train_df[cat_features])
X_num = x_train_df[num_features]
X = X_cat.join(X_num)
X_cat_test = pd.get_dummies(test_df[cat_features])
X_num_test = test_df[num_features]
X_test = X_cat_test.join(X_num_test)

from sklearn.model_selection import train_test_split

X, X_val, y, y_val = train_test_split(X, y, random_state = 0)

from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier()
gbc.fit(X, y)
gbc_score = gbc.score(X_val, y_val)
gbc_score

X.isna().sum()

X_test.isna().sum()

predictions = gbc.predict(X_test)

output = pd.DataFrame({'PassengerId': test_df.PassengerId, 'Survived': predictions})
output.to_csv('submission.csv', index=False)
print("Your submission was successfully saved!")
