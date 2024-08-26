USE [GreatLakesWaterLevels]
GO
/****** Object:  StoredProcedure [dbo].[ModifyStationsIdTable]    Script Date: 8/26/2024 11:13:21 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[ModifyStationsIdTable]
	@StationName NVARCHAR(50), 
	@StationId NVARCHAR(30)
AS 
BEGIN 
	SET NOCOUNT ON;
		IF @StationId is null
		BEGIN 
			RAISERROR('StationId cannot be NULL', 16, 1)
			RETURN 
		END

	IF @StationName is null
		BEGIN 
			RAISERROR('StationName cannot be NULL', 16, 1) 
			RETURN 
		END
	BEGIN 
		IF OBJECT_ID('StationsId', 'U') IS NULL
			BEGIN 
			--Create table if doesnt exsist
				CREATE TABLE StationsId (
					StationName NVARCHAR(50) NOT NULL, 
					StationId NVARCHAR(30) NOT NULL
				);
			--Insert Values to new table
				IF (SELECT StationId FROM StationsId WHERE StationName = @StationName) IS NULL
					BEGIN 
						INSERT INTO StationsId (StationName, StationId) VALUES (@StationName, @StationID) 
					END
			END
		ELSE
			BEGIN 
			--Insert Values to exsisting table
				IF (SELECT StationId FROM StationsId WHERE StationName = @StationName) IS NULL
					BEGIN 
						INSERT INTO StationsId (StationName, StationId) VALUES (@StationName, @StationID) 
					END
			END
	END
END