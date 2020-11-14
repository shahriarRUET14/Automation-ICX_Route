
import pandas as pd
from icx import icx
from parse_file import parse_file
import  config as cf
icx_obj = icx()
parse_file_obj = parse_file()

if __name__ == '__main__':

    # df_dg06, df_dg10 = parse_file_obj.read_plan(f"{cf.input_path}\icx_plan.xlsx")
    # # print(df_dg06)
    # ##Summary Verification and script Generation
    # if icx_obj.verify_plan_xl_df_dg(df_dg06) :
    #     ## Step 1: Summary Verification & lst Script Generation
    #     icx_obj.df_break_into_fragment(df_dg06,cf.virtual_device_code["DG06"])
    #
    # if icx_obj.verify_plan_xl_df_dg(df_dg10):
    #     ## Step 1: Summary Verification & lst Script Generation
    #     icx_obj.df_break_into_fragment(df_dg10 ,cf.virtual_device_code["DG10"])
    # try:
    # #--------Save Plan File Processed Data
    #     with pd.ExcelWriter(f"{cf.process_file_path}{cf.f_n_plan_process}") as writer:
    #         cf.plan_df.to_excel(writer, sheet_name='All_Data', index=False, header=True)
    # #--------Save Plan File Processed Data
    #     with pd.ExcelWriter(f"{cf.process_file_path}{cf.f_n_plan_reject}") as writer:
    #         cf.plan_reject_df.to_excel(writer, sheet_name='All_Data', index=False, header=True)
    # except Exception as e:
    #     ##This is folder permission related issue no big deal for exit whole RPA
    #     print("Unable to write Processed Plan On Excel" +cf.process_file_path )

    print("==================LST output Processing==================")
    parse_file_obj.lst_output_processing(f"""{cf.output_path}lstOp.rst""")
    print(cf.unmatched_rt)






