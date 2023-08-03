from dataExchangelmpl import dataEx,config

unitsId = "61c4a9ca515e2f6d59bff022"
dataEx = dataEx()
# try:
    # dataEx.getLoginToken()
# except:
    # dataEx.getLoginToken()

tag_df = dataEx.getTagmeta(unitsId)

# taglist= ['CEN1_M24_R']
# dataEx.dataExachangeCooling(taglist)
# print(len(tag_df))
for tag in range(0,len(tag_df)): 
    if 'TJY' in tag_df.loc[tag,'dataTagId']:
        taglist = [tag_df.loc[tag,'dataTagId']]
        # taglist= ['CEN1_M24_R']
        print(taglist)
        try:
            dataEx.dataExachangeCooling(taglist)
        except:
            pass