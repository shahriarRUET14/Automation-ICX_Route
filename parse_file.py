import pandas as pd
import xlsxwriter
import re

from numpy.core.defchararray import upper

import config as cf
import xlwt
from xlwt import Workbook
class parse_file:
    def __int__(self):
        #====== Writing Header of lst command output
        # cf.workbook.write_row(0, 1, cf.tergate_header)
        print("Parse File Constructor")
        # cf.lst_parsed_op_df = pd.DataFrame(columns=["firstname", "lastname"])
    #
    #
    # def __del__(self):
    #     # cf.workbook.close()
    #     print("lst parsed Xlsx Created")
    #     print('Destructor called')
    #     print(cf.lst_parsed_op_df)
    def to_uppercase(self,mystr):
        try:
            for idx, i in enumerate(mystr):
                if i.isalpha():
                    return ''.join(mystr[:idx] + mystr[idx:].capitalize())
        except:
            print("")
        return mystr

    def srt_finder_txt(self,srt,exist_srt,exist_percent, data,head,tail):
        exist_srt_match =False
        exist_percent_match =False

        i = head
        while i < tail :
            #= Matching Existing percentage
            exist_percent = int(exist_percent)
            key = f"""Percentage of {srt}  =  {exist_percent}"""
            if upper(str(key).replace(" ", "")) in upper(str(data[i]).replace(" ", "")) and exist_percent_match == False:
                exist_percent_match = True

            # = Matching Existing SRT Name
            key = f""" {srt}  =  {exist_srt}"""
            if upper(str(key).replace(" ", "")) in upper(str(data[i]).replace(" ", "")) and exist_srt_match  == False:
                exist_srt_match = True
            i = i + 1

        return exist_srt_match and exist_percent_match

    #=== Plan File Divider
    def lst_fragment_parser(self, plan_df, plan_length, data, head, tail):
        #= RT finding on block
        temp = data[head].split('"') #=First row contains RT in a quated part
        rt = temp[1]
        #=check if the  lst command is run successfully
        key =upper(str("RETCODE = 0  Operation succeeded").replace(" ",""))
        if  key in upper(str(data[head + 5]).replace(" ","")) : #= 5 for output patern follow so
            print("SuccessFully Runed lst Command for RT "+ rt)
            try:
                row = plan_df[plan_df['RT'] == rt].index[0]
                print(rt, " on plan file Row ",row )
            except Exception as e :
                print("! Processed Plan File Corrupted" + e )
                exit("! Processed Plan File Corrupted" + e)
                return False
            i = row

            first_row =True
            # print(plan_df.iloc[i:i+10])
            while i < plan_length and (plan_df.loc[i,'Node'] != plan_df.loc[i,'Node'] or first_row):
                first_row = False
                #= getting Processed Plan File First row
                srt = plan_df.loc[i, 'SRT#']
                exist_srt = plan_df.loc[i, 'Existing SRT']
                exist_percent = plan_df.loc[i, 'Existing %']
                # print(plan_df.loc[i, 'SRT#'])

                if not self.srt_finder_txt(srt, exist_srt,exist_percent, data,head,tail) :
                    print("!Plan Vs Current Configuration not matched for " , rt)
                    #= Thus file is unmatched for a single attribute then no need to check for it  just sore RT and Go for next RT
                    # while plan_df.loc[i,'Node'] != plan_df.loc[i,'Node'] :
                    #     i = i+1 #if we want to store whole fragment
                    cf.unmatched_rt.append(rt)
                    break

                i = i+1
        else:
            print("!Error  not  Run lst Command for  " + rt)
            return False

    def read_plan(self,path):
        try:
            self.df_dg06 = pd.read_excel(path, 'DG06')
            self.df_dg10 = pd.read_excel(path, 'DG10')
        except Exception as e:
            print(e +"! Failed to read plan file")

        return self.df_dg06, self.df_dg10
    def srt_founder(self, key, line ):
        print(key + line)


    #=LST output Divider
    def lst_output_processing(self,path):
        file_rader = open(f"{path}", "r")
        data = file_rader.read().splitlines()
        rows =len(data)
        try:

            path = f"""{cf.process_file_path}{cf.f_n_plan_process}"""
            plan_df = pd.read_excel(path, 'All_Data')
            plan_length = len(plan_df)
            # print("Plan Length ",plan_length)
            # print(plan_df.loc[plan_length-1,"Existing %"])
            print("Successful : Processed Plan File Read ")
        except Exception as e:
            print("!Failed Opening Processed Plan File  ", path)
        first = 0
        last = 0
        i =0
        #=End Identifier
        key = upper(str("---    END").replace(" ", ""))
        while i < rows :
            if key in upper(str(data[i]).replace(" ","")) :
                last = i
                print("Lst Output Separated")
                self.lst_fragment_parser(plan_df, plan_length, data, first, last)
                first = i+2
                i = i+1
            i = i+1

