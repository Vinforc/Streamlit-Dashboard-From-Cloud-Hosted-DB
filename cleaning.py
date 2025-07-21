# utils/cleaning.py

def standardize_column_names(df):
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df

def deduplicate(df, subset=None):
    return df.drop_duplicates(subset=subset)

def clean_emails(df, column="email"):
    if column in df.columns:
        df[column] = df[column].str.strip().str.lower()
    return df

def remove_null_ids(df, id_col="id"):
    return df[df[id_col].notnull()]
