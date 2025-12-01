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
    # entry.published에서 날짜 파싱, 시간대(GMT 등) 자동 처리
    try:
        date_obj = parser.parse(entry.published)
        date_str = date_obj.strftime('%Y-%m-%d')  # YYYY-MM-DD 형식
    except AttributeError:
        # published 속성이 없으면 updated 속성 사용, 없으면 'unknown-date'
        date_str = parser.parse(entry.updated).strftime('%Y-%m-%d') if hasattr(entry, 'updated') else 'unknown-date'

    # --- 파일명 처리 ---
    # 제목에서 파일명으로 쓸 수 없는 특수문자 제거
    safe_title = re.sub(r'[\\/*?:"<>|]', '-', entry.title)
    # 날짜-제목.md 형태로 파일명 생성
    file_name = f"{date_str}-{safe_title}.md"
    file_path = os.path.join(posts_dir, file_name)

    # --- 파일 존재 여부 및 내용 변경 체크 ---
    write_file = False
    if not os.path.exists(file_path):
        # 파일이 없으면 새로 생성
        write_file = True
    else:
        # 파일이 존재하면 기존 내용과 비교
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        if existing_content != entry.description:
            # 내용이 다르면 덮어쓰기
            write_file = True

    # --- 파일 작성 및 Git 커밋 ---
    if write_file:
        # 파일 쓰기
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)

        # 커밋 메시지: 새 글이면 Add, 기존 글 내용 변경이면 Update
        commit_msg = 'Add post' if not os.path.exists(file_path) else 'Update post'
        repo.git.add(file_path)
        repo.git.commit('-m', f'{commit_msg}: {entry.title}')

# --- 변경 사항 GitHub에 push ---
repo.git.push()
