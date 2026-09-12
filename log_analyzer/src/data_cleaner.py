import pandas as pd

def create_dataframe(parsed_logs):
    df = pd.DataFrame(parsed_logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"],format="%d/%b/%Y:%H:%M:%S %z")
    df = df.set_index("timestamp")

    return df
