#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import requests
import os

URL = 'http://ec2-54-189-234-66.us-west-2.compute.amazonaws.com:8001/'

def get_environ(name):
    if name in os.environ:
        return os.environ[name]
    else:
        print("Exception occurred while getting environment variable - {} ".format(name))
        exit(0)

pipeline_id=81

def check_http(result):
    if result.status_code < 200 or result.status_code > 202:
        if result.text:
            raise requests.HTTPError(result.text)
        result.raise_for_status()

def start_testsuite( area_name, triage_owners=None):
    try:
        result = requests.post(URL + 'testsuite/add', json={
            'testsuitename': area_name,
            'owner': triage_owners
            })
        check_http(result)
        return result.text
    except Exception as exception:
            print("Exception occurred during start_testsuite for   area_name - {},"
                                "Exception details : {}".format(area_name,str(exception)))

def start_test(pipeline_id, test_name, suite_id, starttime):
    try:
        result = requests.post(URL + 'testcase/start', json={
            'pipelineid': pipeline_id,
            'testcasename': test_name,
            'testsuiteid': suite_id,
            'starttime': starttime
            })
        check_http(result)
        return result.text
    except Exception as exception:
            print("Exception occurred during start_test for pipelineid - {} and testname - {},"
                                "Exception details : {}".format(pipeline_id,test_name,str(exception)))

def finish_test(test_id, result,test_duration, data={}, state_dump_collect=False):
    try:
        error_message = None
        error_status = None
        if state_dump_collect:
            error_message = data['errorDetails']
            error_status = "infra_error or Test case Failed"
        finish_test_data = {
            'testid': test_id,
            'result': result,
            'duration':test_duration,
            'errormessage':error_message,
            'errorstatus':error_status
            }

       # finish_test_data.update(data)
        result = requests.put(URL + 'testcase/finish', json=finish_test_data)
        check_http(result)
        return result.text
    except Exception as exception:
        print("Exception occurred during finish_test for testid - {},"
                                        "Exception details : {}".format(test_id,str(exception)))


def finish_pipeline(finish_pipeline_data):
    try:
        result = requests.put(URL + 'pipeline/finish', json=finish_pipeline_data)
        check_http(result)
        return result.text
    except Exception as exception:
        print("Exception occurred during finish_pipeline : {}".format(str(exception)))

def upload_tests(root):
    try:

        failed_count = int(root.attrib['failures']) + int(root.attrib['errors'])
        suucess_count = int(root.attrib['tests']) - ( failed_count + int(root.attrib['skipped']))

        testreport = {
            "pipelineid": pipeline_id,
            "duration": int(float(root.attrib['time'])),
            "endtime": root.attrib['timestamp'],
            "result": "Success",
            "totaltestcase": int(root.attrib['tests']),
            "testcasepassed": suucess_count,
            "testcasefailed": failed_count,
            "testcaseskipped": int(root.attrib['skipped'])
        }

        for child in root:
            suite_id = start_testsuite(child.attrib['classname'], "Deepa Krishna")
            test_id = start_test(pipeline_id, child.attrib['name'], suite_id, root.attrib['timestamp'])
            added_finish = False
            for gc in child:
                finish_test_id = finish_test(test_id, 'FAILED', int(float(child.attrib['time'])))
                added_finish = True
                break
            if not added_finish:
                finish_test_id = finish_test(test_id, 'SUCCESS', int(float(child.attrib['time'])))

        finish_pipeline(testreport)

    except Exception as exception:
        print("Exception occured in upload test results : {}".format(exception))


def main():
    try:
        print('Calling a function upload tests ')
        tree = ET.parse('unit_report.xml')
        print(tree.getroot())
        root = tree.getroot()
        print("tag=%s, attrib=%s" % (root.tag, root.attrib))

        for child in root:
            upload_tests(child)
            print("tag=%s, attrib=%s" % (child.tag, child.attrib))

    except Exception as exception:
        print("Exception occurred during running upload results  for pipeline-id - Exception details : {}".format(str(exception)))
        pass

if __name__ == "__main__":
    main()
