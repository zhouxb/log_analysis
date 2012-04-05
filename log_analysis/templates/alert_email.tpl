<html>
<head></head>
<body>
TOP100 域名中未 IP 解析至 Chinacache 服务器的情况如下:
{% for alert in alerts %}
    <div> 
        {{ alert.date }} 
        {{ alert.domain }} 
        {% for ip, count in alert.ips.items() %}
            {{ ip }}: {{count}} 次
        {% endfor %}
    </div>
{% endfor %}
</body>
</html>
