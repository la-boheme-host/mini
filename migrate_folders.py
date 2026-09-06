import os
import shutil
import re
from datetime import datetime
from bs4 import BeautifulSoup

# 설정 경로
SOURCE_DIR = "./tistory_backup_posts"  # 티스토리 백업 폴더
TARGET_POSTS_DIR = "./_posts"          # Jekyll _posts 폴더
TARGET_IMG_DIR = "./assets/images"     # Jekyll 이미지 폴더

def advanced_migrate():
    if not os.path.exists(SOURCE_DIR):
        print(f"오류: {SOURCE_DIR} 폴더를 찾을 수 없습니다.")
        return

    os.makedirs(TARGET_POSTS_DIR, exist_ok=True)

    for post_folder in os.listdir(SOURCE_DIR):
        folder_path = os.path.join(SOURCE_DIR, post_folder)
        
        if os.path.isdir(folder_path):
            post_id = post_folder # 폴더명 (포스트 번호)
            
            # 1. 이미지 폴더 이동
            src_img_folder = os.path.join(folder_path, "img")
            dest_img_folder = os.path.join(TARGET_IMG_DIR, post_id)
            
            first_image_path = ""
            if os.path.exists(src_img_folder):
                os.makedirs(dest_img_folder, exist_ok=True)
                img_files = sorted(os.listdir(src_img_folder))
                for img_file in img_files:
                    if img_file.startswith('.'):
                        continue
                    shutil.copy(
                        os.path.join(src_img_folder, img_file),
                        os.path.join(dest_img_folder, img_file)
                    )
                valid_imgs = [f for f in img_files if not f.startswith('.')]
                if valid_imgs:
                    first_image_path = f"/assets/images/{post_id}/{valid_imgs[0]}"

            # 2. 포스트 파일(.html 또는 .md) 처리
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".html") or file_name.endswith(".md"):
                    src_file = os.path.join(folder_path, file_name)
                    
                    with open(src_file, "r", encoding="utf-8") as f:
                        raw_html = f.read()
                    
                    # BeautifulSoup으로 HTML 파싱
                    soup = BeautifulSoup(raw_html, 'html.parser')
                    
                    # 타이틀 추출
                    title_tag = soup.find('title')
                    post_title = title_tag.text.strip() if title_tag else f"Post {post_id}"
                    
                    # 2-1. <p class="category"> 추출 및 본문에서 제거
                    category_tag = soup.find('p', class_='category')
                    post_category = category_tag.text.strip() if category_tag else ""
                    if category_tag:
                        category_tag.decompose()

                    # 2-2. 태그 추출 수정: 태그 종류에 상관없이 class="tags" 탐색 후 # 기준 파싱 (최대 2개)
                    tags_tag = soup.find(class_='tags')
                    post_tags = []
                    if tags_tag:
                        tags_text = tags_tag.text.strip()
                        if tags_text:
                            # 정규표현식으로 # 뒤에 오는 단어를 찾고, 최대 2개만 추출
                            raw_tags = re.findall(r'#([^\s,]+)', tags_text)
                            post_tags = raw_tags[:2]
                        tags_tag.decompose()

                    # 2-3. <p class="date"> 추출 및 포스트별 고유 날짜 파싱
                    date_tag = soup.find('p', class_='date')
                    extracted_date_str = date_tag.text.strip() if date_tag else ""
                    if date_tag:
                        date_tag.decompose()

                    file_date_prefix = datetime.now().strftime('%Y-%m-%d')
                    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S +0900')

                    if extracted_date_str:
                        try:
                            parsed_dt = datetime.strptime(extracted_date_str, "%Y-%m-%d %H:%M:%S")
                            file_date_prefix = parsed_dt.strftime('%Y-%m-%d')
                            formatted_date = parsed_dt.strftime('%Y-%m-%d %H:%M:%S +0900')
                        except ValueError:
                            pass

                    # 2-4. <h2 class="title-article"> 태그 삭제
                    h2_title_tag = soup.find('h2', class_='title-article')
                    if h2_title_tag:
                        h2_title_tag.decompose()

                    # 본문 내용 추출 및 요약글(excerpt) 생성
                    body_tag = soup.find('body')
                    post_excerpt = ""
                    if body_tag:
                        plain_text = body_tag.get_text(separator=' ', strip=True)
                        post_excerpt = plain_text[:150].replace('"', "'").replace('\n', ' ') + "..."
                        post_content = "".join([str(child) for child in body_tag.children])
                    else:
                        post_content = raw_html

                    # 본문 내부 이미지 경로 치환
                    post_content = re.sub(
                        r'src=["\'](\./)?img/', 
                        f'src="/mini/assets/images/{post_id}/', 
                        post_content
                    )

                    # 3. Jekyll Front Matter 조합
                    front_matter = f"""---
layout: single
title: "{post_title}"
date: {formatted_date}
permalink: /{post_id}/
"""
                    if post_excerpt:
                        front_matter += f'excerpt: "{post_excerpt}"\n'

                    if post_category:
                        front_matter += f"categories: {post_category}\n"

                    # tags: 값1 값2 형태 조합
                    if post_tags:
                        tags_str = " ".join(post_tags)
                        front_matter += f"tags: {tags_str}\n"

                    if first_image_path:
                        front_matter += f"""header:
  image: {first_image_path}
"""
                    front_matter += "---\n\n"

                    final_markdown_content = front_matter + post_content

                    # 4. 파일명 변경 규칙 적용
                    new_file_name = f"{file_date_prefix}-{post_id}.md"
                    dest_file = os.path.join(TARGET_POSTS_DIR, new_file_name)
                    
                    with open(dest_file, "w", encoding="utf-8") as f:
                        f.write(final_markdown_content)
                        
                    print(f"변환 완료: {new_file_name} (태그: {post_tags})")

if __name__ == "__main__":
    advanced_migrate()