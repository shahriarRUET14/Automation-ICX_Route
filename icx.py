import pandas as pd
import config
import numpy as np
import pandas as pd

from icx_script import icx_script

class icx:
    def __init__(self):
        print("Constractor")
        icx_script_obj = icx_script()

    def __del__(self):

        print('Destructor called, File Closed')


    def prepare_lst_script(self,last_code, fragment,head,tail) :
        i =head
        config.plan_df = config.plan_df.append(fragment)
        while i < tail -1:
            #step 2
            #point 1 Generating script and
            # if fragment.loc[i, 'Existing %'].astype(float) == fragment.loc[i, 'Proposed %'].astype(float) :
            lst_script = f"""LST RT:RN="{fragment.loc[head, 'RT']}",SSR=YES,SRA=YES,SOFC=YES,SPFX=YES,QR=LOCAL;{{{last_code}}}\n"""
            ##Saving the fragment
            print(lst_script)
            file_writer = open(f"{config.script_path}{config.f_n_lst_script}", "a")
            file_writer.write(lst_script)
            break
            # else:
            #     print("Send Mail")

            i = i + 1
        file_writer.close()


    def check_fragment_1_1(self,fragment,head,tail):
        sum = 0
        while head < tail -1 :
            sum += (fragment.loc[head, 'Proposed %']).astype(float)
            # if fragment.loc[head, 'RT'] == "G10MAURITIUS" :
            #     print(fragment)
            #     exit("For bug finding purposes")
            head = head + 1
        return sum == 100

        #step 1
    def df_break_into_fragment(self, df,last_code):
        """
            Step 1: Summary Verification
        """
        len_df_dg = len(df)
        i = 1 #avoid firs
        f_first_index = 0 #each fragment first index
        while i < len_df_dg :
            if not df['Node'].isnull().iloc[i]:
                 fragment = df.iloc[f_first_index :i]
                # # Step 1: Summary Verification
                # #  Go to step 2
                 if self.check_fragment_1_1(fragment,f_first_index,i) : #verify Sumation of each Fragment
                    #Step 2: Script Preparation
                     print("Verified Each Part of Fragment")
                     print(fragment)
                     self.prepare_lst_script(last_code,fragment,f_first_index,i)
                 else:
                     ##=== Save the unused Fragment into xl
                     config.plan_reject_df = config.plan_reject_df.append(fragment)
                     print( "Failed ! #verify Sumation of each Fragment")
                     print("Mail prepare to shoot Pending")

                 f_first_index = i #next fragment first index
            else:
                fragment =""
            i = i+1
            # print (i)
    def verify_plan_xl_df_dg(self,df):

        #get df header
        dg_column = df.columns.ravel()
        #matching Column
        if all(item in dg_column for item in config.tergate_header): #Header Verification
            print("Success! Plan header")
            return True
        else:
            print("Plan Header in wrong format Warning and  shot mail")
            return False


