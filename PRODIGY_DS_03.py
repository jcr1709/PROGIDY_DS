# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

bank=pd.read_csv("/content/bank-full1.csv")

bank.columns

bank.dtypes

bank.isna().sum()

mapping = {'yes': 1, 'no': 0}

# Apply mapping to the 'Response' column
bank['y'] = bank['y'].map(mapping)

# Display the result
print(bank)

bank.shape

bank['y'].value_counts()

bank['age'].value_counts()

bank['marital'].value_counts()

bank['education'].value_counts()

bank['housing'].value_counts()

bank['loan'].value_counts()

bank.duplicated().sum()

bank.describe()

for x in bank.columns:
  print("\n\n",bank[x].value_counts())

bank.columns

categorical = bank.select_dtypes(include = 'object')
categorical

bank["job"] = bank["job"].replace(["management", "admin.","services"], "Working_Professionals")
bank["job"] = bank["job"].replace(["self-employed", "entrepreneur"], "Business")
bank["job"] = bank["job"].replace(["blue-collar","technician","housemaid"], "Household")
bank["job"] = bank["job"].replace(["retired", "student", "unemployed", "unknown"], "Unemployed")

bank['job'] = bank['job'].map( {'Working_Professionals':1, 'Unemployed':-1, 'Business':2, 'Household':0} )
bank.head(10)

bank["job"].value_counts()

sns.countplot(x = "job", data=bank)

ax = bank['day'].value_counts() \
    .head(10) \
    .plot(kind='bar', title='Top 10 days data count')
ax.set_xlabel('day')
ax.set_ylabel('Count')

bank["marital"].value_counts()
bank['marital'] = bank['marital'].map( {'married':1, 'single':0, 'divorced': -1} )

sns.barplot(x="job", y="marital", hue="y", data=bank)

sns.violinplot(bank,x='day',y='age',grid=True,color='pink')

bank  =bank.rename(columns = {"default": "Credit Card"})

bank["housing"].value_counts()

bank["housing"] = bank["housing"].map( {'yes':1, 'no':0} )
bank["loan"] = bank["loan"].map( {'yes':1, 'no':0} )
bank.head(1)

bank['Credit Card'].value_counts()
bank['Credit Card'] = bank['Credit Card'].map( {'yes':1, 'no':0} )
bank.head(1)

bank['contact'] = bank['contact'].map( {'cellular':1, 'telephone':0, 'unknown': -1} )

bank= bank.rename(columns = {"campaign": "No_of_calls_done_by_team", "pdays":"No_of_days_after_calling", "previous":"Conatcts before call", "poutcome":"Results of Campaign"})

bank['Results of Campaign'].value_counts()
bank["Results of Campaign"] = bank["Results of Campaign"].replace(['unknown'],'other')

bank['Results of Campaign'].value_counts()
bank["Results of Campaign"] = bank["Results of Campaign"].replace(['unknown'],'other')
bank.head()

bank['Results of Campaign'] = bank['Results of Campaign'].map( {'success':1, 'failure':0, 'other': -1} )
bank.head(1)

bank = bank.rename(columns={"day":"Date"})
bank = bank.drop(['duration', 'Date', 'month'], axis = 1)

bank['education'] = bank['education'].map( {'primary':1, 'unknown':0, 'secondary':2, 'tertiary':3} )

bank.corr()

corr=bank.corr()
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(corr, annot=True, ax=ax, cmap = 'coolwarm')

plt.figure(figsize=(10,7))
plt.pie(x=bank['y'].value_counts().values,
        labels=bank['y'].value_counts().index,
        autopct='%2.2f%%')
plt.title('Deposit Subscibed or not')
plt.show()

bank.head

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score



x = bank.drop('y',axis=1)
y = bank['y']

X_train, X_test, y_train, y_test = train_test_split(x,y,test_size = 0.25, shuffle = True, random_state = 30)

print('train samples ->', X_train.shape[0])
print('test samples ->', X_test.shape[0])

bank.dtypes



clf = DecisionTreeClassifier()

# Train the model on the training data
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")