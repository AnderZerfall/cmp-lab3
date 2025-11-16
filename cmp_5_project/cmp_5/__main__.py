from models.DataManager import DataManager

FILE_PATH = "cmp_5/dataset/cancer_patient.csv"

def run_model():
    data_manager = DataManager(FILE_PATH)
    
    print("\n ============ 🧼 Cleaning info ============ \n" )
    data_manager.clean()
    
    print("\n ============ ℹ️ Data Frame Info ============ \n" )
    data_manager.get_info()
    
    print("\n ============ ⏰ Encoding ... ============ \n" )
    data_manager.encode_categories()
    
    print("\n ============ 🖌️ Plot Scatter Matrix ============ \n" )
    data_manager.plot_scatter_matrix()
    
    print("\n ============ 📈 Build Data Model (Unscaled) ============ \n" )
    data_manager.divide_data()
    data_manager.build_classificator()
    print("\n ============ 🚨 Data Model Results (Unscaled) ============ \n" )
    data_manager.analyze_classificator_results()
    
    print("\n ============ 📈 Build Data Model (Scaled ➕) ============ \n" )
    data_manager.divide_data(scale = True)
    data_manager.build_classificator()
    print("\n ============ 🚨 Data Model Results (Scaled ➕) ============ \n" )
    data_manager.analyze_classificator_results()
    
    
    print("\n ============ 🔥 Find Best Model (KNN 🙍 vs Random🌲) ============ \n" )
    data_manager.find_best_method()
    
    print("\n ============ 🙍 Check how KNN works ============ \n" )
    data_manager.test_k_neigbor_method()



def main() -> None:
    print("Start coding in Python today!")
    run_model()


if __name__ == "__main__":
    main()
