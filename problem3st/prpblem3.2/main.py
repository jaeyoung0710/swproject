import pandas as pd
import matplotlib.pyplot as plt


def load_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df


def filter_general_household(df):
    filtered_cols = [col for col in df.columns if '일반가구원' in col or col == '시점']
    return df[filtered_cols]


def filter_since_2015(df):
    df = df[df['시점'] >= 2015]
    return df


def separate_gender_age_data(df):
    years = df['시점']
    gender_cols = [col for col in df.columns if '남자' in col or '여자' in col]
    age_cols = [col for col in df.columns if '세 일반가구원' in col and '남자' not in col and '여자' not in col]

    gender_data = df[['시점'] + gender_cols]
    age_data = df[['시점'] + age_cols]

    return years, gender_data, age_data


def plot_age_trend(years, age_data):
    plt.figure(figsize=(10, 6))
    for col in age_data.columns[1:]:
        plt.plot(years, age_data[col], marker='o', label=col)

    plt.title('2015년 이후 연령별 일반가구원 통계')
    plt.xlabel('연도')
    plt.ylabel('가구원 수')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    file_path = 'C:\swproject\swproject\problem3st\prpblem3.2\kosis_household.csv'

    df = load_data(file_path)
    df = filter_general_household(df)
    df = filter_since_2015(df)
    years, gender_data, age_data = separate_gender_age_data(df)

    print('\n[남녀 연도별 일반가구원]')
    print(gender_data.to_string(index=False))

    print('\n[연령별 연도별 일반가구원]')
    print(age_data.to_string(index=False))

    plot_age_trend(years, age_data)


if __name__ == '__main__':
    main()
