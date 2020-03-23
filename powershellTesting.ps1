Add-Type -Path "C:\Program Files\System.Data.SQLite\2010\bin\System.Data.SQLite.dll"
$con = New-Object -TypeName System.Data.SQLite.SQLiteConnection
$con.ConnectionString = "DataSource=powershellDatabase.db"
$con.Open()
$sql = $con.CreateCommand()
$sql.CommandText = "INSERT INTO test (message) VALUES (@message)";
$sql.Parameters.AddWithValue("@message", "asdaasdda");
$sql.ExecuteNonQuery();
$sql.CommandText = "SELECT * FROM test"
$adapter = New-Object -TypeName System.Data.SQLite.SQLiteDataAdapter $sql
$data = New-Object System.Data.DataSet
[void]$adapter.Fill($data)
$data.tables.rows
