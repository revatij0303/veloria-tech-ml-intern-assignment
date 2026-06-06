
# Cricket Match Winner Prediction
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

df = pd.read_csv("matches.csv")

df = df[['team1', 'team2', 'venue', 'toss_winner', 'winner', 'date']]
df.dropna(inplace=True)

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')


# 1. Team Strength (win count proxy)
win_counts = df['winner'].value_counts()

df['team1_strength'] = df['team1'].map(win_counts)
df['team2_strength'] = df['team2'].map(win_counts)


# 2. Home Advantage (approximation)
df['home_advantage'] = (df['team1'] == df['venue']).astype(int)


# 3. Head-to-Head Strength (approx)
df['matchup'] = df['team1'] + "_vs_" + df['team2']

h2h_wins = df.groupby('matchup')['winner'].transform('count')
df['h2h_strength'] = h2h_wins


# 4. Recent Form (last 5 matches approximation)
df['team1_form'] = df.groupby('team1')['winner'].transform(
    lambda x: x.eq(x.iloc[-1]).rolling(5, min_periods=1).mean()
)

df['team2_form'] = df.groupby('team2')['winner'].transform(
    lambda x: x.eq(x.iloc[-1]).rolling(5, min_periods=1).mean()
)

features = [
    'team1_strength',
    'team2_strength',
    'home_advantage',
    'h2h_strength',
    'team1_form',
    'team2_form'
]

X = df[features]
y = df['winner']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


print("\n===== MODEL EVALUATION =====")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred, average='weighted'))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


def predict_match(team1_strength, team2_strength, home_advantage, h2h_strength, team1_form, team2_form):
    prediction = model.predict([[team1_strength, team2_strength, home_advantage,
                                h2h_strength, team1_form, team2_form]])
    return prediction[0]
