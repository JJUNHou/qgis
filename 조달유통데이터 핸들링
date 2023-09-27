import os
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

workingdirectory = "C:\\Users\\kofpi\\Downloads\\distribution"
filename1 = workingdirectory + "\\DealTB3.xlsx"
filename2 = workingdirectory + "\\central_point\\kr_province_central_point.xlsx"

df = pd.read_excel(filename1, dtype = {'물품분류번호':str, '세부물품분류번호':str,
                                       '물품식별번호':str, '업체사업자등록번호':str,
                                         'year': str})

province_df = pd.read_excel(filename2, dtype= {'SIG_CD':str, 'PROV_CD': str})

type_list = ['자연석판석', '조경석', '자연석경계석']

for type in type_list:
    is_type = df['세부품명'] == type # 자연석판석, 자연석경계석, 조경석 여부확인

    # 데이터추출
    subset_df = df[is_type]
    subset_df = subset_df.loc[:,['SupplyArea','DemandArea','금액']]
    not_zero = subset_df['금액'] != 0
    subset_df = subset_df[not_zero]
    #pivot_df의 SupplyArea, DemandArea열과 province_df의 x,y를 각각 조인
    subset_df = pd.merge(subset_df, province_df[['NameID','x','y']], left_on = 'SupplyArea', right_on = 'NameID',
          how = 'left')
    subset_df = subset_df.rename(columns = {'x' : 'Sup_x', 'y' : 'Sup_y'})
    subset_df = pd.merge(subset_df, province_df[['NameID','x','y']], left_on = 'DemandArea', right_on = 'NameID',
          how = 'left')
    subset_df = subset_df.rename(columns = {'x' : 'Dem_x', 'y' : 'Dem_y'})
    subset_df = subset_df.drop(labels=['NameID_x','NameID_y'],axis=1)
    subset_df['type'] = type

    subset_df.to_csv(f'C:\\Users\\kofpi\\Downloads\\distribution\\'+ type + '_전국.csv', index=True)



# for type in type_list:
#     is_type = df['세부품명'] == type # 자연석판석, 자연석경계석, 조경석 여부확인

#     # 데이터추출
#     subset_df = df[is_type]
#     subset_df = subset_df.loc[:,['SupplyArea','DemandArea','금액']]
#     pivot_df = subset_df.groupby(['SupplyArea', 'DemandArea'])['금액'].agg(['sum','count']).reset_index()
#     not_zero = pivot_df['sum'] != 0
#     pivot_df = pivot_df[not_zero]
#     #pivot_df의 SupplyArea, DemandArea열과 province_df의 x,y를 각각 조인
#     pivot_df = pd.merge(pivot_df, province_df[['NameID','x','y']], left_on = 'SupplyArea', right_on = 'NameID',
#           how = 'left')
#     pivot_df = pivot_df.rename(columns = {'x' : 'Sup_x', 'y' : 'Sup_y'})
#     pivot_df = pd.merge(pivot_df, province_df[['NameID','x','y']], left_on = 'DemandArea', right_on = 'NameID',
#           how = 'left')
#     pivot_df = pivot_df.rename(columns = {'x' : 'Dem_x', 'y' : 'Dem_y'})
#     pivot_df = pivot_df.drop(labels=['NameID_x','NameID_y'],axis=1)
#     pivot_df['type'] = type

#     # 결과 출력
#     금액_합계 = pivot_df['sum'].sum()
#     거래횟수_합계 = pivot_df['count'].sum()
#     print(f"{type}|{금액_합계}|{거래횟수_합계}")


#     pivot_df.to_csv(f'C:\\Users\\kofpi\\Downloads\\distribution\\'+ type + '_전국.csv', index=True)
