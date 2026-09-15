import pandas as pd

def create_dataframe(parsed_logs):
    if not parsed_logs:
        return pd.DataFrame()
    df = pd.DataFrame(parsed_logs)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%d/%b/%Y:%H:%M:%S %z"
    )

    return df
def clean_data(df):
    if df.empty:
        return df
    df = df.dropna()
    return df
