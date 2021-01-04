# debugtalk.py
import random
import time


def sleep(n_secs):
    time.sleep(n_secs)


def get_user_agent():
    user_agents = ["Mozilla/5.0 BenBen", "Mozilla/5.0 MaZai", "Mozilla/5.0 icon"]
    return random.choice(user_agents)


def get_accounts():
    accounts = [
        {"title": "������¼", "username": "keyou1", "password": "123456",
            "status_code": 200, "contain_msg": "token"},
        {"title": "�������", "username": "keyou1", "password": "123457",
            "status_code": 400, "contain_msg": "non_field_errors"},
        {"title": "�˺Ŵ���", "username": "keyou1111", "password": "123456",
            "status_code": 400, "contain_msg": "non_field_errors"},
        {"title": "�û���Ϊ��", "username": "", "password": "123456",
            "status_code": 400, "contain_msg": "username"},
        {"title": "����Ϊ��", "username": "keyou1", "password": "",
            "status_code": 400, "contain_msg": "password"},
    ]
    return accounts


def get_project_name():
    old_project_name = []
    while True:
        project_name = "����һ����ʱ����{}��Ŀ".format(random.randint(0, 10000))
        if project_name not in old_project_name:
            old_project_name.append(project_name)
            return project_name


def create_project():
    projects = [
        {
            "title": "����������Ŀ",
            "name": get_project_name(),
            "leader": "����",
            "tester": "�ɿ�",
            "programmer": "����",
            "publish_app": "������ɻ�C919����Ӧ��",
            "desc": "����Ŀ����������������",
            "status_code": 201
        },
        {
            "title": "��Ŀ��Ϊ��",
            "name": None,
            "leader": "С�ɿ�",
            "tester": "�ɿ�",
            "programmer": "����",
            "publish_app": "������ɻ�C919����Ӧ��",
            "desc": "����Ŀ����������������",
            "status_code": 400
        },
        {
            "title": "leaderΪ��",
            "name": get_project_name(),
            "leader": None,
            "tester": "�ɿ�",
            "programmer": "����",
            "publish_app": "������ɻ�C919����Ӧ��",
            "desc": "����Ŀ����������������",
            "status_code": 400
        },
        {
            "title": "testerΪ��",
            "name": get_project_name(),
            "leader": "С����",
            "tester": None,
            "programmer": "����",
            "publish_app": "������ɻ�C919����Ӧ��",
            "desc": "����Ŀ����������������",
            "status_code": 400
        },
    ]

    return projects