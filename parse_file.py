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
    def lst_fragment_parser(self, plan_df, plan_length, data, head, tail,post_verification):
        #= RT finding on block
        temp = data[head].split('"') #=First row contains RT in a quated part
        rt = temp[1]
        #=check if the  lst command is run successfully
        key =upper(str("RETCODE = 0  Operation succeeded").replace(" ",""))
        if  key in upper(str(data[head + 5]).replace(" ","")) : #= 5 for output patern follow so
            print("SuccessFully Runed lst Command for RT ",rt)
            try:
                row = plan_df[plan_df['RT'] == rt].index[0]
                # print(rt, " on plan file Row ",row )
            except Exception as e :
                print("! Processed Plan File Corrupted" , e )
                exit("! Processed Plan File Corrupted" , e)
                return False
            i = row

            first_row = True
            while i < plan_length and ( plan_df.loc[i,'Node'] != plan_df.loc[i,'Node'] or first_row):
                first_row = False
                #= getting Processed Plan File First row
                srt = plan_df.loc[i, 'SRT#']
                if not post_verification :
                    exist_srt = plan_df.loc[i, 'Existing SRT']
                    exist_percent = plan_df.loc[i, 'Existing %']
                else :
                    exist_srt = plan_df.loc[i, 'Proposed SRT']
                    exist_percent = plan_df.loc[i, 'Proposed %']


                if not self.srt_finder_txt(srt, exist_srt,exist_percent, data,head,tail) :
                    print("!Plan Vs Current Configuration not matched for " , rt)
                    #= Thus file is unmatched for a single attribute then no need to check for it  just sore RT and Go for next RT
                    # while plan_df.loc[i,'Node'] != plan_df.loc[i,'Node'] :
                    #     i = i+1 #if we want to store whole fragment
                    # print(srt, exist_srt,exist_percent)
                    if not post_verification:
                        cf.unmatched_rt.append(rt)
                    else :
                        cf.post_unmatched_rt.append(rt)
                    break;

                i = i+1
        else:
            print("!Error  not  Run lst Command for  " + rt)
            return False
        #checking if there is any unmatched fragment or not
        if len(cf.unmatched_rt) :
            return False

        return True

####################### Plan File Reader #########################
    def read_plan(self,path):
        #creating Emty Data Frame
        df_dg05 = df_dg06 = df_dg10 = df_cg11 = df_cg12 = pd.DataFrame()

        try:
            df_dg06 = pd.read_excel(path, 'DG06')
        except:
            print("! DG06 No Sheet Found plan file")
            pass
        else:
            print("!Okay  DG06 Sheet Found")
        try:
            df_dg10 = pd.read_excel(path, 'DG10')
        except:
            print("! DG10 No Sheet Found plan file")
            pass
        else:
            print("!Okay  DG10 Sheet Found")

        try:
            df_dg05 = pd.read_excel(path, 'DG05')
        except:
            print("! DG05 No Sheet Found plan file")
            pass
        else:
            print("!Okay  DG05 Sheet Found")

        try:
            df_cg11 = pd.read_excel(path, 'CG11')
        except:
            print("! CG11 No Sheet Found plan file")
            pass
        else:
            print("!Okay  CG11 Sheet Found")

        try:
            df_cg12 = pd.read_excel(path, 'CG12')
        except:
            print("! CG12 No Sheet Found plan file")
            pass
        else:
            print("!Okay  CG12 Sheet Found")

        return df_dg05,df_dg06, df_dg10, df_cg11,df_cg12

    def srt_founder(self, key, line ):
        print(key + line)


    #=LST output Divider
    def lst_output_processing(self,path,post_verification):
        file_rader = open(f"{path}", "r")
        data = file_rader.read().splitlines()
        rows =len(data)
        try:

            path = f"""{cf.process_file_path}{cf.f_n_plan_process}"""
            plan_df = pd.read_excel(path, 'All_Data')
            plan_length = len(plan_df)
        except Exception as e:
            print("!Failed Opening Processed Plan File  ", path)
            exit("XLSX File Corrupted Please check Processed File")
            return False
        first = 0
        last = 0
        i =0
        #=End Identifier
        key = upper(str("---    END").replace(" ", ""))
        while i < rows :
            if key in upper(str(data[i]).replace(" ","")) :
                last = i
                self.lst_fragment_parser(plan_df, plan_length, data, first, last, post_verification)  #go for find and break fragment on plan

                first = i+2
                i = i+1
            i = i+1
        return True

