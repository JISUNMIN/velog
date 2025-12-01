import feedparser
import git
import os
from dateutil import parser  # 날짜 문자열을 안전하게 파싱
import re  # 파일명에서 특수문자 처리

# ------------------------------
# 설정
# ------------------------------

# 벨로그 RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@sunmins'

# 깃허브 레포지토리 경로 (Actions 환경에서는 루트 기준)
repo_path = '.'

# 글을 저장할 폴더
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 로컬 Git 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# ------------------------------
# 글 처리
# ------------------------------
for entry in feed.entries:
    # --- 날짜 처리 ---
    try:
        date_obj = parser.parse(entry.published)
        date_str = date_obj.strftime('%Y-%m-%d')
    except AttributeError:
        date_str = parser.parse(entry.updated).strftime('%Y-%m-%d') if hasattr(entry, 'updated') else 'unknown-date'

    # --- 파일명 ---
    safe_title = re.sub(r'[\\/*?:"<>|]', '-', entry.title)
    file_name = f"{date_str}-{safe_title}.md"
    file_path = os.path.join(posts_dir, file_name)

    # --- 파일 존재 체크 ---
    file_existed = os.path.exists(file_path)

    # --- 파일 쓰기 여부 결정 ---
    write_file = False
    if not file_existed:
        write_file = True
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        if existing_content != entry.description:
            write_file = True

    # --- 파일 쓰기 & 커밋 ---
    if write_file:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(entry.description)

        commit_msg = 'Add post' if not file_existed else 'Update post'

        repo.git.add(file_path)
        repo.git.commit('-m', f'{commit_msg}: {entry.title}')
        print(f"{commit_msg}: {file_name}")

# --- 변경 사항 push ---
repo.git.push()
