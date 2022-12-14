import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import datasets, svm
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from math import sqrt
from csv import reader
from math import exp
from math import pi

def kmeans(filename, clusters, useColumns):

    df = pd.read_csv(filename, usecols=useColumns.split(','))

    kmeans = KMeans(n_clusters=int(clusters)).fit(df)
    centroids = kmeans.cluster_centers_
    print(centroids)

    x = np.array(df["Age"])
    y = np.array(df["Annual Income (k$)"])

    plt.scatter(x, y, c= kmeans.labels_, s=50, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    plt.show()
    inertias = []

    for i in range(1,11):
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(df)
        inertias.append(kmeans.inertia_)

    plt.plot(range(1,11), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(df)

    plt.scatter(x, y, c=kmeans.labels_)
    plt.show()
    
def knnNN(fileName, columns, point):

    df = pd.read_csv(fileName, usecols=columns.split(','))

    x = df[columns.split(',')[0]]
    y = df[columns.split(',')[1]]
    classes = df[columns.split(',')[2]]
    plt.scatter(x, y, c=classes)
    plt.show()

    data = list(zip(x, y))
    knn = KNeighborsClassifier(n_neighbors=1)

    knn.fit(data, classes)

    new_x = float(point.split(',')[0])
    new_y = float(point.split(',')[1])
    new_point = [(new_x, new_y)]
    prediction = knn.predict(new_point)
    print(prediction)

    plt.scatter(x + [new_x], y + [new_y], c=classes + [prediction[0]])
    plt.text(x=new_x-1.7, y=new_y-0.7, s=f"new point, class: {prediction[0]}")
    plt.show()

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(data, classes)
    prediction = knn.predict(new_point)
    print(prediction)

    plt.scatter(x + [new_x], y + [new_y], c=classes + [prediction[0]])
    plt.text(x=new_x-1.7, y=new_y-0.7, s=f"new point, class: {prediction[0]}")
    plt.show()

def randomForest():
    
    iris = datasets.load_iris()
    print(iris.target_names)
    print(iris.feature_names)
    print(iris.data[0:5])
    print(iris.target)

    data=pd.DataFrame({
    'sepal length':iris.data[:,0],
    'sepal width':iris.data[:,1],
    'petal length':iris.data[:,2],
    'petal width':iris.data[:,3],
    'species':iris.target
    })
    data.head()

    X=data[['sepal length', 'sepal width', 'petal length', 'petal width']]
    y=data['species']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    clf=RandomForestClassifier(n_estimators=100)
    clf.fit(X_train,y_train)

    y_pred=clf.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    clf.predict([[3, 5, 4, 2]])

    clf=RandomForestClassifier(n_estimators=100)
    clf.fit(X_train,y_train)

    RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False)
    
    feature_imp = pd.Series(clf.feature_importances_,index=iris.feature_names).sort_values(ascending=False)
    feature_imp

    sns.barplot(x=feature_imp, y=feature_imp.index)

    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title("Visualizing Important Features")
    plt.legend()
    plt.show()

    X=data[['petal length', 'petal width','sepal length']]
    y=data['species']                           
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=5) # 70% training and 30% test

    clf=RandomForestClassifier(n_estimators=100)


    clf.fit(X_train,y_train)


    y_pred=clf.predict(X_test)

    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

def dendrogramHC(fileName, columns):

    df = pd.read_csv(fileName, usecols=columns.split(','))

    x = df[columns.split(',')[0]]
    y = df[columns.split(',')[1]]

    data = list(zip(x,y))

    linkage_data = linkage(data, method='ward', metric='euclidean')
    dendrogram(linkage_data)

    plt.show()

    hierarchical_cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
    labels = hierarchical_cluster.fit_predict(data)

    plt.scatter(x, y, c=labels)
    plt.show()

def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
 
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
		print('[%s] => %d' % (value, i))
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup
 
def separate_by_class(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset[i]
		class_value = vector[-1]
		if (class_value not in separated):
			separated[class_value] = list()
		separated[class_value].append(vector)
	return separated
 
def mean(numbers):
	return sum(numbers)/float(len(numbers))
 
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
	return sqrt(variance)
 
def summarize_dataset(dataset):
	summaries = [(mean(column), stdev(column), len(column)) for column in zip(*dataset)]
	del(summaries[-1])
	return summaries
 
def summarize_by_class(dataset):
	separated = separate_by_class(dataset)
	summaries = dict()
	for class_value, rows in separated.items():
		summaries[class_value] = summarize_dataset(rows)
	return summaries
 
def calculate_probability(x, mean, stdev):
	exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))
	return (1 / (sqrt(2 * pi) * stdev)) * exponent
 
def calculate_class_probabilities(summaries, row):
	total_rows = sum([summaries[label][0][2] for label in summaries])
	probabilities = dict()
	for class_value, class_summaries in summaries.items():
		probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
		for i in range(len(class_summaries)):
			mean, stdev, _ = class_summaries[i]
			probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
	return probabilities
 
def predict(summaries, row):
	probabilities = calculate_class_probabilities(summaries, row)
	best_label, best_prob = None, -1
	for class_value, probability in probabilities.items():
		if best_label is None or probability > best_prob:
			best_prob = probability
			best_label = class_value
	return best_label

def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

def naiveBayes(fileName):
    dataset = load_csv(fileName)
    for i in range(len(dataset[0])-1):
        str_column_to_float(dataset, i)

    str_column_to_int(dataset, len(dataset[0])-1)

    model = summarize_by_class(dataset)

    row = [5.7,2.9,4.2,1.3]

    label = predict(model, row)
    print('Data=%s, Predicted: %s' % (row, label))

def svmAlg(fileName):

    df = pd.read_csv(fileName)
    cancer = datasets.load_breast_cancer()

    print("Features: ", cancer.feature_names)
    print("Labels: ", cancer.target_names)


    X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, test_size=0.3,random_state=109)

    clf = svm.SVC(kernel='linear')

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    print("Precision:",metrics.precision_score(y_test, y_pred))
    print("Recall:",metrics.recall_score(y_test, y_pred))
