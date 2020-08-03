import pandas as pd

decision = {
    "Regular Decision": "Regular",
    "Early Decision 1": "ED1",
    "Early Decision 2": "ED2",
}

reasons_columns = [
    "Transfer Reason 1",
    "Transfer Reason 2",
    "Transfer Reason 3",
    "Transfer Reason 4",
    "Transfer Reason 5",
]

stayed = [
    "Internally Transferred",
    "Active and enrolled in SP21",
    "Leave of Absence",
    "Graduated",
]

left = ["Discontinued"]


def get_count_series(df):
    return df.iloc[:, 10].value_counts(dropna=True)


def get_country_series(df):
    return df.iloc[:, 11].value_counts(ascending=False)


def get_admissions_type_series(df):
    return df.iloc[:, 7].value_counts(dropna=True)


def get_school_series(df):
    return pd.Series(df.iloc[:, 29:].values.flatten()).value_counts(ascending=False)


def get_census_status_series(df):
    return df.iloc[:, 9].value_counts(dropna=True)


def get_number_stayed_at_nyu(df):
    remained_nyu = 0
    census_series = get_census_status_series(df)
    for category in stayed:
        remained_nyu += census_series.get(category, 0)
    return remained_nyu


def get_number_stayed_at_cas(df):
    census_series = get_census_status_series(df)
    return (
        census_series.get("Active and enrolled in SP21", 0)
        + census_series.get("Leave of Absence", 0)
        + census_series.get("Graduated", 0)
    )


def get_met_dataframe(df):
    return df.loc[df.iloc[:, 20] == "Yes"]


def get_not_met_dataframe(df):
    return df.loc[df.iloc[:, 20] == "No"]


def get_transfer_reasons_series(df):
    return pd.Series(df.iloc[:, 21:26].values.flatten()).value_counts()


def get_domestic_dataframe(df):
    return df.loc[df.iloc[:, 10] == "No"]


def get_international_dataframe(df):
    return df.loc[df.iloc[:, 10] == "Yes"]


def get_stayed_at_nyu_dataframe(df):
    return df[df.iloc[:, 9].isin(stayed)]


def get_left_nyu_dataframe(df):
    return df[df.iloc[:, 9].isin(left)]
