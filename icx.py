import pandas as pd
from numpy.core.defchararray import upper

import config
import numpy as np
import pandas as pd

from icx_script import icx_script

class icx:
    def __init__(self):
        print("Constractor")
        icx_script_obj = icx_script()

    def __del__(self):

        print('Destructor called')
########################## SET Script Preparation ##################################
    def prepare_set_script(self,path):
        try:
            file_writer = open(f"{config.script_path}{config.f_n_lst_script}", "w")
            plan_df = pd.read_excel(path, 'All_Data')
            plan_length = len(plan_df)
        except Exception as e:
            exit("!Error: Failed opening Process Plan File in SET Script Preparation",e)
            return False

        i = 1  # avoid first index
        f_first_index = 0  # each fragment first index
        node = plan_df.loc[0, 'Node']
        rt = plan_df.loc[0, 'RT']
        while i  < plan_length:
            if not plan_df['Node'].isnull().iloc[i] or i  == plan_length:
                fragment = plan_df.iloc[f_first_index:i-1]
                j = f_first_index
                script_ln = f"""SET RT: RN="{rt}",SRSM=PERC"""
                first_line = ""
                second_line = ""

                while j < i-1:
                    srt = plan_df.loc[j, 'SRT#']
                    try:
                        srt_no = str(srt.split("Sub-route")[1])
                    except Exception as e:
                        print("!Index OverFlow ",e)
                        return False
                    exist_srt = plan_df.loc[j, 'Existing SRT']
                    prop_srt = plan_df.loc[j, 'Proposed SRT']
                    exist_srt_val = plan_df.loc[j, 'Existing %']
                    prop_srt_val= plan_df.loc[j, 'Proposed %']
                    # print(srt,exist_srt, prop_srt,exist_srt_val,prop_srt_val)
                    if upper(str(exist_srt).replace(" ", "")) != upper(str(prop_srt).replace(" ", "")) or upper(str(exist_srt_val).replace(" ", "")) != upper(str(prop_srt_val).replace(" ", "")) :
                        first_line += f""",SR{srt_no}N="{prop_srt}" """
                        second_line += f""",PSR{srt_no}={prop_srt_val}"""
                    j = j+1
                first_line = first_line.replace(" ", "")
                second_line = second_line.replace(" ", "")

                if len(first_line) and len(second_line) :
                    script_ln = script_ln + first_line + second_line +";\n"
                else:
                    script_ln =""
                    print("Completed Configuration Same no Set Script will require")

                print(script_ln)
                file_writer.write(script_ln)
                node = plan_df.loc[i, 'Node']
                rt = plan_df.loc[i, 'RT']
                f_first_index = i        # next fragment first index
            else:
                fragment = ""
            i = i + 1

        file_writer.close()
        return True




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
            break #run only first time a block of fragment will create one lst script
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
                     print("Verified Each Part of Fragment " +df.loc[f_first_index,"RT"] )
                     # print(fragment)
                     self.prepare_lst_script(last_code,fragment,f_first_index,i)
                 else:
                     ##=== Save the unused Fragment into xl
                     config.plan_reject_df = config.plan_reject_df.append(fragment)
                     # print( "Failed ! #verify Sumation of each Fragment"+ df.loc[f_first_index,"RT"])
                     # print("Mail prepare to shoot Pending")

                 f_first_index = i  #next fragment first index
            else:
                fragment =""
            i = i+1
            # print (i)
    def verify_plan_xl_df_dg(self,df):
        if not df.empty:
            #get df header
            dg_column = df.columns.ravel()
            #matching Column
            if all(item in dg_column for item in config.tergate_header): #Header Verification
                print("Success! Plan header")
                return True
            else:
                print("Plan Header in wrong format Warning and  shot mail")
                return False
        else :
            print("Empty DataFrame")
            return False


