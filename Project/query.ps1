Add-Type -Path "..\Project\System.Data.SQLite\2010\bin\System.Data.SQLite.dll" 
#initialising system.data.sqlite libraries
$con = New-Object -TypeName System.Data.SQLite.SQLiteConnection #creating new object connection
$con.ConnectionString = "DataSource=..\powershellDatabase.db" #showing the path to the database
$con.Open()
$sql = $con.CreateCommand()
$sql.CommandText = "SELECT * FROM test" #testing select queries
$adapter = New-Object -TypeName System.Data.SQLite.SQLiteDataAdapter $sql
$data = New-Object System.Data.DataSet
[void]$adapter.Fill($data)
$data.tables.rows #showing all data in $data