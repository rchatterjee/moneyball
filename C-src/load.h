/*
 * load.h
 *
 *  Created on: Nov 18, 2013
 *      Author: saikat
 */

#pragma once

#include <iostream>
#include <string>
#include "string.h"
#include <sstream>
#include <stdio.h>
#include <cstdlib>
#include <iostream>
#include <string.h>
#include <fstream>
#include <dirent.h>
#include <vector>
#include <fstream>
#include <stdlib.h>
#include <boost/algorithm/string.hpp>
#include <sqlite3.h>

//this structure stores all the info required to create a table
struct tableDef {
	std::string tableName;
	std::string fileName;
	std::vector<std::string> colNames;
	std::vector<std::string> colConstaints;
	std::vector<int> colType;
	std::vector<int> colKeyType;
	std::vector<int> primaryKeyIndexList;
	std::vector<int> foreignKeyIndexList;
};

std::string DATA_DIR_LOCATION = ".";
//std::string DATA_DIR_LOCATION = "./";
std::string DOT_TXT = ".dat";
const char* DB_NAME = "census.db";
const char* BEG_TRANS = "BEGIN TRANSACTION";
const char* FK_ON = "PRAGMA foreign_keys = ON";
const char* DROP_TBL = "DROP TABLE IF EXISTS ";
const char* CREATE_TBL = "CREATE TABLE ";
const char* CMT_TXN = "COMMIT TRANSACTION";
const std::string PK = "PRIMARY KEY";
const std::string FK = "FOREIGN KEY";
const std::string REF = "REFERENCES ";
const std::string QUOTE = "\"";
std::vector<tableDef> tableList;
const int TXN_LIMIT = 1000;

sqlite3 *db_Connection;

void printTableList();
bool createTableList();
void reorderTableList();
bool createTables();
bool insertRecords();
const char *sqlStatement(const std::string sqlStr);
std::string getType(int type);
std::string getValue(std::string rawValue, int type);

