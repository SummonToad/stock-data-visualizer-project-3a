import pandas as pd


class DataError(Exception):
    pass


def build_dataframe(raw):
    key = next((k for k in raw if "Time Series" in k), None)
    if key is None:
        raise DataError("No time series data found in the API response.")

    df = pd.DataFrame.from_dict(raw[key], orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.columns = [c.split(". ", 1)[-1] for c in df.columns]
    return df[["open", "high", "low", "close"]].astype(float)


def filter_by_date(df, start_date, end_date):
    filtered = df.loc[pd.Timestamp(start_date):pd.Timestamp(end_date)]
    if filtered.empty:
        raise DataError(
            f"No data between {start_date} and {end_date}. "
            f"Available range: {df.index.min().date()} to {df.index.max().date()}."
        )
    return filtered
