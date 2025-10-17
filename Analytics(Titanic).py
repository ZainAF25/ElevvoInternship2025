import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\Zain Farooqi\Desktop\DAtasks\TASK2\trainn.csv") 
df.drop('Cabin', axis=1, inplace=True)
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

if 'Name' in df.columns:
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    rare_titles = ['Lady', 'Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona']
    df['Title'] = df['Title'].replace(['Mlle', 'Ms'], 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    df['Title'] = df['Title'].replace(rare_titles, 'Rare')
    df.drop('Name', axis=1, inplace=True) 


df['Survived'] = df['Survived'].astype(int)
df['Pclass'] = df['Pclass'].astype('category')
df['Sex'] = df['Sex'].astype('category')
df['Embarked'] = df['Embarked'].astype('category')
df['IsAlone'] = df['IsAlone'].astype('category')
if 'Title' in df.columns:
    df['Title'] = df['Title'].astype('category')


print("---  Summary Statistics (Numerical Features) ---")
print(df.describe())
print("-" * 40)

print("\n---  Survival Rate by Gender and Passenger Class (Group Insight) ---")
if 'Sex' in df.columns and 'Pclass' in df.columns and 'Survived' in df.columns:
    survival_rate_grouped = df.groupby(['Sex', 'Pclass'])['Survived'].mean().unstack()
    print(survival_rate_grouped)
print("-" * 40)

df_corr = df.copy()
if 'Sex' in df_corr.columns:
    df_corr['Sex'] = df_corr['Sex'].astype('category') 
    df_corr['Sex_Encoded'] = df_corr['Sex'].cat.codes 

numerical_cols = [col for col in ['Survived', 'Sex_Encoded', 'Pclass', 'Age', 'FamilySize', 'IsAlone', 'Fare', 'SibSp', 'Parch'] if col in df_corr.columns]
corr_matrix = df_corr[numerical_cols].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix of Key Features with Survival')
plt.show()

if 'Sex' in df.columns and 'Pclass' in df.columns and 'Survived' in df.columns:
    plt.figure(figsize=(10, 6))
    survival_rate_plot_data = df.groupby(['Sex', 'Pclass'])['Survived'].mean().reset_index()

    sns.barplot(x='Pclass', y='Survived', hue='Sex', data=survival_rate_plot_data,
                palette={'female': 'darkorange', 'male': 'skyblue'}, edgecolor='black')
    plt.title('Survival Rate by Passenger Class and Gender')
    plt.xlabel('Passenger Class (1=1st, 2=2nd, 3=3rd)')
    plt.ylabel('Survival Rate (Mean of Survived)')
    plt.legend(title='Sex')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if 'Title' in df.columns and 'Survived' in df.columns:
    plt.figure(figsize=(8, 5))
    survival_by_title = df.groupby('Title')['Survived'].mean().sort_values(ascending=False).reset_index()

    sns.barplot(x='Title', y='Survived', hue='Title', data=survival_by_title, palette='viridis', edgecolor='black', legend=False)
    
    plt.title('Survival Rate by Passenger Title')
    plt.xlabel('Title')
    plt.ylabel('Survival Rate')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if 'FamilySize' in df.columns and 'IsAlone' in df.columns and 'Survived' in df.columns:
    plt.figure(figsize=(10, 6))

    sns.barplot(x='FamilySize', y='Survived', hue='IsAlone', data=df,
                palette='Set1', edgecolor='black', errorbar=None)
    
    plt.title('Survival Rate vs. Family Size')
    plt.xlabel('Family Size')
    plt.ylabel('Survival Rate (Mean of Survived)')
    plt.legend(title='Is Alone (1=Yes)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()