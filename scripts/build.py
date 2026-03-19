#!/usr/bin/env python3
"""
Blog Builder - 从 GitHub Issues 生成静态博客
"""
import os
import re
import json
import requests
import markdown
from datetime import datetime
from urllib.parse import quote

# 配置
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('REPO', 'ZhiXuanWang/blog')
DOCS_DIR = 'docs'
POSTS_DIR = f'{DOCS_DIR}/posts'

def fetch_issues():
    """获取 GitHub Issues（仅保留 open 且有 blog 标签的）"""
    url = f'https://api.github.com/repos/{REPO}/issues'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    params = {
        'state': 'open',
        'labels': 'blog',
        'sort': 'created',
        'direction': 'desc'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def slugify(title):
    """生成 URL 友好的 slug"""
    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]

def format_date(iso_date):
    """格式化日期"""
    dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
    return dt.strftime('%Y 年 %m 月 %d 日')

def md_to_html(content):
    """Markdown 转 HTML"""
    return markdown.markdown(content, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.toc'
    ])

def generate_post_page(issue, template):
    """生成文章页"""
    title = issue['title']
    content = md_to_html(issue['body'] or '')
    date = format_date(issue['created_at'])
    number = issue['number']
    labels = [l['name'] for l in issue['labels'] if l['name'] != 'blog']

    tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in labels])

    html = template.replace('{{title}}', title) \
                   .replace('{{content}}', content) \
                   .replace('{{date}}', date) \
                   .replace('{{tags}}', tags_html) \
                   .replace('{{number}}', str(number))

    return html

def generate_index(issues, template):
    """生成首页"""
    posts_html = ''
    for issue in issues:
        title = issue['title']
        excerpt = (issue['body'] or '')[:150] + '...'
        date = format_date(issue['created_at'])
        slug = slugify(title)
        labels = [l['name'] for l in issue['labels'] if l['name'] != 'blog']
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in labels])

        posts_html += f'''
        <article class="post-card">
            <p class="post-date">{date}</p>
            <h3 class="post-title"><a href="posts/{slug}.html">{title}</a></h3>
            <p class="post-excerpt">{excerpt}</p>
            <div class="post-tags">{tags_html}</div>
        </article>
        '''

    html = template.replace('{{posts}}', posts_html)
    return html

def main():
    print('🚀 开始构建博客...')

    # 创建输出目录
    os.makedirs(POSTS_DIR, exist_ok=True)

    # 读取模板
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index_template = f.read()

    with open('templates/post.html', 'r', encoding='utf-8') as f:
        post_template = f.read()

    # 获取 Issues
    print('📥 获取 Issues...')
    issues = fetch_issues()
    print(f'✅ 获取到 {len(issues)} 篇文章')

    # 生成首页
    print('🏠 生成首页...')
    index_html = generate_index(issues, index_template)
    with open(f'{DOCS_DIR}/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

    # 生成文章页
    print('📝 生成文章页...')
    for issue in issues:
        title = issue['title']
        slug = slugify(title)
        html = generate_post_page(issue, post_template)

        with open(f'{POSTS_DIR}/{slug}.html', 'w', encoding='utf-8') as f:
            f.write(html)

    # 复制 CNAME
    if os.path.exists('CNAME'):
        with open('CNAME', 'r') as f:
            cname_content = f.read()
        with open(f'{DOCS_DIR}/CNAME', 'w') as f:
            f.write(cname_content)
        print('📋 复制 CNAME 文件')

    print(f'✅ 构建完成！共生成 {len(issues)} 篇文章')

if __name__ == '__main__':
    main()
