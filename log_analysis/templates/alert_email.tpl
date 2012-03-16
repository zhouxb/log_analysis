<html>
<head></head>
<body>
具体情况如下:
{% for date, domain, resolve_state, resolve_detail, count in alerts %}
	<div>{{date}} {{domain}} {{resolve_state}} {{resolve_detail}} {{count}}</div>
{% endfor %}
</body>
</html>
