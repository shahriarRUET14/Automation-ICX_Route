import pandas as pd

class parse_file:
    def __int__(self):
        print("Parse File Constructor")
    def read_plan(self,path):
        try:
            self.df_dg06 = pd.read_excel(path, 'DG06')
            self.df_dg10 = pd.read_excel(path, 'DG10')
        except Exception as e:
            print(e +"! Failed to read plan file")

        return self.df_dg06, self.df_dg10

