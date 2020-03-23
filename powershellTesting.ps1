Add-Type -Path "C:\Program Files\System.Data.SQLite\2010\bin\System.Data.SQLite.dll"
$con = New-Object -TypeName System.Data.SQLite.SQLiteConnection
$con.ConnectionString = "DataSource=C:\Users\danie\Desktop\13DTP\powershellDatabase.db"
$con.Open()
$sql = $con.CreateCommand()
$sql.CommandText = "SELECT * FROM test"
$adapter = New-Object -TypeName System.Data.SQLite.SQLiteDataAdapter $sql
$data = New-Object System.Data.DataSet
[void]$adapter.Fill($data)
$data.tables.rows