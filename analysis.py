import pandas as pd
import AnalyzeModule


# 1 Student Number Breakdown (a for total b for met)
# need total number, domestic number and international number
# 2 Country Breakdown ( a b )
# 3 Admissions Breakdown (a b)
# 4 School Breakdown (a b)
# 5 Census Breakdown (a b)
# 6 Reasons ( a total b domestic c international)
# 7 indcated codes ( a stayed b left)
# 8 census and meeting analysis (a met b not met)


def analyze(file):
    output_data = {}
    try:
        df = pd.read_csv(file)
        met_df = AnalyzeModule.get_met_dataframe(df)
        not_met_df = AnalyzeModule.get_not_met_dataframe(df)

        output_data["1"] = {}
        output_data["2"] = {}
        output_data["3"] = {}
        output_data["4"] = {}
        output_data["5"] = {}
        output_data["6"] = {}
        output_data["7"] = {}
        output_data["8"] = {}

        output_data["1"]["a"] = {
            "total": len(df),
            "domestic": AnalyzeModule.get_count_series(df).get("No", 0),
            "international": AnalyzeModule.get_count_series(df).get("Yes", 0),
        }
        output_data["1"]["b"] = {
            "total": len(met_df),
            "domestic": AnalyzeModule.get_count_series(met_df).get("No", 0),
            "international": AnalyzeModule.get_count_series(met_df).get("Yes", 0),
        }

        output_data["2"]["a"] = AnalyzeModule.get_country_series(
            AnalyzeModule.get_international_dataframe(df)
        ).to_dict()
        output_data["2"]["b"] = AnalyzeModule.get_country_series(
            AnalyzeModule.get_international_dataframe(met_df)
        ).to_dict()

        output_data["3"]["a"] = AnalyzeModule.get_admissions_type_series(df).to_dict()
        output_data["3"]["b"] = AnalyzeModule.get_admissions_type_series(met_df).to_dict()

        output_data["4"]["a"] = AnalyzeModule.get_school_series(df).to_dict()
        output_data["4"]["b"] = AnalyzeModule.get_school_series(met_df).to_dict()

        output_data["5"]["a"] = {
            "nyu": AnalyzeModule.get_number_stayed_at_nyu(df),
            "cas": AnalyzeModule.get_number_stayed_at_cas(df),
            "internal": AnalyzeModule.get_number_stayed_at_nyu(df)
            - AnalyzeModule.get_number_stayed_at_cas(df),
            "left": len(AnalyzeModule.get_left_nyu_dataframe(df)),
        }
        output_data["5"]["b"] = {
            "nyu": AnalyzeModule.get_number_stayed_at_nyu(met_df),
            "cas": AnalyzeModule.get_number_stayed_at_cas(met_df),
            "internal": AnalyzeModule.get_number_stayed_at_nyu(met_df)
            - AnalyzeModule.get_number_stayed_at_cas(met_df),
            "left": len(AnalyzeModule.get_left_nyu_dataframe(met_df)),
        }

        output_data["6"]["a"] = AnalyzeModule.get_transfer_reasons_series(met_df).to_dict()
        output_data["6"]["b"] = AnalyzeModule.get_transfer_reasons_series(
            AnalyzeModule.get_domestic_dataframe(met_df)
        ).to_dict()
        output_data["6"]["c"] = AnalyzeModule.get_transfer_reasons_series(
            AnalyzeModule.get_international_dataframe(met_df)
        ).to_dict()

        output_data["7"]["a"] = AnalyzeModule.get_transfer_reasons_series(
            AnalyzeModule.get_stayed_at_nyu_dataframe(df)
        ).to_dict()

        output_data["7"]["b"] = AnalyzeModule.get_transfer_reasons_series(
            AnalyzeModule.get_left_nyu_dataframe(df)
        ).to_dict()
        output_data["8"]["a"] = {
            "left": len(AnalyzeModule.get_left_nyu_dataframe(met_df)),
            "stayed": len(AnalyzeModule.get_stayed_at_nyu_dataframe(met_df)),
        }

        output_data["8"]["b"] = {
            "left": len(AnalyzeModule.get_left_nyu_dataframe(not_met_df)),
            "stayed": len(AnalyzeModule.get_stayed_at_nyu_dataframe(not_met_df)),
        }
    except Exception as e:
        print(e)
        return -1

    return output_data
