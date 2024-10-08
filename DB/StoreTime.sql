USE [GreatLakesWaterLevels]
GO
/****** Object:  StoredProcedure [dbo].[StoreTime]    Script Date: 8/26/2024 11:13:27 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[StoreTime]
	@StationId NVARCHAR(30),
	@Date DATETIME, 
	@V NVARCHAR(20), 
	@S NVARCHAR(20), 
	@F NVARCHAR(5), 
	@Q NVARCHAR(5)
AS 
BEGIN 
	SET NOCOUNT ON;
	IF @StationId is null
		BEGIN 
			RAISERROR('StationId cannot be NULL', 16, 1)
			RETURN 
		END

	IF @Date is null
		BEGIN 
			RAISERROR('Date cannot be NULL', 16, 1) 
			RETURN 
		END

	BEGIN TRY
		BEGIN TRANSACTION; 
		DECLARE @TableName NVARCHAR(30)
		SET @TableName = (SELECT StationName FROM StationsId WHERE @StationId = StationId);


		IF OBJECT_ID(QUOTENAME(@TableName), 'U') is null
			BEGIN 
				--Create new table for station
				DECLARE @SQL NVARCHAR(MAX) 
				SET @SQL = 'CREATE TABLE ' + QUOTENAME(@TableName) + ' (
					Date DATETIME, 
					V NVARCHAR(20), 
					S NVARCHAR(20), 
					F NVARCHAR(10), 
					Q NVARCHAR(5)
				);'
				EXEC sp_executesql @SQL, N'@TableName NVARCHAR(30)', @TableName
				
				--Add info to new table
				SET @SQL = 'INSERT INTO ' + QUOTENAME(@TableName) + ' VALUES (@Date, @V, @S, @f, @Q)'
				EXEC sp_executesql @SQL, N'@Date NVARCHAR(30), @V NVARCHAR(20), @S NVARCHAR(20), @F NVARCHAR(10), @Q NVARCHAR(5)', @Date, @V, @S, @F, @Q

			END;
		ELSE
			BEGIN
				--Add info to exsisting table
				DECLARE @SQL2 NVARCHAR(MAX) 
				SET @SQL2 = 'INSERT INTO ' + QUOTENAME(@TableName) + ' VALUES (@Date, @V, @S, @f, @Q)'
				EXEC sp_executesql @SQL2, N'@Date NVARCHAR(30), @V NVARCHAR(20), @S NVARCHAR(20), @F NVARCHAR(10), @Q NVARCHAR(5)', @Date, @V, @S, @F, @Q
			END;
	COMMIT TRANSACTION;
	END TRY 
	BEGIN CATCH
		ROLLBACK TRANSACTION;
		THROW; 
	END CATCH 
END;