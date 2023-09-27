import geopandas as gpd
from shapely.geometry import MultiLineString, LineString
import pandas as pd
from pyproj import CRS
import json
# CSV 파일을 읽어옵니다. CSV 파일에는 x1, y1, x2, y2 등의 좌표 열이 포함되어 있다고 가정합니다.

type_list = ['가평석','포천석','운천석','동해석','보령석','남원석','익산석',
             '보성석','고흥석','장흥석','영주석','상주석','거창석','도림석','마천석','제주석']

workingdirectory = "C:\\Users\\kofpi\\Downloads\\distribution"
savedirectory = "C:\\Users\\kofpi\\Downloads\\distribution\\shp"

for type in type_list:
    filename = workingdirectory + f"\\판석_{type}.csv"
    csv_file = filename
    df = pd.read_csv(csv_file, encoding= 'UTF-8')

    # LineString 객체를 생성하여 리스트에 추가합니다.
    try:
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
        output_shapefile = savedirectory+f"\\{type}.shp"
        gdf.to_file(output_shapefile, encoding = 'utf-8')
    except:
        print(f"{type}의 경우 국내 공급되는 자연석판석이 없습니다.")
        continue


