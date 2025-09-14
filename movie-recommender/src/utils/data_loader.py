def load_movie_data(file_path):
    import pandas as pd

    # Film verilerini yükle
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(data):
    # Veriyi ön işleme tabi tut
    # Örneğin, eksik değerleri doldurma veya gereksiz sütunları kaldırma
    data = data.dropna()
    return data

def get_movie_titles(data):
    # Film başlıklarını al
    return data['title'].tolist() if 'title' in data.columns else []