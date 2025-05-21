# Latest update: 2025-05-13

import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.build_your_df_features import init_df_data_analysis

current_file_path = os.path.abspath(__file__)
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(current_file_path))
PATH_OUTPUT = os.path.join('experiments', 'tests_data_visualization', 'tests_data')


# Latest update: 2025-05-13
# Design test functions
def test_init_df_data_analysis(): 
    df_data_analysis = init_df_data_analysis(haida=True, sanyi=False, small_town=False)
    df_data_analysis.to_csv(
        os.path.join(
            PROJECT_ROOT_PATH, PATH_OUTPUT, 'test_init_df_data_analysis.csv'
        ),
        index=False
    )
    print("The output file is saved in the following path:")
    print(os.path.join(PROJECT_ROOT_PATH, PATH_OUTPUT, 'test_init_df_data_analysis.csv'))

if __name__ == "__main__":
    test_init_df_data_analysis()

    print("\nTesting program runs successfully!")

