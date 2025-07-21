# tests/test_cleaning.py

import unittest
import pandas as pd
from utils.cleaning import standardize_column_names, deduplicate, clean_emails, remove_null_ids

class TestCleaningFunctions(unittest.TestCase):

    def test_standardize_column_names(self):
        df = pd.DataFrame(columns=["Name ", " Email"])
        df_clean = standardize_column_names(df)
        self.assertEqual(list(df_clean.columns), ["name", "email"])

    def test_deduplicate(self):
        df = pd.DataFrame({"email": ["a@example.com", "a@example.com"]})
        df_clean = deduplicate(df, subset=["email"])
        self.assertEqual(len(df_clean), 1)

    def test_clean_emails(self):
        df = pd.DataFrame({"email": [" A@EXAMPLE.COM "]})
        df_clean = clean_emails(df)
        self.assertEqual(df_clean["email"].iloc[0], "a@example.com")

    def test_remove_null_ids(self):
        df = pd.DataFrame({"id": [1, None, 3]})
        df_clean = remove_null_ids(df, id_col="id")
        self.assertEqual(len(df_clean), 2)

if __name__ == "__main__":
    unittest.main()
