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

# 백업 폴더 없으면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# Git repo 로드
repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

# 새로 추가되는 파일 목록
new_files = []

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

    # 이미 파일이 있으면 건너뛰기 (초기 백업용이니까)
    if os.path.exists(file_path):
        print(f"[SKIP] 이미 존재하는 파일입니다: {file_name}")
        continue

    # 파일이 없으면 새로 생성
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(entry.description)

    repo.git.add(file_path)
    new_files.append(file_path)
    print(f"[ADD] 새 파일 추가: {file_name}")

# ------------------------------
# 커밋 & 푸시
# ------------------------------
if new_files:
    # 새 파일이 하나 이상 있을 때만 커밋/푸시
    repo.git.commit('-m', 'Initial backup of blog posts')
    repo.git.push()
    print(f"[DONE] {len(new_files)}개 글을 백업하고 푸시했습니다.")
else:
    print("[DONE] 새로 백업할 글이 없어 커밋/푸시를 생략합니다.")
