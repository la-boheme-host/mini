---
layout: home
title: "La bohème Blog"
excerpt: "haanss Blog."
entries_layout: list
---

{% assign latest_post = site.posts.first %}

<!-- 1. 좌우 여백 없이 화면에 꽉 차는 동적 히어로(헤더) 영역 -->
<div class="page__hero--overlay" style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.2)), url('{{ latest_post.header.overlay_image | relative_url }}'); background-size: cover; background-position: center; padding: 5rem 2rem; text-align: left; color: #fff; width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; margin-bottom: 2rem;">
  <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
    <h1 style="color: #fff; font-size: 2.5rem; margin-bottom: 1rem;">{{ latest_post.title }}</h1>
    <p style="font-size: 1.2rem; max-width: 600px; margin: 0 0 1.5rem 0;">{{ latest_post.excerpt | strip_html | truncate: 100 }}</p>
    <a href="{{ latest_post.url | relative_url }}" class="btn btn--primary btn--large">최신 글 읽으러 가기 &rarr;</a>
  </div>
</div>