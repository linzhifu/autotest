# from django.test import TestCase
# (通过mysql源代码获取数据)
import requests
import time
import json
# import hashlib
import pymysql
import logging

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
if 1:
    logging.disable(logging.DEBUG)

# 保存实时token数值
TOKEN = ""


# Create your tests here.
# 连接MYSQL数据库 database 数据库名称
def connect_database(database='autotest'):
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='test123456',
        port=3306,
        db=database)
    return db


# 获取数据库内容 table:表  filterKey:筛选条件  filterValue:筛选值(筛选条件和值可以为空，代表不筛选)
# 如：SELECT * FROM table where filterKey=filterValue
def get_data(table, filterKey=None, filterValue=None):
    # 连接MYSQL数据库
    db = connect_database()
    cursor = db.cursor()
    if filterKey:
        sql = 'SELECT * FROM %s where %s=%s' % (table, filterKey, filterValue)
    else:
        sql = 'SELECT * FROM %s' % (table)
    try:
        cursor.execute(sql)
        # print('Count:', cursor.rowcount)
        # one = cursor.fetchone()
        # print('One:', one)
        # print('One Type:', type(one))
        results = cursor.fetchall()
        # print('Results:', results)
        # print('Results Type:', type(results))
        return results
    except Exception:
        print('Error 获取MYSQL数据失败')


# 更新数据库信息
def update_data(table, setKey, setValue, filterKey=None, filterValue=None):
    # 连接mysql
    db = connect_database()
    cursor = db.cursor()
    if filterKey:
        sql = 'UPDATE %s SET %s=%s WHERE %s=%s' % (table, setKey, setValue,
                                                   filterKey, filterValue)
    else:
        sql = 'UPDATE %s SET %s=%s' % (table, setKey, setValue)
    try:
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except Exception:
        print('Error 更新MYSQL数据失败')
        db.rollback()
    db.close()


# 获取MYSQL后端API信息
def get_apiInfo():
    data = {}
    # 获取所有模块,如user等模块
    results = get_data(table='apitest_apis')
    # 遍历所有模块，并获取API接口
    for result in results:
        api_id = result[0]
        module = result[1]
        data[module] = []
        apiinfos = get_data(
            table='apitest_apiinfo', filterKey='api_id', filterValue=api_id)
        for apiinfo in apiinfos:
            api = {}
            api['module'] = result[0]
            api['id'] = apiinfo[0]
            api['url'] = result[2] + apiinfo[9]
            api['name'] = apiinfo[1]
            api['method'] = apiinfo[2]
            api['param'] = apiinfo[3]
            api['json'] = apiinfo[4]
            api['response'] = apiinfo[5]
            data[module].append(api)
    return data


# 测试请求
def api_request(api):
    start = time.time()
    r = requests.Response()
    error = 'PASS'
    try:
        r = requests.request(
            method=api['method'],
            url=api['url'],
            params=api['param'],
            json=api['json'])
    except requests.exceptions.ConnectionError:
        error = "ConnectionError"
    except requests.exceptions.HTTPError:
        error = "HTTPError"
    except requests.exceptions.URLRequired:
        error = "URLRequired"
    except requests.exceptions.TooManyRedirects:
        error = "TooManyRedirects"
    except requests.exceptions.ReadTimeout:
        error = "ReadTimeout"
    except requests.exceptions.InvalidURL:
        error = "InvalidURL"

    finally:
        if error != 'PASS':
            # print(error)
            return False
    # 计算测试时间，精确到小数点后两位
    timeval = time.time() - start
    timeval = str(round(timeval, 2))
    logging.debug('RESPONSE：' + r.text)
    rev = json.loads(r.text)
    if 'data' in rev:
        if 'token' in rev['data']:
            global TOKEN
            TOKEN = rev['data']['token']
    if rev['errcode'] == api['response']['errcode'] and rev['errmsg'] == api[
            'response']['errmsg']:
        logging.info(error + '-' + api['name'] + '-测试时间：' + timeval)
        return True
    else:
        error = 'FAIL-RESPONSE 不一致'
        logging.info(error + '-' + api['name'] + '-测试时间：' + timeval)
        return False


# 测试API
def test_apis():
    apiInfos = get_apiInfo()
    for apiInfo in apiInfos:
        start = time.time()
        logging.info(apiInfo + '模块测试开始')
        moduleResu = True
        moduleID = ''
        apis = apiInfos[apiInfo]
        for api in apis:
            moduleID = api['module']
            if api['param']:
                api['param'] = json.loads(api['param'])
                for i in api['param']:
                    if i == 'token':
                        api['param'][i] = TOKEN
                update_data(
                    table='apitest_apiinfo',
                    setKey='apiparamvalue',
                    setValue='\'' + json.dumps(api['param']) + '\'',
                    filterKey='id',
                    filterValue=api['id'])
            if api['json']:
                api['json'] = json.loads(api['json'])
                # md5转换
                # api['json']['pswmd5'] = hashlib.md5(
                #     api['json']['pswmd5'].encode('utf-8')).hexdigest()
                for i in api['json']:
                    if api['json'][i] == 'NOW':
                        api['json'][i] = int(time.time())
            if api['response']:
                api['response'] = json.loads(api['response'])
            logging.debug('API：' + json.dumps(api))
            resu = api_request(api)
            if resu is False:
                moduleResu = False
            update_data(
                table='apitest_apiinfo',
                setKey='apistatus',
                setValue=resu,
                filterKey='id',
                filterValue=api['id'])
        update_data(
            table='apitest_apis',
            setKey='apistatus',
            setValue=moduleResu,
            filterKey='id',
            filterValue=moduleID)
        timeval = time.time() - start
        timeval = str(round(timeval, 2))
        if moduleResu:
            logging.info('PASS-' + apiInfo + '模块测试结束-测试时间：' + timeval + '\n')
        else:
            logging.info('FAIL-' + apiInfo + '模块测试结束-测试时间：' + timeval + '\n')


if __name__ == '__main__':
    test_apis()
