---
layout: home
title: "포스트 목록"
permalink: /posts/
author_profile: true
paginate: true
---

<div class="entries-layout">
  <div class="list__item">
    <ul>
      {% for post in paginator.posts %}
        <li style="margin-bottom: 20px;">
          <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
          <p><small><i class="far fa-calendar-alt" aria-hidden="true"></i> {{ post.date | date: "%Y년 %m월 %d일" }}</small></p>
          <p>{{ post.excerpt | strip_html | truncate: 120 }}</p>
        </li>
      {% endfor %}
    </ul>
  </div>
</div>

<!-- 페이지네이션 번호 이동 UI -->
{% if paginator.total_pages > 1 %}
<nav class="pagination">
  <ul>
    <!-- 이전 페이지 버튼 -->
    {% if paginator.previous_page %}
      <li><a href="{{ paginator.previous_page_path | relative_url }}" class="pagination--pager">이전</a></li>
    {% else %}
      <li><span class="pagination--pager disabled">이전</span></li>
    {% endif %}

    <!-- 페이지 번호 나열 -->
    {% assign start_page = 1 %}
    {% assign end_page = paginator.total_pages %}
    {% for page_num in (start_page..end_page) %}
      {% if page_num == paginator.page %}
        <li><a href="#" class="current" style="background-color: #494e52; color: #fff; pointer-events: none;">{{ page_num }}</a></li>
      {% elsif page_num == 1 %}
        <li><a href="{{ '/posts/' | relative_url }}">{{ page_num }}</a></li>
      {% else %}
        <li><a href="{{ site.paginate_path | replace: ':num', page_num | relative_url }}">{{ page_num }}</a></li>
      {% endif %}
    {% endfor %}

    <!-- 다음 페이지 버튼 -->
    {% if paginator.next_page %}
      <li><a href="{{ paginator.next_page_path | relative_url }}" class="pagination--pager">다음</a></li>
    {% else %}
      <li><span class="pagination--pager disabled">다음</span></li>
    {% endif %}
  </ul>
</nav>
{% endif %}