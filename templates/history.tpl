%rebase("templates/template.tpl")
%page_title = 'Edit history for {}'.format(name)

<h2>Showing edit history for {{name}}</h2>
<ul>
    % for hist in history:
    <li><a href="{{from_root('/page/{}/history/{}', name, hist[3])}}">{{hist[3]}}</a></li>
    % end
</ul>
