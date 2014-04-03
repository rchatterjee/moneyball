#!/usr/bin/env python
import os, sys
from django.utils import timezone
from threading import Timer
"""
monitors all the upcoming events e.g. start-draft, draft-timeout, finish-draft
and poke the server to take action agains
"""

class EventTracker:
    def __init__(self):
        self.event_queue = []
        self.next_poke = 300  # 5 minutes
        self.update_event_queue()

    def take_action_start_draft(self):
        print "TAKEACTION_START_DRAFT:", self.event_queue
        self.update_event_queue()
        if not self.event_queue:
            Timer(300.0, self.take_action_start_draft).start()
            return
        e = self.event_queue[-1]
        if not e: 
            return take_action_start_draft()

        c_time = timezone.now()
        t_diff = (c_time - e['timeout'])
        
        if t_diff.total_seconds() > 0:
            l = League.objects.get(pk=e['league_id'])
            if l:
                "Starting Draft for:", l, '@', c_time
                if l.start_draft():
                    l.timeout()
            del self.event_queue[-1]
            return self.take_action_start_draft()
        else:
            print t_diff.total_seconds()
            Timer(t_diff.total_seconds(), self.take_action_start_draft).start()
        return 
        

    def update_event_queue(self):
        c_time = timezone.now()
        next_1_hr = c_time + timezone.timedelta(hours=1)
        print "One Hr Ahead:", c_time, next_1_hr
        next_drafts = League.objects.filter((Q(settings__draft_date__lt=next_1_hr) & Q(settings__draft_date__gt=c_time)) 
                                            | (Q(draft_timeout__lt=next_1_hr) & Q(draft_timeout__gt=c_time))) \
                                            .order_by('settings__draft_date').values('id', 'settings__draft_date', 'draft_timeout')
        events = []
        for n in next_drafts:
            if n not in self.event_queue:
                events.append({'league_id': n['id'], 'timeout': n['settings__draft_date']})

        self.event_queue.extend(events)
        self.event_queue.sort(key=lambda x: x['timeout'], reverse=True)
        print "eventQ:", self.event_queue


        
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ffball.settings")
    # settings.configure()
    from league.models import *
    from team import *

    bot = EventTracker()
    bot.take_action_start_draft()
