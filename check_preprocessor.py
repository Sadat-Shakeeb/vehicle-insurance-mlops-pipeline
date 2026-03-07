import pickle
path = r"artifact\03_08_2026_02_14_11\data_transformation\transformed_object\preprocessing_object.pkl"
with open(path, "rb") as f:
    obj = pickle.load(f)
print(obj)
try:
    print("feature names", obj.get_feature_names_out())
except Exception as e:
    print("cannot extract feature names: ", e)
