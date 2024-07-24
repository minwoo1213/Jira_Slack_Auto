import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 설정 파일 읽기
with open('config.json', 'r') as file:
    config = json.load(file)

# 설정 값 로드
jira_url = config['jira']['url']
jira_email = config['jira']['email']
jira_api_token = config['jira']['api_token']
jira_project_key = config['jira']['project_key']
slack_token = config['slack']['token']
slack_channel = config['slack']['channel']

# 멘션할 사용자 정보 가져오기
mention_username = 'mwcha'  # 여기에 멘션할 사용자의 Slack username을 넣으세요.

# Slack 클라이언트 초기화
client = WebClient(token=slack_token)

try:
    # Slack 사용자 목록 가져오기
    users_response = client.users_list()
    users = users_response['members']

    # 멘션할 사용자의 실제 이름 찾기
    mention_user_fullname = None
    for user in users:
        if user['name'] == mention_username:
            mention_user_fullname = user['profile']['real_name']
            break

    # 만약 사용자의 실제 이름을 찾지 못하면 예외 처리
    if not mention_user_fullname:
        raise ValueError(f"사용자 '{mention_username}'의 실제 이름을 찾을 수 없습니다.")

    # 현재 시간에서 1시간 전의 시간 계산
    one_hour_ago = datetime.now() - timedelta(hours=1)
    one_hour_ago_str = one_hour_ago.strftime('%Y-%m-%d %H:%M')

    # JQL 쿼리: 담당자가 지정되고 우선순위가 높은 이슈를 찾습니다.
    jql_query = f'project = "{jira_project_key}" AND assignee IS NOT EMPTY AND priority = "High" AND updated <= "{one_hour_ago_str}"'

    # Jira 요청 헤더
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Jira API 엔드포인트
    api_endpoint = '/rest/api/3/search'
    url = jira_url + api_endpoint

    # 요청 데이터
    data = {
        'jql': jql_query,
        'maxResults': 10,
        'fields': ['id', 'key', 'summary', 'updated']
    }

    # Jira 요청 보내기
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(jira_email, jira_api_token), data=json.dumps(data))

    # 응답 확인
    if response.status_code == 200:
        issues = response.json().get('issues')
        if issues:
            # Slack 메시지 구성
            issue_list = "\n".join([f'> *<{jira_url}/browse/{issue["key"]}|{issue["key"]}>*: {issue["fields"]["summary"]}' for issue in issues])
            slack_message = f'*{mention_user_fullname}님, 이슈들이 1시간 동안 수정되지 않았습니다:*\n\n{issue_list}\n\n'

            # Slack 메시지에 멘션 추가
            slack_message += f'<@{mention_username}>'

            # Slack 블록 구성
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": slack_message
                    }
                },
                {
                    "type": "divider"
                }
            ]

            # Slack 채널로 메시지 보내기
            response = client.chat_postMessage(
                channel=slack_channel,
                blocks=blocks
            )
            print('Slack 알림이 성공적으로 전송되었습니다.')
        else:
            print('조건에 맞는 이슈가 없습니다.')
    else:
        print(f'Jira 요청에 실패했습니다. 상태 코드: {response.status_code}')
        print(f'응답: {response.text}')
except SlackApiError as e:
    print(f'Slack 알림 전송에 실패했습니다: {e.response["error"]}')
except ValueError as ve:
    print(f'사용자 찾기 오류: {ve}')
except Exception as ex:
    print(f'오류 발생: {ex}')