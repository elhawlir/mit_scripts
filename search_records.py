from automated_email import df
import pandas as pd



class Search:

    def __init__(self):
        self.df = pd.DataFrame()

    def search_records(self, first_name, *args):

        columns = self.df.columns
        f_name = first_name

        # print(dataframe.query(f'`First Name` == "{first_name}"'))
    
        try:
            result = [self.df.query(f'`{i}` == "{f_name}"') for i in columns]
            print('hi')
            print(result)
        except EnvironmentError as e:
            print(e)


if __name__ == '__main__':
    s = Search()
    d_frame = s.df
    s.search_records(d_frame, 'Shoaib')