#!/usr/bin/env python


F = [   ('K_0_19_Att', 'float'), ('K_20_29_Att', 'float'),
        ('K_30_39_Att', 'float'), ('K_40_49_Att', 'float'),
        ('K_50_Att', 'float'), ('K_0_19_made', 'float'),
        ('K_20_29_made', 'float'), ('K_30_39_made', 'float'),
        ('K_40_49_made', 'float'), ('K_50_made', 'float'),
        ('K_FGA', 'float'), ('K_FGM', 'float'), ('K_Lng', 'float'),
        ('K_FG_PCT', 'float'), ('K_Pts', 'float'), ('K_XPA', 'float'),
        ('K_XPM', 'float'),
        ('KR', 'float'), ('KR_Avg', 'float'),
        ('KR_Long', 'float'), ('KR_TD','float'), ('KR_Yds', 'float'),
        ('PASS_Att', 'float'), ('PASS_Comp', 'float'),
        ('PASS_Int', 'float'), ('PASS_Lng', 'float'),
        ('PASS_TD', 'float'), ('PASS_Yds', 'float'),
        ('PASS_YPA', 'float'),
        ('PR', 'float'), ('PR_Avg', 'float'), ('PR_Long', 'float'),
        ('PR_TD', 'float'), ('PR_Yds', 'float'),
        ('Rec', 'float'), ('REC_Lng', 'float'), ('REC_TD', 'float'),
        ('REC_Tgt', 'float'), ('REC_Yds', 'float'), ('REC_YPR', 'float'),
        ('RUN_Att', 'float'), ('RUN_Lng', 'float'), ('RUN_TD', 'float'),
        ('RUN_Yds', 'float'), ('RUN_YPA', 'float'),
        ('Sack', 'float'), ('SackYds', 'float'),
        ('Fum', 'float'), ('FumLost', 'float') ]

def create_sql():
    s = "CREATE TABLE \"AGG_STATS\" (\n"
    s += "\t\"PID\" char(9) NOT NULL DEFAULT '',\n"
    s += "\t\"Rating\" float DEFAULT NULL,\n"
    for (f, t) in F:
        s += "\t\"%s\" %s DEFAULT NULL,\n" % (f, t)
    s += "\tPRIMARY KEY(\"PID\"),\n"
    s += "\tCONSTRAINT \"AGG_STATS_ibfk_1\" FOREIGN KEY (\"PID\") "
    s += "REFERENCES \"PLAYERS\" (\"PID\"));\n\n"
    print(s)
    return

def select_sql():
    s = "SELECT PID, Season, AVG(Rating) AS Rating,\n"
    fs = [ "SUM(%s) AS %s" % (f, f) for (f, _) in F]
    s += ', '.join(fs) + "\nFROM STATS\n"
    s += "WHERE Season >= 2008 AND Season <= 2013\n"
    s += "GROUP BY Season, PID"
    return s

def insert_sql(sel):
    s = "INSERT INTO \"AGG_STATS\""
    fs = ['PID', 'Rating'] + [ "\"%s\"" % f for (f, _) in F ]
    s += "(" + ', '.join(fs) + ")\n"
    s += "SELECT PID, AVG(Rating),\n"
    fs = [ "AVG(%s)" % f for (f, _) in F ]
    s += ', '.join(fs) + " FROM (\n\n"
    s += sel + "\n\n"
    s += ") AS T GROUP BY PID;\n"
    print(s)

fix = """
-- Insert missing player records in AGG_STATS
INSERT INTO "AGG_STATS" (PID)
SELECT P.PID
FROM PLAYERS AS P LEFT OUTER JOIN AGG_STATS AS A ON P.PID = A.PID
WHERE A.PID IS NULL;
"""
def fix_sql():
    print fix
    return

def main():
    create_sql()
    s = select_sql()
    insert_sql(s)
    fix_sql()

if __name__ == '__main__':
    main()
