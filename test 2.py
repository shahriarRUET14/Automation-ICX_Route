def lst_fragment_parser(self, data, first, last):
    cf.lst_parsed_op_df = cf.lst_parsed_op_df.append({
        "Node": "John",
        "Country": "John",
        "DN Set": "John",
        "Prefix": "John",
        "RTANA": "John",
        "RT": "John",
        "SRT Selection Mode": "John",
        "SRT#": "John",
        "Proposed SRT": "Johny",
        "Existing %": "Johny",
        "Proposed %": "Johny"
    }, ignore_index=True)
    srt_selection_mode = "SRT Selection Mode"
    file_writer = open("temp.txt", "a")
    if "RETCODE = 0  " in str(data[first + 5]):  # Checking for success lst command
        # print(data[first + 5])

        i = first
        max_srt = 0
        flag = False  # to find max srt
        print("first" + i)
        print("last" + last)
        while i < last:  # checking if there is any block found or not
            if "Server name  =" in str(data[i]):
                temp = data[i].split("Server name  =")
                node = temp[1]
            # if "Route name  =" in str(data[i]):
            #     temp = data[i].split("Server name  =")
            #     country = temp[1]

            if "DN set  =" in str(data[i]):
                rt = data[i].split("DN set  =")
                node = temp[1]

            if "Route name  =" in str(data[i]):
                temp = data[i].split("Route name  =")
                rt = temp[1]

            if "Call prefix  =" in str(data[i]):
                temp = data[i].split("Call prefix  =")
                prefix = temp[1]

            if "Route selection name  =" in str(data[i]):
                temp = data[i].split("Route selection name  =")
                rtana = temp[1]
            # =Finding Max Subroute
            if flag == False and "Sub-route" in str(data[i]):
                t = 0
                while t < 48 and flag == False:  # 48 is possible max index
                    if f"""Sub-route {t}  =  """ in str(data[i]):
                        temp = data[i].split(f"""Sub-route {t}  =  """)
                        if temp[1] == "INVALID":
                            max_srt = t - 1
                            flag = True
                    t = t + 1
            print("i " + i)
            i = i + 1

            first_index = True
            i = first
            # while i < last :

            #
            # while i < last :
            #
            #
            #     file_writer.write(data[i]+"\n")
            #     i = i +1
