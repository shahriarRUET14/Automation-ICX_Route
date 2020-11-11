
import  pandas as pd

#=== Initializing a dataframe with required data from plan xl
plan_df = pd.DataFrame()
plan_df = plan_df.fillna(0) # with 0s rather than NaNs
##===  Rejected Plan File Save
plan_reject_df = pd.DataFrame()
plan_reject_df = plan_reject_df.fillna(0) # with 0s rather than NaNs

##=== directory specifying
root_path = f"resource"
output_path =f"{root_path}/output/"
input_path = f"{root_path}/input/"
process_file_path = f"{root_path}/processed/"
store_path =f"{root_path}/stored/"
f_n_plan_process = 'Processed_Plan.xlsx'
script_path=f"{root_path}/script/"
f_n_lst_script = "lst_script.txt"
f_n_plan_reject= "rejected_plan.xlsx"


## ====Set All mail
mail_dev = ""
mail_cc = ""
mail_planner = ""
mail_bcc = ""

tergate_header_dg06 =['Node', 'Country', 'DN Set', 'Prefix', 'RTANA', 'RT', 'SRT Selection Mode', 'SRT#', 'Existing SRT', 'Proposed SRT', 'Existing %', 'Proposed %']
tergate_header_dg10 = ['Node', 'Country', 'DN Set', 'Prefix', 'RTANA', 'RT', 'SRT Selection Mode', 'SRT#', 'Existing SRT', 'Proposed SRT', 'Existing %', 'Proposed %']
tergate_header = ['Node', 'Country', 'DN Set', 'Prefix', 'RTANA', 'RT', 'SRT Selection Mode', 'SRT#', 'Existing SRT', 'Proposed SRT', 'Existing %', 'Proposed %']



virtual_device_code = {
        "DG05"  : "DG05_MSOFT",
        "DG06"  :"DG06_MSOFT",
        "DG10"  : "DG10_MSOFT",
        "CG11"  : "CG11_MSOFT",
        "CG12"  :"CG12_MSOFT",
        "DRG02" :"DRG02_MSOFT",
        "CGDR01":"CGDR01_MSOFT"
}

legacy_ne_list = {
    'DG05_MSOFTX': '192.168.120.14',
    'DG06_MSOFT': '192.168.116.14',
    'DG10_MSOFT': '192.168.141.35',
    'CG11_MSOFT': '192.168.143.25',
    'CG12_MSOFT': '192.168.145.26',
    'DRG02_MSOFT': '192.168.141.19',
    'CGDR01_MSOFT': '192.168.143.30',
    'SPS01_SPS': '192.168.116.46',
    'SPS02_SPS': '192.168.141.46'
}

virtual_ne_list = {
    'VLSP01_SPS': '10.180.3.83',
    'ALSP01_SPS': '10.180.11.83'
}

legacy_sps_list = {
    'SPS01_SPS': '192.168.116.46',
    'SPS02_SPS': '192.168.141.46'
}

virtual_sps_list = {
    'VLSP01_SPS': '10.180.3.83',
    'ALSP01_SPS': '10.180.11.83'
}
