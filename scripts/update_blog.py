import feedparser
import git
import os
import datetime
import re

# 벨로그 RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@sunmins'

# 깃허브 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 파일 이름에서 유효하지 않은 문자 제거
    # 날짜 + 제목으로 파일명 생성 (중복 방지)
    try:
        date_str = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    except AttributeError:
        # published 속성이 없으면 오늘 날짜 사용
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 제목에서 파일명에 쓸 수 없는 문자 제거
    safe_title = re.sub(r'[\\/*?:"<>|]', '-', entry.title)
    file_name = f"{date_str}-{safe_title}.md"
    file_path = os.path.join(posts_dir, file_name)

    # 파일이 존재하지 않거나 내용이 바뀌었으면 생성/수정
    write_file = False
    if not os.path.exists(file_path):
        write_file = True
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        if existing_content != entry.description:
            write_file = True

    if write_file:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)  # 글 내용을 파일에 작성

        # 깃허브 커밋
        repo.git.add(file_path)
        repo.git.commit('-m', f'Update post: {entry.title}')

# 변경 사항을 깃허브에 푸시
repo.git.push()
