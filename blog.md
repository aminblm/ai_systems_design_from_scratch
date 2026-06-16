---
layout: default
title: "Engineering Blog Index"
---

# Engineering Blog Archive

Welcome to the first-principles systems design log. Below is a dynamically generted index of all architectural breakdowns implemented so far:

---

<ul>
    {% for post in site.posts %}
        <li>
            <strong> {{ post.date | date: "%Y-%m-%d" }} </strong> - 
            <a href=" {{ site.baseurl }}{{ post.url }}"> {{ post.title }} </a>
            {% if post.description %}
                <br><small><em> {{ post.description }} </em></small></br>
            {% endif %}
        </li>
    {% endfor %}
</ul>