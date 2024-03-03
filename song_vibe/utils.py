def load_data(data_folder):
    data = pd.read_csv(f"{data_folder}/data.csv")
    data.rename(columns={"Song_name": "category", "Response": "text"}, inplace=True)
    df = pd.DataFrame(data, columns=["text", "category"])
    return df
