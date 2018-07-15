%rebase("templates/template.tpl")

<form action="{{from_root('/page/{}/edit', name)}}" method="post">
    <textarea name="x" cols="80" rows="15">{{content}}</textarea><br>
    <button type="submit">Submit!</button>
</form>
