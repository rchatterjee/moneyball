# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Player(models.Model):
    pid = models.CharField(db_column='PID', primary_key=True, max_length=10) # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True) # Field name made lowercase.
    team = models.ForeignKey('Team', db_column='TID', blank=True, null=True) # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=2, blank=True) # Field name made lowercase.
    other_teams = models.CharField(db_column='Other_Teams', max_length=100, blank=True) # Field name made lowercase.
    espnid = models.CharField(db_column='ESPNID', max_length=10, blank=True) # Field name made lowercase.
    yahooid = models.CharField(db_column='YAHOOID', max_length=10, blank=True) # Field name made lowercase.
    cbsid = models.CharField(db_column='CBSID', max_length=10, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'PLAYERS'

class Stat(models.Model):
    fum = models.IntegerField(db_column='Fum', blank=True, null=True) # Field name made lowercase.
    fumlost = models.IntegerField(db_column='FumLost', blank=True, null=True) # Field name made lowercase.
    k_0_19_att = models.IntegerField(db_column='K_0_19_Att', blank=True, null=True) # Field name made lowercase.
    k_20_29_att = models.IntegerField(db_column='K_20_29_Att', blank=True, null=True) # Field name made lowercase.
    k_30_39_att = models.IntegerField(db_column='K_30_39_Att', blank=True, null=True) # Field name made lowercase.
    k_40_49_att = models.IntegerField(db_column='K_40_49_Att', blank=True, null=True) # Field name made lowercase.
    k_50_att = models.IntegerField(db_column='K_50_Att', blank=True, null=True) # Field name made lowercase.
    k_0_19_made = models.IntegerField(db_column='K_0_19_made', blank=True, null=True) # Field name made lowercase.
    k_20_29_made = models.IntegerField(db_column='K_20_29_made', blank=True, null=True) # Field name made lowercase.
    k_30_39_made = models.IntegerField(db_column='K_30_39_made', blank=True, null=True) # Field name made lowercase.
    k_40_49_made = models.IntegerField(db_column='K_40_49_made', blank=True, null=True) # Field name made lowercase.
    k_50_made = models.IntegerField(db_column='K_50_made', blank=True, null=True) # Field name made lowercase.
    k_fga = models.IntegerField(db_column='K_FGA', blank=True, null=True) # Field name made lowercase.
    k_fgm = models.IntegerField(db_column='K_FGM', blank=True, null=True) # Field name made lowercase.
    k_lng = models.IntegerField(db_column='K_Lng', blank=True, null=True) # Field name made lowercase.
    k_fg_pct = models.FloatField(db_column='K_FG_PCT', blank=True, null=True) # Field name made lowercase.
    k_pts = models.IntegerField(db_column='K_Pts', blank=True, null=True) # Field name made lowercase.
    k_xpa = models.IntegerField(db_column='K_XPA', blank=True, null=True) # Field name made lowercase.
    k_xpm = models.IntegerField(db_column='K_XPM', blank=True, null=True) # Field name made lowercase.
    kr = models.IntegerField(db_column='KR', blank=True, null=True) # Field name made lowercase.
    kr_avg = models.FloatField(db_column='KR_Avg', blank=True, null=True) # Field name made lowercase.
    kr_long = models.IntegerField(db_column='KR_Long', blank=True, null=True) # Field name made lowercase.
    kr_td = models.IntegerField(db_column='KR_TD', blank=True, null=True) # Field name made lowercase.
    kr_yds = models.IntegerField(db_column='KR_Yds', blank=True, null=True) # Field name made lowercase.
    pass_att = models.IntegerField(db_column='PASS_Att', blank=True, null=True) # Field name made lowercase.
    pass_comp = models.IntegerField(db_column='PASS_Comp', blank=True, null=True) # Field name made lowercase.
    pass_int = models.IntegerField(db_column='PASS_Int', blank=True, null=True) # Field name made lowercase.
    pass_lng = models.IntegerField(db_column='PASS_Lng', blank=True, null=True) # Field name made lowercase.
    pass_td = models.IntegerField(db_column='PASS_TD', blank=True, null=True) # Field name made lowercase.
    pass_yds = models.IntegerField(db_column='PASS_Yds', blank=True, null=True) # Field name made lowercase.
    pass_ypa = models.FloatField(db_column='PASS_YPA', blank=True, null=True) # Field name made lowercase.
    player = models.ForeignKey(Player, db_column='PID') # Field name made lowercase.
    pr = models.IntegerField(db_column='PR', blank=True, null=True) # Field name made lowercase.
    pr_avg = models.FloatField(db_column='PR_Avg', blank=True, null=True) # Field name made lowercase.
    pr_long = models.IntegerField(db_column='PR_Long', blank=True, null=True) # Field name made lowercase.
    pr_td = models.IntegerField(db_column='PR_TD', blank=True, null=True) # Field name made lowercase.
    pr_yds = models.IntegerField(db_column='PR_Yds', blank=True, null=True) # Field name made lowercase.
    rating = models.FloatField(db_column='Rating', blank=True, null=True) # Field name made lowercase.
    rec = models.IntegerField(db_column='Rec', blank=True, null=True) # Field name made lowercase.
    rec_lng = models.IntegerField(db_column='REC_Lng', blank=True, null=True) # Field name made lowercase.
    rec_td = models.IntegerField(db_column='REC_TD', blank=True, null=True) # Field name made lowercase.
    rec_tgt = models.IntegerField(db_column='REC_Tgt', blank=True, null=True) # Field name made lowercase.
    rec_yds = models.IntegerField(db_column='REC_Yds', blank=True, null=True) # Field name made lowercase.
    rec_ypr = models.FloatField(db_column='REC_YPR', blank=True, null=True) # Field name made lowercase.
    run_att = models.IntegerField(db_column='RUN_Att', blank=True, null=True) # Field name made lowercase.
    run_lng = models.IntegerField(db_column='RUN_Lng', blank=True, null=True) # Field name made lowercase.
    run_td = models.IntegerField(db_column='RUN_TD', blank=True, null=True) # Field name made lowercase.
    run_yds = models.IntegerField(db_column='RUN_Yds', blank=True, null=True) # Field name made lowercase.
    run_ypa = models.FloatField(db_column='RUN_YPA', blank=True, null=True) # Field name made lowercase.
    sack = models.IntegerField(db_column='Sack', blank=True, null=True) # Field name made lowercase.
    sackyds = models.IntegerField(db_column='SackYds', blank=True, null=True) # Field name made lowercase.
    season = models.IntegerField(db_column='Season') # Field name made lowercase.
    team = models.ForeignKey('Team', db_column='TID') # Field name made lowercase.
    week = models.IntegerField(db_column='Week') # Field name made lowercase.
    k_xp_pct = models.FloatField(db_column='K_XP_PCT', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'STATS'

class Team(models.Model):
    tid = models.CharField(db_column='TID', primary_key=True, max_length=3) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True) # Field name made lowercase.
    active_since = models.IntegerField(db_column='ACTIVE_SINCE', blank=True, null=True) # Field name made lowercase.
    reg_wins = models.IntegerField(db_column='REG_WINS', blank=True, null=True) # Field name made lowercase.
    reg_losses = models.IntegerField(db_column='REG_LOSSES', blank=True, null=True) # Field name made lowercase.
    reg_ties = models.IntegerField(db_column='REG_TIES', blank=True, null=True) # Field name made lowercase.
    post_wins = models.IntegerField(db_column='POST_WINS', blank=True, null=True) # Field name made lowercase.
    post_losses = models.IntegerField(db_column='POST_LOSSES', blank=True, null=True) # Field name made lowercase.
    overall_wins = models.IntegerField(db_column='OVERALL_WINS', blank=True, null=True) # Field name made lowercase.
    overall_losses = models.IntegerField(db_column='OVERALL_LOSSES', blank=True, null=True) # Field name made lowercase.
    overall_ties = models.IntegerField(db_column='OVERALL_TIES', blank=True, null=True) # Field name made lowercase.
    pct = models.FloatField(db_column='PCT', blank=True, null=True) # Field name made lowercase.
    games_played = models.IntegerField(db_column='GAMES_PLAYED', blank=True, null=True) # Field name made lowercase.
    cbsid = models.CharField(db_column='CBSID', max_length=10, blank=True) # Field name made lowercase.
    espnid = models.CharField(db_column='ESPNID', max_length=10, blank=True) # Field name made lowercase.
    yahooid = models.CharField(db_column='YAHOOID', max_length=10, blank=True) # Field name made lowercase.
    home = models.CharField(db_column='HOME', max_length=30, blank=True) # Field name made lowercase.
    
    def __str__(self):
        return ' '.join([str(v) for v in vars(self).values()])

    class Meta:
        managed = False
        db_table = 'TEAMS'

class User(models.Model):
    first_name = models.CharField(max_length=20, blank=True)
    last_name  = models.CharField(max_length=20, blank=True)
    username   = models.CharField(max_length=20, blank=True)
    
