<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="{{ site.baseurl }}/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="{{ site.baseurl }}/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>

# Engineering Blog Archive

Welcome to the first-principles systems design log. Below is a dynamically generted index of all architectural breakdowns implemented so far:

---

<ul>
    {% for post in site.posts %}
        <li>
            <strong> {{ post.date | date: "%Y-%m-%d" }} </strong> - 
            <a href=" {{ site.baseurl }}{{ post.url }}"> {{ post.title }} </a>
            {% if post.description %}
                <br><small><em> {{ post.description }} </em></small>
            {% endif %}
        </li>
    {% endfor %}
</ul>

---

[Back to Documentation Hub]( {{ site.baseurl }} )