%rebase("templates/template.tpl")

<h2 style="margin: 0;">{{page_title}}</h2>
<a href="{{bottle.request.url}}/edit">Edit page</a> -
<a href="{{bottle.request.url}}/history">History</a> -
<a href="{{ROOT}}">Backlinks</a>
<hr>

{{!content}}
