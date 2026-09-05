---
layout: splash
title: "환영합니다"
excerpt: "저의 멋진 블로그에 오신 것을 환영합니다."

header:
  overlay_color: "#5e6165"
  actions:
    - label: "내 소개 보기"
      url: "/about/"

feature_row:
  - alt: "자동 업데이트"
    title: "최신 포스트 자동 노출"
    excerpt: "새 글을 작성하면 메인 페이지에 자동으로 반영됩니다."
    btn_label: "블로그 글 보기"
    btn_class: "btn--primary"
    url: "#"
---

{% include feature_row %}

## 🔥 가장 최근에 작성한 포스트

{% assign latest_post = site.posts.first %}
<div class="notice--primary" style="text-align: left; padding: 20px; border-radius: 4px;">
  <h3><a href="{{ latest_post.url | relative_url }}" style="color: inherit; text-decoration: none;">{{ latest_post.title }}</a></h3>
  <p><small><i class="far fa-calendar-alt" aria-hidden="true"></i> {{ latest_post.date | date: "%Y년 %m월 %d일" }}</small></p>
  <p>{{ latest_post.excerpt | strip_html | truncate: 120 }}</p>
  <a href="{{ latest_post.url | relative_url }}" class="btn btn--inverse btn--small">포스트 읽기 &rarr;</a>
</div>