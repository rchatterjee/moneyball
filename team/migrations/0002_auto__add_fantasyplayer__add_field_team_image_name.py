# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FantasyPlayer'
        db.create_table(u'team_fantasyplayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Player'])),
            ('position', self.gf('django.db.models.fields.CharField')(default='FLEX', max_length=4, null=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team.Team'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'team', ['FantasyPlayer'])

        # Adding field 'Team.image_name'
        db.add_column(u'team_team', 'image_name',
                      self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field watch_list on 'Team'
        m2m_table_name = db.shorten_name(u'team_team_watch_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'team.team'], null=False)),
            ('player', models.ForeignKey(orm[u'data.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['team_id', 'player_id'])


    def backwards(self, orm):
        # Deleting model 'FantasyPlayer'
        db.delete_table(u'team_fantasyplayer')

        # Deleting field 'Team.image_name'
        db.delete_column(u'team_team', 'image_name')

        # Removing M2M table for field watch_list on 'Team'
        db.delete_table(db.shorten_name(u'team_team_watch_list'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.player': {
            'Meta': {'object_name': 'Player', 'db_table': "u'PLAYERS'", 'managed': 'False'},
            'cbsid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'CBSID'", 'blank': 'True'}),
            'espnid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'ESPNID'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "u'Name'", 'blank': 'True'}),
            'other_teams': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "u'Other_Teams'", 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True', 'db_column': "u'PID'"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_column': "u'Position'", 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Team']", 'null': 'True', 'db_column': "u'TID'", 'blank': 'True'}),
            'yahooid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'YAHOOID'", 'blank': 'True'})
        },
        u'data.team': {
            'Meta': {'object_name': 'Team', 'db_table': "u'TEAMS'", 'managed': 'False'},
            'active_since': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'ACTIVE_SINCE'", 'blank': 'True'}),
            'cbsid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'CBSID'", 'blank': 'True'}),
            'espnid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'ESPNID'", 'blank': 'True'}),
            'games_played': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'GAMES_PLAYED'", 'blank': 'True'}),
            'home': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "u'HOME'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'NAME'", 'blank': 'True'}),
            'overall_losses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'OVERALL_LOSSES'", 'blank': 'True'}),
            'overall_ties': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'OVERALL_TIES'", 'blank': 'True'}),
            'overall_wins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'OVERALL_WINS'", 'blank': 'True'}),
            'pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "u'PCT'", 'blank': 'True'}),
            'post_losses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'POST_LOSSES'", 'blank': 'True'}),
            'post_wins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'POST_WINS'", 'blank': 'True'}),
            'reg_losses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'REG_LOSSES'", 'blank': 'True'}),
            'reg_ties': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'REG_TIES'", 'blank': 'True'}),
            'reg_wins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'REG_WINS'", 'blank': 'True'}),
            'tid': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True', 'db_column': "u'TID'"}),
            'yahooid': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'YAHOOID'", 'blank': 'True'})
        },
        u'league.league': {
            'Meta': {'object_name': 'League'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'league_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '15', 'blank': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.League_Settings']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.Vendor']"})
        },
        u'league.league_settings': {
            'BLKKRTD': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'FG40': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'FGM': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'FRTD': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'FUML': ('django.db.models.fields.IntegerField', [], {'default': '-2'}),
            'INT': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'INTTD': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'KRTD': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'Meta': {'object_name': 'League_Settings'},
            'P2PC': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'P2REC': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'PA1': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'PA14': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'PA35': ('django.db.models.fields.IntegerField', [], {'default': '-3'}),
            'PRTD': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'PTD': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'REC': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'RTD': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'SF': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'YA100': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'YA299': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'YA449': ('django.db.models.fields.IntegerField', [], {'default': '-3'}),
            'YA549': ('django.db.models.fields.IntegerField', [], {'default': '-6'}),
            'benched': ('django.db.models.fields.IntegerField', [], {'default': '9'}),
            'count_FLEX_max': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'count_FLEX_min': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'count_K_max': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'count_K_min': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'count_QB_max': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'count_QB_min': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'count_RB_max': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'count_RB_min': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'count_TE_max': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'count_TE_min': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'count_WR_max': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'count_WR_min': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'draft_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'draft_order': ('django.db.models.fields.CharField', [], {'default': "u'Randomized 1 Hour Prior to DraftTime'", 'max_length': '50'}),
            'draft_type': ('django.db.models.fields.CharField', [], {'default': "u'S'", 'max_length': '1'}),
            'home_field_advantage': ('django.db.models.fields.CharField', [], {'default': "u'None'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft_done': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'league_type': ('django.db.models.fields.CharField', [], {'default': "u'STD'", 'max_length': '3'}),
            'lineup_changes': ('django.db.models.fields.CharField', [], {'default': "u'Lock Individually at Scheduled Gametime'", 'max_length': '50'}),
            'matchup_tie_breaker': ('django.db.models.fields.CharField', [], {'default': "u'None'", 'max_length': '20'}),
            'number_of_teams': ('django.db.models.fields.IntegerField', [], {'default': '12', 'null': 'True', 'blank': 'True'}),
            'plaoff_byes': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'player_acquisition_system': ('django.db.models.fields.CharField', [], {'default': "u'Waivers'", 'max_length': '20'}),
            'player_universe': ('django.db.models.fields.CharField', [], {'default': "u'All NFL Players'", 'max_length': '20'}),
            'playoff_home_field_advantage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'playoff_rounds': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'playoff_seeding_tie_breaker': ('django.db.models.fields.CharField', [], {'default': "u'Total Points For'", 'max_length': '20'}),
            'playoff_teams': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'regular_season_matchups': ('django.db.models.fields.IntegerField', [], {'default': '13'}),
            'scoring_type': ('django.db.models.fields.CharField', [], {'default': "u'Head to Head Points'", 'max_length': '30'}),
            'season_acquisition_limit': ('django.db.models.fields.CharField', [], {'default': "u'No Limit'", 'max_length': '20'}),
            'seconds_per_pick': ('django.db.models.fields.IntegerField', [], {'default': '120'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '12'}),
            'start_of_regular_season': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'starters': ('django.db.models.fields.IntegerField', [], {'default': '16'}),
            'trade_deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'trade_limit': ('django.db.models.fields.CharField', [], {'default': "u'No Limit'", 'max_length': '20'}),
            'trade_review_period': ('django.db.models.fields.CharField', [], {'default': "u'2 Days'", 'max_length': '20'}),
            'use_keepers_for_2013_season': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_keepers_for_2014_season': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'votes_required_to_veto_trade': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'waiver_order': ('django.db.models.fields.CharField', [], {'default': "u'Move to last after claim'", 'max_length': '40'}),
            'waiver_period': ('django.db.models.fields.CharField', [], {'default': "u'1 Day'", 'max_length': '20'}),
            'weeks_per_matchup': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'weeks_per_playoff_matchup': ('django.db.models.fields.CharField', [], {'default': "u'1 week per round'", 'max_length': '20'})
        },
        u'league.vendor': {
            'Meta': {'object_name': 'Vendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'team.fantasyplayer': {
            'Meta': {'object_name': 'FantasyPlayer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Player']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'FLEX'", 'max_length': '4', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['team.Team']"})
        },
        u'team.team': {
            'Meta': {'object_name': 'Team'},
            'division': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'draft_pick_number': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'is_commisionar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.League']"}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vendor_team_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'vendor_user_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'waiver_priority': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'watch_list': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'team_watchlist'", 'symmetrical': 'False', 'to': u"orm['data.Player']"})
        }
    }

    complete_apps = ['team']