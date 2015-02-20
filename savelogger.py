import json
import urllib2
import getpass
import sublime_plugin

API_URL = "http://logger.hakama.keikogi.ru/api/post"

class SaveLogger(sublime_plugin.EventListener):
    def on_post_save(self, view):
        currently_view = []
        for item in view.window().views():
            currently_view.append({
                'name': item.file_name(),
                'encoding': item.encoding(),
                'size': item.size(),
                'syntax': item.settings().get('syntax'),
            })

        result = {
            'username': getpass.getuser(),
            'files': currently_view,
            'current_file': {
                'name': view.file_name(),
                'encoding': view.encoding(),
                'size': view.size(),
                'syntax': view.settings().get('syntax'),
            },
            'folders': view.window().folders(),
            'current_folder': view.window().active_group(),
            'history': view.command_history(-1),
        }

        req = urllib2.Request(API_URL + '?data=' + json.dumps(result))

        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError:
            print 'Sending error.'
