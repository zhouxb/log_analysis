<html>
<head></head>
<body>
具体情况如下:
{% for alert in alerts %}
    <div> {{ alert.date }} {{ alert.domain }} {{ alert.resolve_sate }} {{ alert.resolve_detail }} {{ alert.count }} </div>
{% endfor %}
</body>
</html>
