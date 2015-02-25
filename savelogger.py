import json
import urllib
import urllib2
import getpass
import sublime_plugin

DEBUG_LEVEL = 0

API_KEY = "NONE"
API_URL = "http://logger.hakama.keikogi.ru/api/post"

class SaveLogger(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if not view.is_dirty():
            return

        currently_view = []
        for item in view.window().views():
            currently_view.append({
                'name': item.file_name(),
                'encoding': item.encoding(),
                'size': item.size(),
                'syntax': item.settings().get('syntax'),
            })

        data_container = {
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

        result_container = {
            'data': json.dumps(data_container),
            'api_key': API_KEY
        }

        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL))
        data = urllib.urlencode(result_container)

        try:
            opener.open(API_URL, data=data)
        except urllib2.HTTPError:
            print 'Sending error'
