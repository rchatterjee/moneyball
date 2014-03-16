/*
 * load.cpp
 *
 *  Created on: Nov 13, 2013
 *      Author: Saikat R. Gomes
 *      saikat@cs.wisc.edu
 *      CS 564 sec1
 */
#include "load.h"

int main(void) {
	int returnCode;
	if (!createTableList()) {
		std::cout << "ERROR: Files reading failure!"
				<< "... loading terminating with fatal error!!!";
		return -1;
	}
	returnCode = sqlite3_open(DB_NAME, &db_Connection);
	if (returnCode) {
		std::cout << "ERROR: " << sqlite3_errmsg(db_Connection);
		sqlite3_close(db_Connection);
		return -1;
	}
	std::cout << "INFO: Sqlite3 database created: " << DB_NAME;
	std::cout << "\n\nINFO: Creating tables ...";
	if (!createTables()) {
		std::cout << "ERROR: Table creation failure!"
				<< "... loading terminating with fatal error!!!";
		return -1;
	}
	std::cout << "\n\nINFO: " << tableList.size()
			<< " tables created successfully.";
	std::cout << "\n\nINFO: Inserting records ...";
	if (!insertRecords()) {
		std::cout << "ERROR: Record insertion failure!"
				<< "... loading terminating with fatal error!!!";
		return -1;
	}
	sqlite3_close(db_Connection);
	std::cout << "\n\nINFO: Records inserted successfully.";
	std::cout
			<< "\n\nINFO: Load operation completed successfully ... terminating.\n";
	return 0;
}
//create the tables agnostically
bool createTables() {
	bool isSuccess = true;
	char *errMsg = 0;
	int returnCode;

	returnCode = sqlite3_exec(db_Connection, BEG_TRANS, NULL, NULL, &errMsg);
	if (returnCode != SQLITE_OK) {
		isSuccess = false;
		sqlite3_free(errMsg);
	}
	returnCode = sqlite3_exec(db_Connection, FK_ON, NULL, NULL, &errMsg);
	if (returnCode != SQLITE_OK) {
		isSuccess = false;
		sqlite3_free(errMsg);
	}

	for (unsigned int listIndex = 0; listIndex < tableList.size(); listIndex++) {

		tableDef newTable = tableList.at(listIndex);
		std::string tName = newTable.tableName;
		sqlite3_exec(db_Connection, sqlStatement(DROP_TBL + tName), NULL, NULL,
				&errMsg);
		std::string createStatement = CREATE_TBL + tName + " (";
		for (unsigned int colIndex = 0; colIndex < newTable.colNames.size(); colIndex++) {
			createStatement += newTable.colNames.at(colIndex) + " " + getType(
					newTable.colType.at(colIndex)) + ",";
		}
		createStatement += " " + PK + " (";
		for (unsigned int pkColIndex = 0; pkColIndex
				< newTable.primaryKeyIndexList.size(); pkColIndex++) {
			createStatement += newTable.colNames.at(
					newTable.primaryKeyIndexList.at(pkColIndex));
			if (pkColIndex < newTable.primaryKeyIndexList.size() - 1) {
				createStatement += ",";
			}
		}
		createStatement += ")";

		if (newTable.foreignKeyIndexList.size() > 0) {
			createStatement += ",";
			for (unsigned int fkColIndex = 0; fkColIndex
					< newTable.foreignKeyIndexList.size(); fkColIndex++) {
				createStatement += FK + " (" + newTable.colNames.at(
						newTable.foreignKeyIndexList.at(fkColIndex)) + ") "
						+ REF + newTable.colConstaints.at(
						newTable.foreignKeyIndexList.at(fkColIndex));
				if (fkColIndex < newTable.foreignKeyIndexList.size() - 1) {
					createStatement += ",";
				}
			}
		}

		createStatement += ");";
		std::cout << "\n      -> " << createStatement;
		returnCode = sqlite3_exec(db_Connection, sqlStatement(createStatement),
				NULL, NULL, &errMsg);
		if (returnCode != SQLITE_OK) {
			isSuccess = false;
			sqlite3_free(errMsg);
		}
	}

	returnCode = sqlite3_exec(db_Connection, CMT_TXN, NULL, NULL, &errMsg);
	if (returnCode != SQLITE_OK) {
		isSuccess = false;
		sqlite3_free(errMsg);
	}
	return isSuccess;
}

//insert records
bool insertRecords() {
	bool isSuccess = true;
	int counter = 0;
	char *errMsg = 0;
	int returnCode;

	for (unsigned int listIndex = 0; listIndex < tableList.size(); listIndex++) {
		returnCode
				= sqlite3_exec(db_Connection, BEG_TRANS, NULL, NULL, &errMsg);
		if (returnCode != SQLITE_OK) {
			isSuccess = false;
			sqlite3_free(errMsg);
		}
		counter = 0;
		tableDef newTable = tableList.at(listIndex);
		std::string tableName = newTable.tableName;
		std::string fileName = newTable.fileName;
		std::cout << "\n      -> Inserting records in " << tableName;
		std::ifstream inFile;
		inFile.open(newTable.fileName.c_str());
		if (!inFile.fail()) {
			int linecount = 0;
			std::string line;
			getline(inFile, line);
			getline(inFile, line);
			getline(inFile, line);
			getline(inFile, line);
			getline(inFile, line);
			std::string createStatement;
			linecount = 5;
			while (getline(inFile, line)) {
				linecount++;
				std::stringstream ssLine(line);
				unsigned int attCount = 0;
				std::string holder = "";
				createStatement = "INSERT INTO " + tableName + " VALUES (";
				while (ssLine.good()) {
					std::string substr;
					std::string value;
					getline(ssLine, substr, ',');
					if (QUOTE.compare(substr.substr(0, 1)) == 0
							&& holder.compare("") == 0) {
						holder = substr;
						continue;
					} else if (holder.compare("") != 0) {
						holder += "," + substr;
						if (substr.substr(substr.size() - 1, 1).compare(QUOTE)
								== 0) {
							substr = holder;
							substr.erase(substr.size() - 1, 1);
							substr.erase(0, 1);
							holder = "";
						} else {
							continue;
						}
					}
					value = getValue(substr, newTable.colType.at(attCount));
					createStatement += value;
					if (attCount < newTable.colType.size() - 1) {
						createStatement += ",";
					}
					attCount++;
				}
				createStatement += ");";
				counter++;
				returnCode = sqlite3_exec(db_Connection, sqlStatement(
						createStatement), NULL, NULL, &errMsg);
				if (returnCode != SQLITE_OK) {
					std::cout << "\n        -X Failed to insert records in "
							<< tableName;
					std::cout << "\n        -X " << linecount << "- "
							<< createStatement;
					isSuccess = false;
					sqlite3_free(errMsg);
				}
			}

		} else {
			std::cout << "ERROR: loading file failed!";
			isSuccess = false;
		}
		inFile.close();

		returnCode = sqlite3_exec(db_Connection, CMT_TXN, NULL, NULL, &errMsg);
		if (returnCode != SQLITE_OK) {
			isSuccess = false;
			sqlite3_free(errMsg);
		} else {
			std::cout << " ... [" << counter << " record(s) inserted]";
		}
	}
	return isSuccess;
}

//given a raw text get the formatted data based on att type
std::string getValue(std::string rawValue, int type) {
	std::string formattedValue;

	if (rawValue.size() > 0 && rawValue.substr(rawValue.size() - 1, 1).compare(
			"\r") == 0) {
		rawValue.erase(rawValue.size() - 1, 1);
	}
	if (rawValue.compare("") == 0) {
		return "NULL";
	}
	std::size_t found = rawValue.find("'");
	while (found != std::string::npos) {
		rawValue.insert(found, "\'");
		if (found == rawValue.size() - 1) {
			found = std::string::npos;
		} else {
			found = rawValue.find("'", found + 2);
		}
	}
	if (type == 2) {
		formattedValue = "\'" + rawValue + "\'";
	} else {
		formattedValue = rawValue;
		if (formattedValue.compare("X") == 0) {
			formattedValue = "NULL";
		}
	}
	return formattedValue;
}

//create internal data structures to create tables later
bool createTableList() {
	bool isSuccess = true;
	DIR *pDIR;
	struct dirent *entry;
	if (pDIR = opendir(DATA_DIR_LOCATION.c_str())) {
		while (entry = readdir(pDIR)) {
			std::string fileName = entry->d_name;
			if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..")
					!= 0 && strstr(entry->d_name, DOT_TXT.c_str()) != NULL) {
				tableDef* newTable = new tableDef();
				newTable->fileName = DATA_DIR_LOCATION + "/" + fileName;
				std::ifstream inFile;
				inFile.open(newTable->fileName.c_str());
				if (!inFile.fail()) {
					for (int LineNumber = 0; LineNumber < 5; LineNumber++) {
						std::string line;
						getline(inFile, line);
						boost::to_upper(line);
						std::stringstream ssLine(line);
						while (ssLine.good()) {
							std::string substr;
							getline(ssLine, substr, ',');
							if (LineNumber == 0) {
								newTable->tableName = substr;
								break;
							} else if (LineNumber == 1) {
								newTable->colNames.push_back(substr);
							} else if (LineNumber == 2) {
								int tType = atoi(substr.c_str());
								newTable->colType.push_back(tType);
							} else if (LineNumber == 3) {
								int tKeyType = atoi(substr.c_str());
								newTable->colKeyType.push_back(tKeyType);
								if (tKeyType == 1 || tKeyType == 4) {
									newTable->primaryKeyIndexList.push_back(
											newTable->colKeyType.size() - 1);
								}
								if (tKeyType == 2 || tKeyType == 3 || tKeyType
										== 4) {
									newTable->foreignKeyIndexList.push_back(
											newTable->colKeyType.size() - 1);
								}
							} else if (LineNumber == 4) {
								newTable->colConstaints.push_back(substr);
							}
						}
					}
				} else {
					std::cout << "ERROR: loading file failed!";
					isSuccess = false;
				}
				inFile.close();
				tableList.push_back(*newTable);
				delete newTable;
			}
		}
		closedir(pDIR);
		reorderTableList();
	} else {
		std::cout << "ERROR: Cannot Open Dir!\n";
		isSuccess = false;
	}
	return isSuccess;
}

//reorder the tables so that tables with no fk is created first
void reorderTableList() {
	std::vector<tableDef> priorityTableList;
	std::vector<tableDef> otherTableList;
	for (unsigned int listIndex = 0; listIndex < tableList.size(); listIndex++) {
		tableDef newTable = tableList.at(listIndex);
		if (newTable.foreignKeyIndexList.size() == 0) {
			priorityTableList.push_back(newTable);
		} else {
			otherTableList.push_back(newTable);
		}
	}
	tableList.clear();
	for (unsigned int priorityListIndex = 0; priorityListIndex
			< priorityTableList.size(); priorityListIndex++) {
		tableList.push_back(priorityTableList.at(priorityListIndex));
	}
	for (unsigned int otherListIndex = 0; otherListIndex
			< otherTableList.size(); otherListIndex++) {
		tableList.push_back(otherTableList.at(otherListIndex));
	}
	priorityTableList.clear();
	otherTableList.clear();
}

//get a sql string
const char *sqlStatement(const std::string sqlStr) {
	return sqlStr.c_str();
}

//get attribute tupe
std::string getType(int type) {
	std::string typeStr;
	if (type == 0) {
		typeStr = "INTEGER";
	} else if (type == 1) {
		typeStr = "REAL";
	} else {
		typeStr = "TEXT";
	}
	return typeStr;
}
