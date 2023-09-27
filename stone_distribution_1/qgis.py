# 필요한 라이브러리를 임포트합니다.
from qgis.core import QgsMapRendererParallelJob
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject, QgsFeature
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsLineSymbol, QgsSimpleLineSymbolLayer, QgsSymbol, QgsSingleSymbolRenderer
from qgis.core import QgsProject, QgsVectorLayer, QgsLineSymbol, QgsMarkerLineSymbolLayer, QgsSingleSymbolRenderer
from qgis.core import QgsMapSettings
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtGui import QPageLayout, QPageSize
from qgis.core import QgsProject, QgsLayout, QgsLayoutExporter
##############################################
###############이전 레이어 삭제################
##############################################

# 현재 QGIS 프로젝트를 가져옵니다.
project = QgsProject.instance()

# 모든 레이어를 삭제합니다.
for layer in project.mapLayers().values():
    project.removeMapLayer(layer)

print('모든 레이어가 삭제되었습니다.')

##############################################
########### 프로젝트 좌표계설정 ###############
##############################################
crs = QgsCoordinateReferenceSystem('EPSG:4326')

# 현재 QGIS 프로젝트를 가져옵니다.
project = QgsProject.instance()

# 프로젝트의 좌표계를 설정합니다.
project.setCrs(crs)

# 좌표계가 설정되었는지 확인합니다.
if project.crs() == crs:
    print('프로젝트 좌표계가 설정되었습니다: EPSG 4326')
else:
    print('프로젝트 좌표계 설정에 실패했습니다.')

##############################################
#######대한민국 시군구 지도 레이어 올리기########
##############################################

shapefile_path1 = "C:/Users/dlwns/Downloads/distribution (1)/korea_province/korea_province.shp" # Shapefile 경로 지정
layer1 = QgsVectorLayer(shapefile_path1, "MyLayer1", "ogr") # 레이어 불러오기

# 레이어가 성공적으로 불러와지면 레이어를 맵에 추가합니다.
if layer1.isValid():
    QgsProject.instance().addMapLayer(layer1)
    print("레이어가 성공적으로 불러와졌습니다.")
else:
    print("레이어를 불러오는데 문제가 발생했습니다.")

#스타일 불러오기
existing_layer_name = "MyLayer1"
existing_layers = QgsProject.instance().mapLayersByName(existing_layer_name)
if existing_layers:
    existing_layer = existing_layers[0]  # 첫 번째 레이어를 선택
    print(f"{existing_layer_name} 레이어가 활성화되었습니다.")

style_path = 'D:/coding/stone_distribution_1/style/MyLayer1.qml'
existing_layer.loadNamedStyle(style_path)
existing_layer.triggerRepaint()

##############################################
########## 자연석판석 공급 지도 올리기##########
##############################################

shapefile_path2 = "C:/Users/dlwns/Downloads/distribution (1)/shp/조경석_경남수요.shp" # Shapefile 경로를 지정합니다.
layer2 = QgsVectorLayer(shapefile_path2, "MyLayer2", "ogr") # 레이어를 불러옵니다.

# 레이어가 성공적으로 불러와지면 레이어를 맵에 추가합니다.
if layer2.isValid():
    QgsProject.instance().addMapLayer(layer2)
    print("레이어가 성공적으로 불러와졌습니다.")
else:
    print("레이어를 불러오는데 문제가 발생했습니다.")

#스타일 불러오기
existing_layer_name = "MyLayer2"
existing_layers = QgsProject.instance().mapLayersByName(existing_layer_name)
if existing_layers:
    existing_layer = existing_layers[0]  # 첫 번째 레이어를 선택
    print(f"{existing_layer_name} 레이어가 활성화되었습니다.")

style_path = 'D:/coding/stone_distribution_1/style/MyLayer2.qml'
existing_layer.loadNamedStyle(style_path)
existing_layer.triggerRepaint()

##############################################
###############공급 포인트 찍기################
##############################################

existing_layer_name = "MyLayer2" # 기존 레이어의 이름을 지정합니다. (예: 'existing_layer')
existing_layers = QgsProject.instance().mapLayersByName(existing_layer_name) #기존레이어를 가져옵니다.

# 레이어가 발견되면 활성화합니다.
if existing_layers:
    existing_layer = existing_layers[0]  # 첫 번째 레이어를 선택
    print(f"{existing_layer_name} 레이어가 활성화되었습니다.")

# 포인트 레이어를 생성합니다.
point_layer_name = 'point_supply'
point_layer = QgsVectorLayer("Point?crs=epsg:4326", point_layer_name, "memory")

# 포인트 레이어에 필드를 정의합니다.
point_layer.startEditing()
point_layer.addAttribute(QgsField("SupplyArea", QVariant.String))  # 공급 지역 필드 추가
point_layer.addAttribute(QgsField("Sup_x", QVariant.Double))  # x 좌표 필드 추가
point_layer.addAttribute(QgsField("Sup_y", QVariant.Double))  # y 좌표 필드 추가
point_layer.addAttribute(QgsField("cost", QVariant.Double))  # y 좌표 필드 추가
point_layer.updateFields()

# 기존 레이어의 피처를 반복하면서 포인트 데이터를 생성하고 새 레이어에 추가합니다.
for feature in existing_layer.getFeatures():
    # 기존 레이어에서 좌표 가져오기 (예: x 및 y는 기존 레이어의 필드 이름)
    x = feature['Sup_x']  # x 필드 이름을 적절하게 변경
    y = feature['Sup_y']  # y 필드 이름을 적절하게 변경
    supply_area = feature['SupplyArea']
    cost = feature['cost']

    # 포인트 피처를 생성하고 새 레이어에 추가합니다.
    point_feature = QgsFeature()
    point_geometry = QgsGeometry.fromPointXY(QgsPointXY(x, y))
    point_feature.setGeometry(point_geometry)
    point_feature.setAttributes([supply_area, x, y, cost])
    point_layer.addFeature(point_feature)

# 변경 내용을 저장합니다.
point_layer.commitChanges()

# 새로운 레이어를 맵에 추가합니다.
QgsProject.instance().addMapLayer(point_layer)

#스타일 불러오기
existing_layer_name = "point_supply"
existing_layers = QgsProject.instance().mapLayersByName(existing_layer_name)
if existing_layers:
    existing_layer = existing_layers[0]  # 첫 번째 레이어를 선택
    print(f"{existing_layer_name} 레이어가 활성화되었습니다.")

style_path = 'D:/coding/stone_distribution_1/style/supply_point_symbol.qml'
existing_layer.loadNamedStyle(style_path)
existing_layer.triggerRepaint()


#######################################
########### 수요포인트 찍기#############
#######################################

existing_layer_name = "MyLayer2" # 기존레이어 이름을 지정합니다.
existing_layers = QgsProject.instance().mapLayersByName(existing_layer_name) # 기존 레이어를 가져옵니다.

# 레이어가 발견되면 활성화합니다.
if existing_layers:
    existing_layer = existing_layers[0]  # 첫 번째 레이어를 선택
    print(f"{existing_layer_name} 레이어가 활성화되었습니다.")

# 포인트 레이어를 생성합니다.
point_layer_name = 'point_demand'
point_layer = QgsVectorLayer("Point?crs=epsg:4326", point_layer_name, "memory")

# 포인트 레이어에 필드를 정의합니다.
point_layer.startEditing()
point_layer.addAttribute(QgsField("DemandArea", QVariant.String))  # 공급 지역 필드 추가
point_layer.addAttribute(QgsField("Dem_x", QVariant.Double))  # x 좌표 필드 추가
point_layer.addAttribute(QgsField("Dem_y", QVariant.Double))  # y 좌표 필드 추가
point_layer.updateFields()

# 기존 레이어의 피처를 반복하면서 포인트 데이터를 생성하고 새 레이어에 추가합니다.
for feature in existing_layer.getFeatures():
    # 기존 레이어에서 좌표 가져오기 (예: x 및 y는 기존 레이어의 필드 이름)
    x = feature['Dem_x']  # x 필드 이름을 적절하게 변경
    y = feature['Dem_y']  # y 필드 이름을 적절하게 변경
    demand_area = feature['DemandArea']

    # 포인트 피처를 생성하고 새 레이어에 추가합니다.
    point_feature = QgsFeature()
    point_geometry = QgsGeometry.fromPointXY(QgsPointXY(x, y))
    point_feature.setGeometry(point_geometry)
    point_feature.setAttributes([demand_area, x, y])
    point_layer.addFeature(point_feature)

field_name = 'DemandArea'

# 중복된 값을 제거한 고유한 값 목록을 가져옵니다.
unique_values = []
for feature in point_layer.getFeatures():
    value = feature[field_name]
    if value not in unique_values:
        unique_values.append(value)

# 변경 내용을 저장합니다.
point_layer.commitChanges()

# 새로운 레이어를 맵에 추가합니다.
QgsProject.instance().addMapLayer(point_layer)

#스타일 불러오기
existing_layer_name = "point_demand"
existing_layers = QgsProject.instance().mapLayersByName(existing_layer_name)
if existing_layers:
    existing_layer = existing_layers[0]  # 첫 번째 레이어를 선택
    print(f"{existing_layer_name} 레이어가 활성화되었습니다.")

style_path = 'D:/coding/stone_distribution_1/style/demand_point_symbol.qml'
existing_layer.loadNamedStyle(style_path)
existing_layer.triggerRepaint()