# scripts/update_popular_posts.py

import os
import re
import requests
import git
from dateutil import parser

# -----------------------------
# 설정
# -----------------------------
VELOG_USERNAME = "sunmins"
GRAPHQL_URL = "https://v2.velog.io/graphql"  # velog GraphQL 엔드포인트

REPO_PATH = "."
README_PATH = os.path.join(REPO_PATH, "README.md")

POPULAR_START = "<!-- VELLOG_POPULAR_POSTS:START -->"
POPULAR_END = "<!-- VELLOG_POPULAR_POSTS:END -->"

TOP_N = 3  # 인기글 개수


# -----------------------------
# Velog 인기글 조회 로직
# -----------------------------
def get_session_with_cookies():
    access_token = os.getenv("VELOG_ACCESS_TOKEN")
    refresh_token = os.getenv("VELOG_REFRESH_TOKEN")

    if not access_token or not refresh_token:
        print("[Popular] VELOG_ACCESS_TOKEN / VELOG_REFRESH_TOKEN 환경변수가 없습니다. 인기글 업데이트를 건너뜁니다.")
        return None, None

    session = requests.Session()
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"access_token={access_token}; refresh_token={refresh_token}",
    }
    return session, headers


def fetch_all_posts(session, headers, username):
    """
    Posts 쿼리로 모든 글 목록 가져오기 (cursor 기반 페이징)
    """
    posts = []
    cursor = None

    while True:
        payload = {
            "operationName": "Posts",
            "variables": {
                "cursor": cursor,
                "username": username,
                "temp_only": False,
                "tag": None,
                "limit": 100,
            },
            "query": """
            query Posts(
              $cursor: ID
              $username: String
              $temp_only: Boolean
              $tag: String
              $limit: Int
            ) {
              posts(
                cursor: $cursor
                username: $username
                temp_only: $temp_only
                tag: $tag
                limit: $limit
              ) {
                id
                title
                url_slug
                released_at
                __typename
              }
            }
            """,
        }

        resp = session.post(GRAPHQL_URL, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        post_list = data.get("data", {}).get("posts", [])
        if not post_list:
            break

        posts.extend(post_list)
        cursor = post_list[-1]["id"]

    return posts


def fetch_post_views(session, headers, post_id):
    """
    GetStats 쿼리로 특정 글의 조회수(total) 가져오기
    """
    payload = {
        "operationName": "GetStats",
        "variables": {"post_id": post_id},
        "query": """
        query GetStats($post_id: ID!) {
          getStats(post_id: $post_id) {
            total
            __typename
          }
        }
        """,
    }

    resp = session.post(GRAPHQL_URL, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    stats = data.get("data", {}).get("getStats", {})
    return stats.get("total", 0) or 0


def fetch_popular_posts(username, top_n=3):
    session, headers = get_session_with_cookies()
    if session is None:
        return []

    print("[Popular] 전체 글 목록 조회 중...")
    posts = fetch_all_posts(session, headers, username)

    if not posts:
        print("[Popular] 가져온 게시글이 없습니다.")
        return []

    posts_with_views = []
    for idx, p in enumerate(posts, start=1):
        post_id = p["id"]
        title = p["title"]
        slug = p["url_slug"]
        released_at = p.get("released_at")

        print(f"[Popular] ({idx}/{len(posts)}) 조회수 조회 중: {title}")
        try:
            views = fetch_post_views(session, headers, post_id)
        except Exception as e:
            print(f"[Popular] 조회수 조회 실패({title}): {e}")
            views = 0

        posts_with_views.append(
            {
                "title": title,
                "url_slug": slug,
                "released_at": released_at,
                "views": views,
            }
        )

    # 조회수 기준 내림차순 정렬
    posts_with_views.sort(key=lambda x: x["views"], reverse=True)
    top_posts = posts_with_views[:top_n]

    result = []
    for p in top_posts:
        url = f"https://velog.io/@{username}/{p['url_slug']}"
        # released_at 은 안 써도 되지만, 필요하면 파싱해서 쓸 수 있음
        result.append(
            {
                "title": p["title"],
                "url": url,
                "views": p["views"],
            }
        )

    return result


# -----------------------------
# README Popular 섹션 갱신
# -----------------------------
def build_popular_section(popular_posts):
    """
    인기글 섹션용 마크다운 문자열 생성
    """
    lines = []
    lines.append("## Popular Velog Posts")
    lines.append("")
    for p in popular_posts:
        lines.append(f"- {p['views']} views · [{p['title']}]({p['url']})")
    lines.append("")
    return "\n".join(lines)


def update_readme(popular_posts):
    if not os.path.exists(README_PATH):
        old_content = ""
    else:
        with open(README_PATH, "r", encoding="utf-8") as f:
            old_content = f.read()

    new_block = build_popular_section(popular_posts)
    replacement = f"{POPULAR_START}\n{new_block}\n{POPULAR_END}"

    if POPULAR_START in old_content and POPULAR_END in old_content:
        # 기존 섹션 교체
        pattern = re.compile(
            re.escape(POPULAR_START) + r".*?" + re.escape(POPULAR_END),
            re.DOTALL,
        )
        new_content = pattern.sub(replacement, old_content)
    else:
        # 섹션이 없다면 README 끝에 추가
        if old_content and not old_content.endswith("\n"):
            old_content += "\n"
        # Latest 섹션 바로 밑에 오도록 하기 위해 단순히 뒤에 붙임
        new_content = old_content + "\n" + replacement + "\n"

    if new_content == old_content:
        print("[Popular] README 내용 변경 없음. 커밋 생략.")
        return False

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("[Popular] README 인기글 섹션 업데이트 완료.")
    return True


def commit_changes():
    repo = git.Repo(REPO_PATH)
    repo.git.add(README_PATH)
    repo.git.commit("-m", "Update README with popular Velog posts")
    print("[Popular] Git commit 완료.")


def main():
    try:
        popular_posts = fetch_popular_posts(VELOG_USERNAME, TOP_N)
    except Exception as e:
        print(f"[Popular] 인기글 조회 중 오류 발생: {e}")
        return

    if not popular_posts:
        print("[Popular] 인기글 데이터가 없어 README 를 수정하지 않습니다.")
        return

    changed = update_readme(popular_posts)
    if changed:
        commit_changes()


if __name__ == "__main__":
    main()
