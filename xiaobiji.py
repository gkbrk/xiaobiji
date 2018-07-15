#!/usr/bin/env python3
import bottle
import sqlite3
import subprocess
import sys
import os
import re

DB_FILE = 'wiki-database.sqlite'
WIKI_TITLE = '小笔记 Wiki Test'
ROOT = 'https://gkbrk.com/cgi-bin/xiaobiji/xiaobiji.py'

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)

    def get_page(self, name):
        c = self.conn.cursor()
        query = '''select * from pages
                 where pagename = ?
                 order by modifytimestamp desc limit 1;'''
        return c.execute(query, (name,)).fetchone()

    def insert_page(self, name, content):
        c = self.conn.cursor()
        c.execute('''insert into pages (pagename, pagecontent, modifytimestamp)
                     values (?, ?, CURRENT_TIMESTAMP);''', (name, content))
        self.conn.commit()

    def find_history(self, name):
        c = self.conn.cursor()
        return c.execute('''select * from pages
                          where pagename = ?
                          order by modifytimestamp desc limit 50;''', (name,))

    def get_historical_page(self, name, dt):
        c = self.conn.cursor()
        return c.execute('''select * from pages
                            where pagename = ?
                            and modifytimestamp = ?;''', (name, dt)).fetchone()

    def get_pages(self):
        c = self.conn.cursor()
        return c.execute('''select * from pages p1
                            where p1.modifytimestamp =
                            (select max(modifytimestamp) from pages p2
                            where p1.pagename = p2.pagename);''')

    def create_db(self):
        c = self.conn.cursor()
        c.execute('''create table pages (rowid,
                                         pagename text not null,
                                         pagecontent text,
                                         modifytimestamp text);''')
        self.conn.commit()
        
def format_pandoc(s, formatter='org'):
    cmd = ['pandoc', '-f', formatter, '-t', 'html', '--self-contained']
    s = s.encode('utf-8')
    s = subprocess.Popen(
                         cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE
                        ).communicate(s)[0].decode('utf-8')
    return re.sub('\[([\w ]+)\]', '<a href="{}/page/\\1/">\\1</a>'.format(ROOT), s)

def from_root(url, *args):
    return '{}{}'.format(ROOT, url).format(*args)

db = Database(DB_FILE)

@bottle.get('/')
def root():
    bottle.redirect(from_root('/page/Home'))

@bottle.get('/page/<name>')
def show_page(name):
    page = db.get_page(name)
    if not page:
        bottle.redirect(from_root('/page/{}/edit', name))
    page_title = page[1]
    content = format_pandoc(page[2])
    return bottle.template('templates/read.tpl', **(dict(globals(), **locals())))

@bottle.get('/page/<name>/edit')
def page_edit(name):
    page = db.get_page(name)
    if page:
        content = page[2]
    else:
        content = 'Put your content here'
    page_title = 'Editing {}...'.format(name)
    return bottle.template('templates/edit.tpl', **(dict(globals(), **locals())))

@bottle.post('/page/<name>/edit')
def page_edit_post(name):
    content = bottle.request.forms.getunicode('x', '')
    db.insert_page(name, content)
    bottle.redirect(from_root('/page/{}', name))

@bottle.post('/go')
def go():
    target = bottle.request.forms.get('target', 'Home')
    bottle.redirect(from_root('/page/{}', target))

@bottle.get('/page/<name>/history')
def page_history(name):
    history = db.find_history(name)
    return bottle.template('templates/history.tpl', history=history, name=name, **globals())

@bottle.get('/page/<name>/history/<dt>')
def page_historical(name, dt):
    is_read_page = True
    page = db.get_historical_page(name, dt)
    if not page:
        bottle.redirect(from_root('/page/{}', name))
    page_title = 'Reading {} as it appeared on {}'.format(name, dt)
    content = format_pandoc(page[1])
    return bottle.template('templates/read.tpl', **(dict(globals(), **locals())))

@bottle.post('/search')
def wiki_search():
    query = bottle.request.forms.getunicode('q')
    if not query:
        bottle.redirect(from_root('/'))

    def search_filter(page):
        return query in page[1] or query in page[2]
    
    pages = filter(search_filter, db.get_pages())
    return bottle.template('templates/search.tpl', **(dict(globals(), **locals())))

@bottle.get('/maintenance/recreateDatabase')
def recreatedatabase():
    global db
    db.conn.close()
    os.unlink(DB_FILE)
    db = Database(DB_FILE)
    db.create_db()
    db.insert_page('Home', 'Welcome to the /HOME/ page.')

bottle.run(server='cgi', debug=True)
