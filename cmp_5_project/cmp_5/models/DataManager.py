import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.ensemble import  RandomForestClassifier
from sklearn.metrics import  confusion_matrix, classification_report, ConfusionMatrixDisplay, silhouette_score, davies_bouldin_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans
from tabulate import tabulate
from collections import Counter
import numpy as np

LABEL_CLASS = "Level"
NEIGHBORS = 3
CLASSES = 3
CORRELATION_THRESHOLD=0.5

class DataManager:
    def __init__(self, file):
        self.data_frame =  pd.read_csv(file)
        self.train_characteristics = None
        self.train_classes = None
        self.test_characteristics = None
        self.test_classes = None
        self.classificator = None
        self.clusterer = None
    
    def clean(self):
        self.data_frame = self.data_frame.drop(columns=["index", "Patient Id"], errors='ignore')
        
        missing_values = self.data_frame.isnull()
        duplicated_values = self.data_frame.duplicated()
        missing_rows = self.data_frame[missing_values.any(axis=1)]
        
        self.data_frame = self.data_frame.dropna()
        self.data_frame = self.data_frame.drop_duplicates()
        
        print("\n ❌ Missing values: ", missing_rows.shape[0])
        print("\n ⚠️ Duplicated values: ", duplicated_values.sum())
        print("\n ✅ Reports Amount: ", self.data_frame.shape[0])
        
        print("\n 🔍 Analyzing feature importance...")
        
        label_mapping = {"Low": 0, "Medium": 1, "High": 2}
        encoded_labels = self.data_frame[LABEL_CLASS].map(label_mapping)
        
        feature_cols = [col for col in self.data_frame.columns if col != LABEL_CLASS]
        
        correlations = {}
        for col in feature_cols:
            corr = self.data_frame[col].corr(encoded_labels)
            correlations[col] = abs(corr)
        
        sorted_corr = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
        
        features_to_keep = [col for col, corr in sorted_corr if corr >= CORRELATION_THRESHOLD]
        features_to_remove = [col for col, corr in sorted_corr if corr < CORRELATION_THRESHOLD]
        
        print(f"\n 📊 Top correlated features:")
        for col, corr in sorted_corr[:10]:
            print(f"   {col}: {corr:.4f}")
        
        print(f"\n 🗑️  Removing {len(features_to_remove)} low-correlation features:")
        for col in features_to_remove:
            print(f"   - {col} (corr: {correlations[col]:.4f})")
        
        self.data_frame = self.data_frame[features_to_keep + [LABEL_CLASS]]
        
        print(f"\n ✅ Kept {len(features_to_keep)} features")
        print(f" 📏 Final dataset shape: {self.data_frame.shape}")
    
    def get_info(self):
        rows, columns = self.data_frame.shape
        
        classes_amount = self.data_frame.groupby(LABEL_CLASS).size()
        classes_proportion = classes_amount / len(self.data_frame)
        
        
        print("\n 📊 Stats info: ======================= \n")
        print(self.data_frame.describe())
        print("\n  ====================================== \n")
        
        print("\n 📝 Amount of reports: ", rows)
        print("\n ✨ Amount of characteristics: ", columns)
        print("\n 📚 Characteristic types: ================= \n ")
        print(self.data_frame.dtypes)
        print("\n  ====================================== \n")
        print("\n 🏷️ Label column: ", LABEL_CLASS)
        print("\n % Classes proportions: ================= \n")
        print(classes_proportion * 100)
        print("\n  ====================================== \n")
        print("\n 📋 Notes under the classes: ================= \n")
        print(classes_amount)
        print("\n  ====================================== \n")
    
    def encode_categories(self):
        cat_cols = self.data_frame.select_dtypes(include=["object", "category"]).columns.tolist()
        
        if LABEL_CLASS in cat_cols:
            cat_cols.remove(LABEL_CLASS)

        
        if len(cat_cols) == 0:
            print("\n ✅ Done ======================= \n")
            return
        
        self.data_frame = pd.get_dummies(self.data_frame, columns=cat_cols, drop_first=True)
        print("\n 💻 Encoded frame: ======================= \n", self.data_frame)
        print("\n  ====================================== \n")
    
    def plot_scatter_matrix(self):
        color_wheel = {
            "High": "red",
            "Medium": "yellow",
            "Low": "green"
        }
        
        colors = self.data_frame[LABEL_CLASS].map(lambda x: color_wheel.get(x))
        axes = scatter_matrix(self.data_frame, color=colors, alpha=0.6, 
                         diagonal='hist', figsize=(16, 16))
        for ax in axes.flatten():
            ax.xaxis.label.set_rotation(45)
            ax.yaxis.label.set_rotation(45)
            ax.xaxis.label.set_ha('right')
            ax.yaxis.label.set_ha('right')
        print("\n ✅ Done ======================= \n")
        plt.tight_layout()
        plt.show()
    
    def divide_data(self, scale = False):
        characteristics = self.data_frame.drop(columns=[LABEL_CLASS, 'index', 'Patient Id'], errors='ignore')
        classes = self.data_frame[LABEL_CLASS]
        
        
        if scale: 
            scaler = MinMaxScaler()
            characteristics = scaler.fit_transform(characteristics)

        self.train_characteristics, self.test_characteristics, self.train_classes, self.test_classes = train_test_split(
            characteristics, classes, test_size=0.2
            )
        
        
        print("\n 💪 Train Data Set: ======================= \n")
        print(self.train_characteristics)
        print("\n  ====================================== \n")
        
        print("\n 👟 Test Data Set: ======================= \n")
        print(self.test_characteristics)
        print("\n  ====================================== \n")
    
    def build_classificator(self, neighbors = NEIGHBORS):
        self.classificator = KNeighborsClassifier(n_neighbors=neighbors, metric='euclidean')
        self.classificator.fit(self.train_characteristics, self.train_classes)
    
    def analyze_classificator_results(self):
        test_predict = self.classificator.predict(self.test_characteristics)
        
        score = self.classificator.score(self.test_characteristics, self.test_classes)
        
        report = classification_report(self.test_classes, test_predict)
        
        print("\n 🏆 Overall score: ", score)
        print("\n 🚩 Report: ======================= \n")
        print(report)
        print("\n  ====================================== \n")
        
        cm = confusion_matrix(self.test_classes, test_predict)
        cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=self.classificator.classes_)
        cm_display.plot()
        print("\n ✅ Done ======================= \n")
        plt.show()
    
    def find_best_method(self):
        self.divide_data(scale = True)
        
        
        self.classificator = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
        self.classificator.fit(self.train_characteristics, self.train_classes)
        
        test_predict = self.classificator.predict(self.test_characteristics)
        report_neighbors = classification_report(self.test_classes, test_predict,  output_dict=True)
        
        
        
        self.classificator = RandomForestClassifier(random_state=0)
        self.classificator.fit(self.train_characteristics, self.train_classes)
        
        test_predict = self.classificator.predict(self.test_characteristics)
        report_random_forest = classification_report(self.test_classes, test_predict, output_dict=True)
        
        knn_score = report_neighbors['weighted avg']['f1-score'];
        random_forest_score = report_random_forest['weighted avg']['f1-score']
        
        
        print("\n 🏅 Result: ======================= \n")
        print("\n - KNN F1: ", knn_score)
        print("\n - Random forest F1: ", random_forest_score)
        
        
        if knn_score > random_forest_score:
            print('\n ⭐ KNN is better! \n')
        else:
            print('\n ⭐ Random Forest is better! \n')
        
        print("\n  ====================================== \n")
    
    def get_euclidean_distance(self, p, q):
        return np.sqrt(np.sum(p - q) ** 2)

    def test_k_neigbor_method(self):
        obj_idxs = []
        
        for cls in self.data_frame[LABEL_CLASS].unique():
            obj_idxs.extend(np.where(self.test_classes == cls)[0][:3])
        
        for index in obj_idxs:
            test_object = self.test_characteristics[index]
            test_label = self.test_classes.iloc[index]
            
            distance = np.array([self.get_euclidean_distance(test_object, train_object) for train_object in self.train_characteristics])
            
            nearest_distance_index = np.argmin(distance)
            nearest_label = self.train_classes.iloc[nearest_distance_index]
            
            print("\n  ====================================== \n")
            print("\n 💯 True label: ", test_label)
            print("\n 💡 Nearest label: ", nearest_label)
            print("\n 🚀 Distance: ", nearest_distance_index)
            print("\n  ====================================== \n")
    
    def build_cluster(self, clusters = CLASSES, scale = None):
        standard_scaler = StandardScaler()
        min_max_scaler = MinMaxScaler()
        data = data = self.data_frame.drop(columns=['index', 'Patient Id', LABEL_CLASS, "cluster"], errors='ignore').values
        
        
        if scale == "standard":
            data = standard_scaler.fit_transform(data)
        elif scale == "min/max":
            data = min_max_scaler.fit_transform(data)
        
        self.clusterer = KMeans(n_clusters = clusters)
        self.clusterer.fit(data)
        
        return data
    
    def analyze_cluster_results(self, data):
        predictions = self.clusterer.predict(data)
        self.data_frame["cluster"] = predictions;
        count = Counter(self.clusterer.labels_)
        
        cluster_content = self.data_frame.groupby(["cluster", LABEL_CLASS]).size().unstack(fill_value=0)
        cluster_content["Total"] = cluster_content.sum(axis=1)
        cluster_content.loc["Total"] = cluster_content.sum()
        
        print("\n  🗓️ Data Frame ======================== \n")
        print(self.data_frame)
        print("\n  ====================================== \n")
        
        
        print("\n  Clusters =========================== \n")
        print("\n  🧮 Cluster counts: ", count)
        print("\n")
        print(tabulate(cluster_content, headers="keys", tablefmt="psql"))
        print("\n  ====================================== \n")
        
        centroids = self.clusterer.cluster_centers_
        
        print("\n  ❌ Centroids: =========================== \n")
        print(centroids)
        print("\n  ====================================== \n")
        
        feature_pairs = [(0, 1),
                        (2, 3),
                        (4, 5),
                        (6, 7),
                        (8, 9),
                        (10, 11)]
        
        
        fig, ax = plt.subplots(2, 3, figsize=(12,10))
        axes = ax.flatten()

        for i, (x, y) in enumerate(feature_pairs):
            ax_ = axes[i]
            scatter1 = ax_.scatter(data[:, x], data[:, y], c=predictions, s=15, cmap='viridis')
            handles, labels = scatter1.legend_elements()
                
            legend1 = ax_.legend(handles, labels, loc="upper right")
            ax_.add_artist(legend1)
                
            ax_.scatter(centroids[:, x], centroids[:, y], marker='X', c='red', s=200, linewidths=3, label='centroids')
            ax_.legend(loc='lower right')
            ax_.set_xlabel(f"{self.data_frame.columns[x]}")
            ax_.set_ylabel(f"{self.data_frame.columns[y]}")
            
        plt.tight_layout()
        plt.show()
    
    def find_optimal_cluster_amount(self):
        
        results = []
        
        for k in range(2, 10):
            data = self.build_cluster(clusters=k)
            
            labels = self.clusterer.fit_predict(data)
            
            inertia_score = self.clusterer.inertia_
            sil_score = silhouette_score(data, labels)
            davies_score = davies_bouldin_score(data, labels)
            
            results.append([k, inertia_score, sil_score, davies_score])

        df_results = pd.DataFrame(results, columns=["Clusters", "Intertia Score", "Silhoutte Score", "Davies Score"])
        
        print(df_results)
        
        plt.figure(figsize=(10, 6))
        plt.title('Clustering Evaluation Scores vs. Number of Clusters')
        plt.legend(title='ntertia Score')
        plt.xlabel('Number of Clusters ($k$)')
        plt.ylabel('Score Value')
        plt.xticks(df_results["Clusters"])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.plot(df_results["Clusters"], df_results["Intertia Score"], marker='o', label='Inertia Score (Lower is better)')
        plt.show()
        plt.xlabel('Number of Clusters ($k$)')
        plt.ylabel('Score Value')
        plt.xticks(df_results["Clusters"])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(title='Silhoutte Score', loc='best')
        plt.title('Clustering Evaluation Scores vs. Number of Clusters')
        plt.plot(df_results["Clusters"], df_results["Silhoutte Score"], marker='x', label='Silhouette Score (Higher is better)')
        plt.show()
        plt.xlabel('Number of Clusters ($k$)')
        plt.ylabel('Score Value')
        plt.xticks(df_results["Clusters"])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(title='Davies Score', loc='best')
        plt.title('Clustering Evaluation Scores vs. Number of Clusters')
        plt.plot(df_results["Clusters"], df_results["Davies Score"], marker='s', label='Davies-Bouldin Score (Lower is better)')
        plt.show()