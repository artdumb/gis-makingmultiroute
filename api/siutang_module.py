import requests
import json

# =========================================
#       두 위치 사이의 경로 정보
# =========================================
# INPUT :ori_lng - 출발지 경도
#       ori_lat - 출발지 위도
#       des_lng - 도착지 경도
#       des_lat - 도착지 위도
#       mode    - 대중교통(transit), 자동차(driving), 도보(walking)
#       depart_time - 출발시간

# OUTPUT: (dict)
#       x['arrival_time']     -도착시간
#       x['departure_time']   -출발시간
#       x['distance']         -총거리
#       x['duration']         -소요시간
#       x['end_address']      -도착장소주소
#       x['start_address']    -출발장소주소
#       x['end_location']     -도착장소좌표
#       x['start_location']   -출발장소위치
#
#       x['steps']            -상세경로
# ===========================================


def pointroute(ori_lng, ori_lat, des_lng, des_lat, mode='transit', depart_time='now'):
    URL = 'https://maps.googleapis.com/maps/api/directions/json?'\
        'origin='+str(ori_lat)+','+str(ori_lng) + '&'\
        'destination='+str(des_lat)+','+str(des_lng)+'&'\
        'mode='+mode+'&'\
        'departure_time='+depart_time+'&key=APIKEY'
    response = requests.get(URL)
    data = json.loads(response.text)
    return data['routes'][0]['legs'][0]


# =========================================
#           GeoJSON 각 점들간의 거리
# =========================================
# INPUT :GeoJSON
#               geometry : point geometry
#               properties : duration(해당위치에서 소요시간),
#                            startime(출발시간),
#                            serial(순서),
#                            title(장소이름)

# OUTPUT: (list)  --> 경로정보는 위에 참고
#         [ [장소1과2사이 경로정보 (dict)]
#           [장소2과3사이 경로정보 (dict)]
#           [장소3과4사이 경로정보 (dict)]
#                       ...
#         ]

#         (list)  --> 점, 경로 합친 리스트
#         [
#           [경도, 위도 ,소요시간,시작시간,제목]
#           [소요시간,거리,상세정보]
#           [경도, 위도 ,소요시간,시작시간,제목]
#           [소요시간,거리,상세정보]
#                       ...
#         ]

# ===========================================
def eachpointrout(data):
    all_result = []
    for i in range(len(data['features'])-1):
        ori_x = data['features'][i]['geometry']['coordinates'][0]
        ori_y = data['features'][i]['geometry']['coordinates'][1]
        des_x = data['features'][i+1]['geometry']['coordinates'][0]
        des_y = data['features'][i+1]['geometry']['coordinates'][1]
        route_detail = pointroute(ori_x, ori_y, des_x, des_y)

        duration = data['features'][i]['properties']['duration']
        startime = data['features'][i]['properties']['startime']
        title = data['features'][i]['properties']['title']
        all_result.append([ori_x, ori_y, duration, startime, title])
        all_result.append(
            [route_detail['duration'], route_detail['distance'], route_detail['steps']])

    # 마지막 데이터추가
    ori_x = data['features'][len(
        data['features'])-1]['geometry']['coordinates'][0]
    ori_y = data['features'][len(
        data['features'])-1]['geometry']['coordinates'][1]
    duration = data['features'][len(
        data['features'])-1]['properties']['duration']
    startime = data['features'][len(
        data['features'])-1]['properties']['startime']
    all_result.append([ori_x, ori_y, duration, startime, title])

    return all_result
