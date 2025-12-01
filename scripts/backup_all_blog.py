import feedparser
import git
import os
import re
from dateutil import parser

# ------------------------------
# 설정
# ------------------------------

# Velog RSS URL (최근 글 50개 이상 가져오기)
rss_url = 'https://api.velog.io/rss/@sunmins'

repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

# ------------------------------
# 모든 글 처리
# ------------------------------
for entry in feed.entries:
    # 날짜 처리
    try:
        date_obj = parser.parse(entry.published)
        date_str = date_obj.strftime('%Y-%m-%d')
    except AttributeError:
        date_str = parser.parse(entry.updated).strftime('%Y-%m-%d') if hasattr(entry, 'updated') else 'unknown-date'

    # 제목 안전화
    safe_title = re.sub(r'[\\/*?:"<>|]', '-', entry.title)
    file_name = f"{date_str}-{safe_title}.md"
    file_path = os.path.join(posts_dir, file_name)

    # 파일이 없으면 생성, 기존 내용과 달라도 덮어쓰기
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(entry.description)

    # 커밋 메시지: 새 글이면 Add
    repo.git.add(file_path)
    repo.git.commit('-m', f'Add post: {entry.title}')

# push
repo.git.push()
