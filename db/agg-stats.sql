-- Aggregrate stats table
CREATE TABLE "AGG_STATS" (
    "PID" char(9) NOT NULL DEFAULT '',
    "Rating" float DEFAULT NULL,
    "PASS_Att" int(11) DEFAULT NULL,
    "PASS_Comp" int(11) DEFAULT NULL,
    "PASS_TD" int(11) DEFAULT NULL,
    "PASS_Yds" int(11) DEFAULT NULL,
    "RUN_Att" int(11) DEFAULT NULL,
    "RUN_Lng" int(11) DEFAULT NULL,
    "RUN_TD" int(11) DEFAULT NULL,
    "RUN_Yds" int(11) DEFAULT NULL,
    PRIMARY KEY("PID"),
    CONSTRAINT "AGG_STATS_ibfk_1" FOREIGN KEY ("PID") REFERENCES "PLAYERS" ("PID")
);

-- Insert aggregrate stats of last 6 seasons of players.
INSERT INTO "AGG_STATS"
SELECT PID, AVG(Rating), AVG(PASS_Att), AVG(PASS_Comp),
       AVG(PASS_TD), AVG(PASS_Yds), AVG(RUN_Att),
       AVG(RUN_Lng), AVG(RUN_TD), AVG(RUN_Yds) FROM
         (
            SELECT PID, Season, AVG(Rating) AS Rating,
            SUM(PASS_Att) AS PASS_Att, SUM(PASS_Comp) AS PASS_Comp,
            SUM(PASS_TD) AS PASS_TD, SUM(PASS_Yds) AS PASS_Yds,
            SUM(RUN_Att) AS RUN_Att, SUM(RUN_Lng) AS RUN_Lng,
            SUM(RUN_TD) AS RUN_TD, SUM(RUN_Yds) AS RUN_Yds FROM STATS
            WHERE Season >= 2008 AND Season <= 2013
            GROUP BY Season, PID
        ) AS T
       GROUP BY PID;

-- Insert missing player records in AGG_STATS
INSERT INTO "AGG_STATS" (PID)
SELECT P.PID
FROM PLAYERS AS P LEFT OUTER JOIN AGG_STATS AS A ON P.PID = A.PID
WHERE A.PID IS NULL;
