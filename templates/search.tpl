%rebase('templates/template.tpl')
%page_title = 'Search results for {}'.format(query)

<h1>Search results for {{query}}</h1>

<ul>
    % for result in pages:
    <li><a href="{{from_root('/page/{}', result[1])}}">{{result[1]}}</a></li>
    % end
</ul>
