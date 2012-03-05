From: 蓝汛 DNS 服务器 <no-reply@chinacache.com>
To: 监控人员 <dreamersdw@gmail.com>
Subject: DNS 解析出现异常

具体情况如下:
{% for date, domain, resolve_state, resolve_detail, count in alerts %}
    {{date}} {{domain}} {{resolve_state}} {{resolve_detail}} {{count}}
{%- endfor %}
