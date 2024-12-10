import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Laden des Titanic-Datasets
def load_data(file_path):
    return pd.read_csv(file_path)

# 1. Grundlegende Analyse
def basic_analysis(df):
    survival_counts = df['Survived'].value_counts()
    class_distribution = df['Pclass'].value_counts()
    print("\nÜberlebensanzahl:")
    print(survival_counts)
    print("\nVerteilung der Passagierklassen:")
    print(class_distribution)

# 2. Gruppierte Analyse
def grouped_analysis(df):
    avg_fare_by_class = df.groupby('Pclass')['Fare'].mean()
    survival_rate_by_gender = df.groupby('Sex')['Survived'].mean()
    print("\nDurchschnittlicher Ticketpreis pro Klasse:")
    print(avg_fare_by_class)
    print("\nÜberlebensrate nach Geschlecht:")
    print(survival_rate_by_gender)

# 3. Datenbereinigung
def clean_data(df):
    print("\nDatenbereinigung gestartet...")
    print(f"Vorher: Fehlende Alterswerte: {df['Age'].isnull().sum()}")
    df['Age'] = df.groupby('Pclass')['Age'].transform(lambda x: x.fillna(x.mean()))
    print(f"Nachher: Fehlende Alterswerte: {df['Age'].isnull().sum()}")
    print(f"Vorher: Fehlende Embarked-Werte: {df['Embarked'].isnull().sum()}")
    df = df.dropna(subset=['Embarked'])
    print(f"Nachher: Fehlende Embarked-Werte: {df['Embarked'].isnull().sum()}")
    return df

# 4. Erweiterte Analyse
def advanced_analysis(df):
    survival_rate_by_age = df.groupby(pd.cut(df['Age'], bins=5))['Survived'].mean()
    df['Family'] = df['SibSp'] + df['Parch']
    family_survival_rate = df[df['Family'] > 0]['Survived'].mean()
    print("\nÜberlebensrate nach Altersgruppen:")
    print(survival_rate_by_age)
    print("\nÜberlebensrate von Familien:", family_survival_rate)

# 5. Textanalyse
def text_analysis(df):
    df['Title'] = df['Name'].str.extract(r',\s(\w+)\.')[0]
    title_survival = df.groupby('Title')['Survived'].mean()
    df['StartsBeforeM'] = df['Name'].apply(lambda x: x.split(',')[0][0].upper() < 'M')
    print("\nÜberlebensrate nach Titel:")
    print(title_survival)
    return df

# 6. Visualisierung
def create_visualizations(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Pclass', y='Survived', hue='Sex')
    plt.title('Überlebensrate nach Geschlecht und Klasse')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Age', hue='Survived', kde=False, bins=20)
    plt.title('Altersverteilung nach Überlebensstatus')
    plt.show()

# 7. Erstellen einer Vorhersagevariable
def create_prediction_rule(df):
    df['Prediction'] = df.apply(
        lambda row: 1 if (row['Sex'] == 'female' or (row['Pclass'] == 1 and row['Age'] < 18)) else 0,
        axis=1
    )
    print("\nVorhersagen basierend auf Regel erstellt.")
    return df

# Hauptablauf
if __name__ == "__main__":
    file_path = "train.csv"  # Anpassen an den tatsächlichen Dateipfad
    df = load_data(file_path)

    # Analysen durchführen
    basic_analysis(df)
    grouped_analysis(df)

    # Datenbereinigung
    df = clean_data(df)

    # Erweiterte Analyse
    advanced_analysis(df)

    # Textanalyse
    df = text_analysis(df)

    # Visualisierungen
    create_visualizations(df)

    # Vorhersagevariable erstellen
    df = create_prediction_rule(df)

    # Speichern der bearbeiteten Daten
    df.to_csv("titanic_cleaned.csv", index=False)
    print("\nBereinigte Daten wurden gespeichert.")

