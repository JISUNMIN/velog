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

# README 최신 글 섹션용 데이터 담을 리스트
entries_for_readme = []

# ------------------------------
# 글 처리
# ------------------------------
for entry in feed.entries:
    # --- 날짜 처리 ---
    try:
        date_obj = parser.parse(entry.published)
        date_str = date_obj.strftime('%Y-%m-%d')  # YYYY-MM-DD 형식
    except AttributeError:
        if hasattr(entry, 'updated'):
            date_obj = parser.parse(entry.updated)
            date_str = date_obj.strftime('%Y-%m-%d')
        else:
            date_obj = None
            date_str = 'unknown-date'

    # README용 데이터 저장
    entries_for_readme.append({
        "date_obj": date_obj,
        "date_str": date_str,
        "title": entry.title,
        "link": getattr(entry, "link", None),
    })

    # --- 파일명 처리 ---
    # 제목에서 파일명으로 쓸 수 없는 특수문자 제거
    safe_title = re.sub(r'[\\/*?:"<>|]', '-', entry.title)
    # 날짜-제목.md 형태로 파일명 생성
    file_name = f"{date_str}-{safe_title}.md"
    file_path = os.path.join(posts_dir, file_name)

    # --- 파일 존재 여부 및 내용 변경 체크 ---
    file_existed = os.path.exists(file_path)
    write_file = False

    if not file_existed:
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
        commit_msg = 'Add post' if not file_existed else 'Update post'
        repo.git.add(file_path)
        repo.git.commit('-m', f'{commit_msg}: {entry.title}')
        print(f"{commit_msg}: {file_name}")

# ------------------------------
# README.md 최신 글 섹션 업데이트
# ------------------------------
readme_path = os.path.join(repo_path, 'README.md')
old_readme_content = ""

if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        old_readme_content = f.read()

# 최신 글 정렬 (날짜 기준 내림차순)
valid_entries = [e for e in entries_for_readme if e["date_obj"] is not None]
sorted_entries = sorted(valid_entries, key=lambda e: e["date_obj"], reverse=True)

# 최근 N개만 사용 (원하면 숫자 바꿔도 됨)
N = 5
latest_entries = sorted_entries[:N]

# 섹션용 마크다운 생성
lines = []
lines.append("## Latest Velog Posts")
lines.append("")
for e in latest_entries:
    date_str = e["date_str"]
    title = e["title"]
    link = e["link"]
    if link:
        lines.append(f"- {date_str} [{title}]({link})")
    else:
        lines.append(f"- {date_str} {title}")
lines.append("")

new_section = "\n".join(lines)

START_TAG = "<!-- VELLOG_RECENT_POSTS:START -->"
END_TAG = "<!-- VELLOG_RECENT_POSTS:END -->"

if old_readme_content:
    if START_TAG in old_readme_content and END_TAG in old_readme_content:
        # 기존 섹션 교체
        pattern = re.compile(
            re.escape(START_TAG) + r".*?" + re.escape(END_TAG),
            re.DOTALL,
        )
        replacement = f"{START_TAG}\n{new_section}\n{END_TAG}"
        new_readme_content = pattern.sub(replacement, old_readme_content)
    else:
        # 기존 README 끝에 섹션 추가
        if not old_readme_content.endswith("\n"):
            old_readme_content += "\n"
        new_readme_content = (
            old_readme_content
            + "\n"
            + f"{START_TAG}\n{new_section}\n{END_TAG}\n"
        )
else:
    # README가 없으면 새로 생성
    new_readme_content = f"{START_TAG}\n{new_section}\n{END_TAG}\n"

# 내용이 변경된 경우에만 README 갱신 + 커밋
if new_readme_content != old_readme_content:
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_readme_content)

    repo.git.add(readme_path)
    repo.git.commit('-m', 'Update README with latest Velog posts')
    print("[README] 최신 글 목록 업데이트 완료")

# --- 변경 사항 GitHub에 push ---
repo.git.push()
