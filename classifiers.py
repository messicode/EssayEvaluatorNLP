import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score

def classify(essay_details):
    # Separate essays into high and low grades
    high_grade_essays = [details for details in essay_details.values() if details['grade'] == 'high']
    low_grade_essays = [details for details in essay_details.values() if details['grade'] == 'low']

    # Split high grade essays into training and test sets
    X_train_high, X_test_high = train_test_split(high_grade_essays, test_size=0.2, random_state=42)

    # Split low grade essays into training and test sets
    X_train_low, X_test_low = train_test_split(low_grade_essays, test_size=0.2, random_state=42)

    # Combine training and test sets for high and low grade essays
    X_train = X_train_high + X_train_low
    X_tests = X_test_high + X_test_low

    # Separate features and labels to get final train and test sets
    X = np.array([[details['l'], details['e'], details['csim']] for details in X_train])
    y = np.array([details['grade'] for details in X_train])
    X_test = np.array([[details['l'], details['e'], details['csim']] for details in X_tests])
    y_test = np.array([details['grade'] for details in X_tests])
    # print(y)
    # print(y_test)
    # print(np.unique(y_test))

    # Convert labels to binary
    y = np.where(y == 'high', 1, 0)
    y_test = np.where(y_test == 'high', 1, 0)


    # Logistic Regression
    log_reg_clf = LogisticRegression(random_state=42)
    log_reg_clf.fit(X, y)
    log_reg_predictions = log_reg_clf.predict(X_test)
    log_reg_accuracy = f1_score(y_test, log_reg_predictions,labels=['high', 'low'])

    # Multilayer perceptron
    mlp_clf = MLPClassifier(max_iter=10000,random_state=42)
    mlp_clf.fit(X, y)
    mlp_predictions = mlp_clf.predict(X_test)
    # print(f"------predddssss{mlp_predictions}")
    mlp_accuracy = f1_score(y_test, mlp_predictions, labels=['high', 'low'])



    return mlp_accuracy,log_reg_accuracy
#
# essay_details = {
#     1: {"prompt":"jh", "grade":"low","l":10,"e":15,"csim":.78},
#     2: {"prompt": "ja", "grade": "low", "l": 14, "e": 20, "csim": .5},
#     3: {"prompt": "eew", "grade": "low", "l": 25, "e": 19, "csim": .6},
#     4: {"prompt": "jtrth", "grade": "low", "l": 19, "e": 6, "csim": .1},
#     5: {"prompt": "ytyjh", "grade": "low", "l": 20, "e": 25, "csim": .8},
#     6: {"prompt": "jjh", "grade": "high", "l": 40, "e": 15, "csim": .8},
#     7: {"prompt": "jghh", "grade": "high", "l": 50, "e": 6, "csim": .78},
#     8: {"prompt": "jhds", "grade": "high", "l": 20, "e": 6, "csim": .89},
#     9: {"prompt": "jhsa", "grade": "high", "l": 30, "e": 8, "csim": .2},
#     10: {"prompt": "hfdghrjh", "grade": "high", "l": 80, "e": 5, "csim": .9},
# }
#
# v1,v2=classify(essay_details)
# print(v1)
# print(v2)
