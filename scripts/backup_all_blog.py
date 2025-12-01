import requests
import git
import os
import re
from dateutil import parser

# ------------------------------
# 설정
# ------------------------------

USERNAME = "sunmins"
GRAPHQL_URL = "https://v2.velog.io/graphql"

repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

# 백업 폴더 없으면 생성
os.makedirs(posts_dir, exist_ok=True)

# Git repo 로드
repo = git.Repo(repo_path)


def fetch_all_posts(username: str):
    """Velog GraphQL Posts 쿼리로 모든 글 메타데이터 가져오기 (페이지네이션)"""
    cursor = None
    all_posts = []

    while True:
        payload = {
            "operationName": "Posts",
            "variables": {
                "username": username,
                "cursor": cursor,
                "limit": 100,
            },
            "query": """
            query Posts($cursor: ID, $username: String, $temp_only: Boolean, $tag: String, $limit: Int) {
              posts(cursor: $cursor, username: $username, temp_only: $temp_only, tag: $tag, limit: $limit) {
                id
                title
                url_slug
                released_at
              }
            }
            """,
        }

        res = requests.post(GRAPHQL_URL, json=payload)
        res.raise_for_status()
        data = res.json()["data"]["posts"]

        if not data:
            break

        all_posts.extend(data)
        cursor = data[-1]["id"]  # 마지막 글 id를 다음 요청의 cursor로 사용

    return all_posts


def fetch_post_body(username: str, url_slug: str):
    """단일 글의 본문(body) 가져오기"""
    payload = {
        "operationName": "ReadPost",
        "variables": {"username": username, "url_slug": url_slug},
        "query": """
        query ReadPost($username: String, $url_slug: String) {
          post(username: $username, url_slug: $url_slug) {
            title
            body
            released_at
          }
        }
        """,
    }

    res = requests.post(GRAPHQL_URL, json=payload)
    res.raise_for_status()
    post = res.json()["data"]["post"]
    return post


def safe_filename(date_str: str, title: str) -> str:
    safe_title = re.sub(r'[\\/*?:"<>|]', '-', title)
    return f"{date_str}-{safe_title}.md"


def main():
    posts_meta = fetch_all_posts(USERNAME)
    print(f"총 {len(posts_meta)}개 글 메타데이터 조회 완료")

    new_files = []

    for meta in posts_meta:
        # 날짜 처리
        released_at = meta.get("released_at")
        if released_at:
            date_obj = parser.parse(released_at)
            date_str = date_obj.strftime('%Y-%m-%d')
        else:
            date_str = 'unknown-date'

        # 파일명
        file_name = safe_filename(date_str, meta["title"])
        file_path = os.path.join(posts_dir, file_name)

        # 이미 있으면 건너뜀 (초기 백업용)
        if os.path.exists(file_path):
            print(f"[SKIP] 이미 존재: {file_name}")
            continue

        # 본문 가져오기
        post_detail = fetch_post_body(USERNAME, meta["url_slug"])
        body = post_detail["body"]

        # 파일 생성
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(body)

        repo.git.add(file_path)
        new_files.append(file_path)
        print(f"[ADD] 새 파일 추가: {file_name}")

    # 커밋 & 푸시
    if new_files:
        repo.git.commit('-m', 'Full backup of all Velog posts via GraphQL')
        repo.git.push()
        print(f"[DONE] {len(new_files)}개 글을 백업하고 푸시했습니다.")
    else:
        print("[DONE] 새로 백업할 글이 없어 커밋/푸시를 생략합니다.")


if __name__ == "__main__":
    main()
