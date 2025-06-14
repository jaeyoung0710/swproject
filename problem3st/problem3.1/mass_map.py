import pandas as pd

def read_and_display_csv(file_path):
    return pd.read_csv(file_path)


def merge_struct_with_category(struct_df, category_df):
    return pd.merge(struct_df, category_df,
                    left_on='category', right_on='category',
                    how='left')


def merge_all_data(map_df, struct_df, category_df):
    struct_with_names = merge_struct_with_category(struct_df, category_df)
    return pd.merge(map_df, struct_with_names,
                    on=['x', 'y'],
                    how='left')


def filter_area_1(df):
    return df[df['area'] == 1]


def main():
    area_map_df = read_and_display_csv(r'C:\swproject\swproject\problem3st\problem3.1\3-1-area_map.csv')
    print('=== Area Map ===')
    print(area_map_df)

    area_struct_df = read_and_display_csv(r'C:\swproject\swproject\problem3st\problem3.1\3-1-area_struct.csv')
    print('\n=== Area Structure ===')
    print(area_struct_df)

    struct_category_df = read_and_display_csv(r'C:\swproject\swproject\problem3st\problem3.1\3-1-area_category.csv')
    print('\n=== Structure Category ===')
    print(struct_category_df)

    struct_with_names_df = merge_struct_with_category(area_struct_df, struct_category_df)
    print('\n=== Structure with Category Names ===')
    print(struct_with_names_df)

    full_data_df = merge_all_data(area_map_df, area_struct_df, struct_category_df)
    print('\n=== Merged Full Data ===')
    print(full_data_df)

    area_1_df = filter_area_1(full_data_df)
    print('\n=== Filtered Area 1 Data ===')
    print(area_1_df)


if __name__ == '__main__':
    main()
