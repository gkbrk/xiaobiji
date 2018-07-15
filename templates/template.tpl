<html>
    <head>
        <style>
         a {
             color: black;
         }

         textarea {
             width: 100%;
             height: 80vh;
         }

         button {
             width: 100%;
         }
        </style>
        <title>{{page_title}} - {{WIKI_TITLE}}</title>
    </head>
    <body>
        <h1 style="text-align: center;"><a href="{{ROOT}}">{{WIKI_TITLE}}</a></h1>
        {{!base}}
        <form action="{{ROOT}}/go" method="post">
            <hr>
            <span>Go:</span><input name="target" value="help">
        </form>
        <form action="{{ROOT}}/search" method="post">
            <span>Find:</span><input name="q" type="text">
        </form>
        <a href='qiki.py?a=.&p=home page'>What's new</a> | <a href='qiki.py?a='>Home</a>
    </body>
</html>
