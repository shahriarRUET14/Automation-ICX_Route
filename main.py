import pandas as pd
from icx import icx
from parse_file import parse_file
import  config as cf
icx_obj = icx()
parse_file_obj = parse_file()

if __name__ == '__main__':

    df_dg05,df_dg06, df_dg10, df_cg11, df_cg12 = parse_file_obj.read_plan(f"{cf.input_path}\icx_plan.xlsx")
    ##Summary Verification and script Generation
    ## Step 1: Summary Verification & lst Script Generation
    if icx_obj.verify_plan_xl_df_dg(df_dg05):  # Plan Sheet verification
        icx_obj.df_break_into_fragment(df_dg05, cf.virtual_device_code["DG05"])  # Lst Script

    if icx_obj.verify_plan_xl_df_dg(df_dg06) :                              #Plan Sheet verification
        icx_obj.df_break_into_fragment(df_dg06,cf.virtual_device_code["DG06"])              #Lst Script

    if icx_obj.verify_plan_xl_df_dg(df_dg10):                              #Plan Sheet verification
        icx_obj.df_break_into_fragment(df_dg10 ,cf.virtual_device_code["DG10"])             #Lst Script

    if icx_obj.verify_plan_xl_df_dg(df_cg11):                              #Plan Sheet verification
        icx_obj.df_break_into_fragment(df_cg11 ,cf.virtual_device_code["CG11"])             #Lst Script

    if icx_obj.verify_plan_xl_df_dg(df_cg12):                              #Plan Sheet verification
        icx_obj.df_break_into_fragment(df_dg10 ,cf.virtual_device_code["CG12"])             #Lst Script

    print("\n###################  Saving Processed Plan File #####################")
    try:
    #--------Save Plan File Processed Data
        with pd.ExcelWriter(f"{cf.process_file_path}{cf.f_n_plan_process}") as writer:
            cf.plan_df.to_excel(writer, sheet_name='All_Data', index=False, header=True)
    #--------Save Plan File Processed Data
        with pd.ExcelWriter(f"{cf.process_file_path}{cf.f_n_plan_reject}") as writer:
            cf.plan_reject_df.to_excel(writer, sheet_name='All_Data', index=False, header=True)
    except Exception as e:
        ##This is folder permission related issue no big deal for exit whole RPA
        print("Unable to write Processed Plan On Excel" +cf.process_file_path )

    print("\n==================LST output Checking for Plan Verification ==================")
    #=lots of parsing :(
    parse_file_obj.lst_output_processing(f"""{cf.output_path}lstOp.rst""", False) #false for post Verfication status
    if not len(cf.unmatched_rt):
        print("PLAN Verified")
    else:
        print(cf.unmatched_rt)
        print("! Error Plan File Verification ")
        # exit("! Failed  Successfull Plan ")
        # Need a Exit
    print("\n#################  SET Script Preparation ####################")
    icx_obj.prepare_set_script(f"""{cf.process_file_path}{cf.f_n_plan_process}""")

    print("\n####################   Post Verification ###################")
    parse_file_obj.lst_output_processing(f"""{cf.output_path}lstOp.rst""", True) #false for post Verfication status
    if not len(cf.unmatched_rt):
        print("PLAN Verified")
    else:
        print(cf.post_unmatched_rt)
        print("! Error Plan File Verification ")
        # exit("! Failed  Successfull Plan ")
        # Need a Exit








