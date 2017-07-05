import sqlite3

def CreateTable():
    conn = sqlite3.connect('good.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS Deposit;')
    c.execute('CREATE TABLE Deposit('
                  + 'IDDeposit INTEGER PRIMARY KEY AUTOINCREMENT, '
                  + 'DepositName TEXT)')
    c.execute('INSERT INTO Deposit(DepositName) '
                  + 'VALUES (\'Gold\');')
    c.execute('INSERT INTO Deposit(DepositName) '
                  + 'VALUES (\'Silver\');')
    c.execute('INSERT INTO Deposit(DepositName) '
                  + 'VALUES (\'Uranium\');')
    c.execute('DROP TABLE IF EXISTS Bush;')
    c.execute('CREATE TABLE Bush('
                  + 'IDBush INTEGER PRIMARY KEY AUTOINCREMENT, '
                  + 'BushName TEXT,'
                  + 'MotherDeposit int not null,'
                  + 'FOREIGN KEY (MotherDeposit) REFERENCES Field(IDDeposit));')
    
    c.execute('INSERT INTO Bush(BushName, MotherDeposit) '
                  + 'VALUES (\'Zelena\',\'Gold\');')

    c.execute('DROP TABLE IF EXISTS Well;')
    c.execute('CREATE TABLE Well('
                  + 'IDWell INTEGER PRIMARY KEY AUTOINCREMENT, '
                  + 'WellName TEXT,'
                  + 'MotherBush int not null,'
                  + 'FOREIGN KEY (MotherBush) REFERENCES Field(IDBush));')
    
    c.execute('INSERT INTO Well(WellName, MotherBush) '
                  + 'VALUES (\'NameForWell\',\'Zelena\');')
    
    c.execute('DROP TABLE IF EXISTS Dll;')
    
    c.execute('CREATE TABLE Dll('
                  + 'IDDll INTEGER PRIMARY KEY AUTOINCREMENT, '
                  + 'DllName TEXT,'
                  + 'DllPath TEXT,'
                  + 'MotherWell int not null,'
                  + 'FOREIGN KEY (MotherWell) REFERENCES Field(IDWell));')

    c.execute('INSERT INTO Dll(DllName, DllPath, MotherWell) '
                  + 'VALUES (\'NameForDll\', \'None\', \'NameForWell\');')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    CreateTable()
