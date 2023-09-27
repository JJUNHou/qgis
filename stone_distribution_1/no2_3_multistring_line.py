import geopandas as gpd
from shapely.geometry import MultiLineString, LineString
import pandas as pd
from pyproj import CRS
import json
# CSV 파일을 읽어옵니다. CSV 파일에는 x1, y1, x2, y2 등의 좌표 열이 포함되어 있다고 가정합니다.

workingdirectory = "C:\\Users\\kofpi\\Downloads\\distribution"
savedirectory = "C:\\Users\\kofpi\\Downloads\\distribution\\shp"

type_list = ['자연석경계석', '자연석판석', '조경석']
spdm_list = ['경남공급', '경남수요']

for spdm in spdm_list:
    for type in type_list:
        filename = workingdirectory + f"\\"+type+"_"+spdm+".csv"
        csv_file = filename
        df = pd.read_csv(csv_file, encoding= 'UTF-8')

    # LineString 객체를 생성하여 리스트에 추가합니다.
        features = []
        for index, row in df.iterrows():
            line = LineString([(row['Sup_x'], row['Sup_y']), (row['Dem_x'], row['Dem_y'])])
            feature = {'geometry': line, 
                    'SupplyArea': row['SupplyArea'],
                    'DemandArea': row['DemandArea'],
                    'Sup_x': row['Sup_x'],
                    'Sup_y': row['Sup_y'],
                    'Dem_x': row['Dem_x'],
                    'Dem_y': row['Dem_y'],
                    'cost': row['금액']}  # 속성 정보를 포함한 딕셔너리
            features.append(feature)
        
            # GeoDataFrame을 생성합니다.
            gdf = gpd.GeoDataFrame(features, geometry='geometry', crs=CRS('EPSG:4326'))

    # Shapefile로 저장합니다.
        output_shapefile = savedirectory+f"\\"+type+"_"+spdm+".shp"
        gdf.to_file(output_shapefile, encoding = 'utf-8')