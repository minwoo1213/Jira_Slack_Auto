from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack API 토큰 설정
slack_token = ''
client = WebClient(token=slack_token)

try:
    # Slack 사용자 목록 가져오기
    users_response = client.users_list()
    users = users_response['members']

    # 모든 사용자의 username 출력
    for user in users:
        print(f"Username: {user['name']}, Full Name: {user['profile']['real_name']}, Display Name: {user['profile']['display_name']}")
except SlackApiError as e:
    print(f"Error: {e.response['error']}")
except Exception as e:
    print(f"Unexpected error: {e}")
