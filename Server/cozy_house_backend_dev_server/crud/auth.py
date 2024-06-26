import logging
from datetime import datetime

from db.dao.settings_dao import get_user_settings_info
from db.dao.user_devices_dao import get_by_user_id, insert_new_device
from db.dao.users_dao import get_by_uid, insert_new_user, update_access_time, update_user_info
from db.table_info import Users, UserDevices


def signup(data):
    values = Users(
        user_name=data.name,
        user_id=data.email,
        user_pw=data.password,
        phone_num=data.phone,
        address='',
        is_agreed=data.agree,
        uid=data.uid,
        del_fl=False,
        rest_fl=False,
        role_type=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    res = insert_new_user(values)

    if res:
        logging.info('success to insert about user info!')


def device_info(data):
    # users 테이블에서 uid가 data.uid와 같은 데이터 조회
    user = get_by_uid(data.user_uid)
    device = get_by_user_id(user.id)

    if device == None:
        values = UserDevices(
            manufacturer=data.manufacturer,
            device_name=data.device_name,
            device_model=data.device_model,
            os_version=data.os_version,
            uuid=data.uuid,
            push_id=data.push_id,
            app_version=data.app_version,
            del_fl=False,
            user_id=user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        res = insert_new_device(values)

        if res:
            logging.info('success to insert about user device info!')
    else:
        # TODO: 앱 업데이트 및 device 정보 갱신 시, update 쿼리 생성
        logging.info('This device is already exist!')


def signin(param):
    # 마지막 로그인 시간 update
    update_access_time(param.uid)
    logging.info('success to update about user info!')

    user = get_by_uid(param.uid)
    device = get_by_user_id(user.id)
    settings = get_user_settings_info(user.id)

# videos에 담긴 데이터를 1개씩 분리, Json 형식으로 바꾸는 작업

    data = {}
    if user is not None:
        # user 객체의 데이터를 JSON으로 변환
        data['result'] = True
        data['uid'] = param.uid
        data['user_name'] = user.user_name
        data['user_id'] = user.user_id
        data['user_pw'] = user.user_pw
        data['phone_num'] = user.phone_num
        data['address'] = user.address
        data['device_uuid'] = device.uuid
        data['record_yn'] = settings.record_yn
        data['detection_yn'] = settings.detection_yn
        data['detection_time'] = settings.detection_time
        data['detection_area'] = settings.detection_area

        return data
    else:
        # 사용자를 찾지 못한 경우
        data['result'] = False
        return data


def user_info(data):
    # users 테이블에서 uid가 data.uid와 같은 데이터 조회
    update_user_info(data)

    logging.info('success to update about user info!')