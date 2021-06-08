import pandas as pd

from tkinter import filedialog

load_features_file = filedialog.askopenfilename()
df = pd.read_excel(load_features_file)
df = pd.DataFrame(df)
total_cols = len(df.columns)
print(total_cols)
