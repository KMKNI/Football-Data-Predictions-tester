import numpy
import pandas as pd
from tkinter import *
import sys
import math

from pandas.core.frame import DataFrame # Only used for e^x and the factorial

class Team:   

    def __init__(self, name:str):           
        self.name = name
        # ---- [H/A]X[F/A] -----
        # H: Home, A: Away | F: For, A: Against
        # ---------------------- 
        self.HM = 0   # Matches
        self.AM = 0
        self.HP = 0
        self.AP = 0
        self.HGF = 0  # Goals
        self.HGA = 0
        self.AGF = 0
        self.AGA = 0
        self.HSF = 0  # Shots
        self.HSA = 0
        self.ASF = 0
        self.ASA = 0
        self.HSTF = 0 # Shots on Target 
        self.HSTA = 0
        self.ASTF = 0
        self.ASTA = 0
        self.HCF = 0  # Corners
        self.HCA = 0
        self.ACF = 0
        self.ACA = 0
        self.HFF = 0  # Faults
        self.HFA = 0
        self.AFF = 0
        self.AFA = 0
        self.HYF = 0  # Yellow cards
        self.HYA = 0
        self.AYF = 0
        self.AYA = 0
        self.HRF = 0  # Red cars
        self.HRA = 0
        self.ARF = 0
        self.ARA = 0
        self.elog = 1.0 
        self.LG = 0.0  
    
    # Convert to dict. 
    # Return -> {'name': self.name, 'M': self.M,...}
    def as_dict(self):
        return self.__dict__ 

    # Dynamic parameters
    def updateParameters(self):
        self.M = self.HM + self.AM
        self.Pts = self.HP + self.AP
        self.GF = self.HGF + self.AGF
        self.GA = self.HGA + self.AGA
        self.SF = self.HSF + self.ASF
        self.SA = self.HSA + self.ASA
        self.STF = self.HSTF + self.ASTF
        self.STA = self.HSTA + self.ASTA
        self.CF = self.HCF + self.ACF
        self.CA = self.HCA + self.ACA
        self.FF = self.HFF + self.AFF
        self.FA = self.HFA + self.AFA
        self.YF = self.HYF + self.AYF
        self.YA = self.HYA + self.AYA
        self.RF = self.HRF + self.ARF
        self.RA = self.HRA + self.ARA


print ("WELCOME! This is my football data analizer.")
print ("--------------------")
print ("This code has been fully developed by enriqueloz88. Despite being an open source project, its use for commercial purposes without my express authorization is not allowed.")
print ("--------------------\n")

print("First, select your league: ")
print("   1-England - Premier League")
print("   2-Spain - La Liga")
print("   3-Italy - Serie A")
print("   4-France - Ligue 1")
print("   5-Germany - Bundesliga")
print("   q-Quit the program\n")

league = input("Type an option from the ones above and hit enter: ")

if league=="1":
	league = "E0.csv"
elif league=="2":
	league = "SP1.csv"
elif league=="3":
	league = "I1.csv"
elif league=="4":
	league = "F1.csv"
elif league=="5":
	league = "D1.csv"

print("\nOkay, now you have to choose the years of the competition, in a XXYY format. For example, if you type 2021, the selected league will be the season 2020-2021, if you type 1213 will be 2012-2012 and if you type 0203 will be 2002-2003")
year = input("Type a year and hit enter: ")

while(len(year) != 4):
	print("It seems that you have not entered the year correctly, remember that this must be a 4-digit number")
	year = input("Type a year and hit enter: ")

url = 'https://www.football-data.co.uk/mmz4281/' + year + '/' + league
data = pd.read_csv(url)

'''
data = pd.read_csv('input2.csv')
data2 = pd.read_csv('db/2020/SP1.csv')
data = data.merge(data2, how='outer')
data = data.merge(data3, how='outer')
'''

# Delete non-important attributes
eliminate = [0,1,2] # Division, date and time
if 'Referee' in data.columns:
	data = data.drop(['Referee'], axis=1)
for x in range(23, len(data.columns)):
	eliminate.append(x)

#data.drop(['B365CA', 'B365CH', 'B365CD', '', '', '', ''], axis=1)
data = data.drop(data.columns[eliminate], axis=1)  # data.columns is zero-based pd.Index 

#Matches
data['P1'] = 0
data['P2'] = 0
data['HM'] = 0
data['AM'] = 0

# For acting as a local                 -> THX
# Against acting as a local             -> THXA
# In favor acting as a visitor          -> TAX
# Against acting as a visitor           -> TAXA
# Total (home + away) in favor of the team that acts in the current match at home  -> TX1
# Total (home + away) against the team that acts at home in the current match      -> TXA1
# Total (home + away) in favor of the team that acts in the current match as away  -> TX2
# Total (home + away) against the team that acts in the current match as away      -> TXA2

# New columns to add to the dataframe. Will have the total stadistics off all teams until
# the day of the match of the row. In the first match will be 0

newAtr = ['THG','THGA','TAG','TAGA','TG1','TGA1','TG2','TGA2','THS','THSA','TAS',
'TASA','TS1','TSA1','TS2','TSA2','THST','THSTA','TAST','TASTA','TST1','TSTA1','TST2',
'TSTA2','THC','THCA','TAC','TACA','TC1','TCA1','TC2','TCA2','THF','THFA','TAF','TAFA',
'TF1','TFA1','TF2','TFA2','THY','THYA','TAY','TAYA','TY1','TYA1','TY2','TYA2','THR',
'THRA','TAR','TARA','TR1','TRA1','TR2','TRA2']

for atr in newAtr:
	data[atr] = 0

#Other ratings
data['LG1'] = 0.0   #Last games results. data=data*0.5+POINTS     
data['LG2'] = 0.0   #Last games results. data=data*0.5+POINTS   

teams = pd.unique(data['HomeTeam'])
teams.sort()

teamsList = []

for team in teams:

	t = Team(team) # Create new team object
	t.updateParameters()

	for x in range(len(data.index)):
		if team==data['HomeTeam'].values[x]:
			data['P1'].values[x] = t.M
			data['HM'].values[x] = t.HM
			
			data['THG'].values[x] =  t.HGF
			data['THGA'].values[x] = t.HGA
			data['TG1'].values[x] =  t.GF
			data['TGA1'].values[x] = t.GA

			data['THS'].values[x] =  t.HSF
			data['THSA'].values[x] = t.HSA
			data['TS1'].values[x] =  t.SF
			data['TSA1'].values[x] = t.SA

			data['THST'].values[x] = t.HSTF
			data['THSTA'].values[x] =t.HSTA
			data['TST1'].values[x] = t.STF
			data['TSTA1'].values[x] =t.STA

			data['THC'].values[x] =  t.HCF
			data['THCA'].values[x] = t.HCA
			data['TC1'].values[x] =  t.CF
			data['TCA1'].values[x] = t.CA

			data['THF'].values[x] =  t.HFF
			data['THFA'].values[x] = t.HFA
			data['TF1'].values[x] =  t.FF
			data['TFA1'].values[x] = t.FA

			data['THY'].values[x] =  t.HYF
			data['THYA'].values[x] = t.HYA
			data['TY1'].values[x] =  t.YF
			data['TYA1'].values[x] = t.YA

			data['THR'].values[x] =  t.HRF
			data['THRA'].values[x] = t.HRA
			data['TR1'].values[x] =  t.RF
			data['TRA1'].values[x] = t.RA

			data['LG1'].values[x] =  t.LG

			t.HM = t.HM + 1
			t.HGF = t.HGF + data['FTHG'].values[x]
			t.HGA = t.HGA + data['FTAG'].values[x]
			t.HSF = t.HSF + data['HS'].values[x]
			t.HSA = t.HSA + data['AS'].values[x]         
			t.HSTF = t.HSTF + data['HST'].values[x]
			t.HSTA = t.HSTA + data['AST'].values[x]             
			t.HCF = t.HCF + data['HC'].values[x]
			t.HCA = t.HCA + data['AC'].values[x]              
			t.HFF = t.HFF + data['HF'].values[x]
			t.HFA = t.HFA + data['AF'].values[x]              
			t.HYF = t.HYF + data['HY'].values[x]
			t.HYA = t.HYA + data['AY'].values[x]              
			t.HRF = t.HRF + data['HR'].values[x]
			t.HRA = t.HRA + data['AR'].values[x]

			p = -3
			if data['FTR'].values[x] == 'H':
				t.HP = t.HP + 3
				p = 3
			elif data['FTR'].values[x] == 'D':
				t.HP = t.HP + 1
				p = 1
			t.LG = t.LG*0.8 + p

			t.updateParameters()

		if team==data['AwayTeam'].values[x]:
			data['P2'].values[x] = t.M
			data['AM'].values[x] = t.AM			
			
			data['TAG'].values[x] = t.AGF
			data['TAGA'].values[x] =t.AGA
			data['TG2'].values[x] = t.GF
			data['TGA2'].values[x] =t.GA

			data['TAS'].values[x] = t.ASF
			data['TASA'].values[x] =t.ASA
			data['TS2'].values[x] = t.SF
			data['TSA2'].values[x] =t.SA

			data['TAST'].values[x] =t.ASTF
			data['TASTA'].values[x]=t.ASTA
			data['TST2'].values[x] =t.STF
			data['TSTA2'].values[x]=t.STA

			data['TAC'].values[x] = t.ACF
			data['TACA'].values[x] =t.ACA
			data['TC2'].values[x] = t.CF
			data['TCA2'].values[x] =t.CA

			data['TAF'].values[x] = t.AFF
			data['TAFA'].values[x] =t.AFA
			data['TF2'].values[x] = t.FF
			data['TFA2'].values[x] =t.FA

			data['TAY'].values[x] = t.AYF
			data['TAYA'].values[x] =t.AYA
			data['TY2'].values[x] = t.YF
			data['TYA2'].values[x] =t.YA

			data['TAR'].values[x] = t.ARF
			data['TARA'].values[x] =t.ARA
			data['TR2'].values[x] = t.RF
			data['TRA2'].values[x] =t.RA

			data['LG2'].values[x] =  t.LG
			
			t.AM = t.AM + 1
			t.AGF = t.AGF + data['FTAG'].values[x]
			t.AGA = t.AGA + data['FTHG'].values[x]
			t.ASF = t.ASF + data['AS'].values[x]
			t.ASA = t.ASA + data['HS'].values[x]
			t.ASTF = t.ASTF + data['AST'].values[x]
			t.ASTA = t.ASTA + data['HST'].values[x]
			t.ACF = t.ACF + data['AC'].values[x]
			t.ACA = t.ACA + data['HC'].values[x]
			t.AFF = t.AFF + data['AF'].values[x]
			t.AFA = t.AFA + data['HF'].values[x]
			t.AYF = t.AYF + data['AY'].values[x]
			t.AYA = t.AYA + data['HY'].values[x]
			t.ARF = t.ARF + data['AR'].values[x]
			t.ARA = t.ARA + data['HR'].values[x]

			p = -3
			if data['FTR'].values[x] == 'A':
				t.AP = t.AP + 3
				p = 3
			elif data['FTR'].values[x] == 'D':
				t.AP = t.AP + 1
				p = 1
			t.LG = t.LG*0.8 + p
			
			t.updateParameters()  
	
	teamsList.append(t)

''' #TeamList to df
df = pd.DataFrame([x.as_dict() for x in teamsList])
print(df)
'''

'''
print ("\n---------------------------------------------------------")
print ("Team")
print ("Goles anotados en casa:" + str(data['THG'].values[len(data)-1]))
'''

writer = pd.ExcelWriter("trainingData/output.xlsx", engine='xlsxwriter')
data.to_excel(writer, index = False, header=True, sheet_name='Sheet1')  
data.to_csv("trainingData/output.csv", index = False, header=True)  

workbook  = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_column(2, 80, 5)
worksheet.set_column(0, 1, 12)
writer.close()

#Get the means
for atr in newAtr:
	if atr[0]=='T' and atr[1]=='H':
		data[atr] = data[atr]/data['HM']
	if atr[0]=='T' and atr[1]=='A':
		data[atr] = data[atr]/data['AM']
	if atr[-1]=='1':
		data[atr] = data[atr]/data['P1']
	if atr[-1]=='2':
		data[atr] = data[atr]/data['P2']

data = data.fillna(0) # Fill NaN with zeros. Case of divide a number by zero

original_data = data

writer = pd.ExcelWriter("trainingData/outputMeans.xlsx", engine='xlsxwriter')
data.to_excel(writer, index = False, header=True, sheet_name='Sheet1')  

workbook  = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_column(2, 80, 5)
worksheet.set_column(0, 1, 12)
writer.close()

'''---------------------------------------------
---------PRINT DIFFERENT STADISTICS-------------
------------------------------------------------'''

def printTable(data, teamsList):
	teamsList.sort(key=lambda x: x.Pts, reverse=True)
	print("{0:3} | {1:18}|{2:4} | {3:2} {4:3} {5:3} {6:3} {7:3} {8:3} {9:3} {10:3} {11:3}".format("Pos","Name"," Pts", " M", " GF", " GA", " SF", " SA", " CF", " CA", " FF", " FA"))
	print("---------------------------------------------------------------------------------")
	for index,team in enumerate(teamsList, start=1):
		print("{0:3} | {1:18}|{2:4} | {3:2} {4:3} {5:3} {6:3} {7:3} {8:3} {9:3} {10:3} {11:3}".format(index,team.name,team.Pts,team.M,team.GF,team.GA,team.SF,team.SA,team.CF,team.CA,team.FF,team.FA))

	print("")

def printHomeTable(data, teamList):
	teamsList.sort(key=lambda x: x.HP, reverse=True)
	print("{0:3} | {1:18}|{2:4} | {3:2} {4:3} {5:3} {6:3} {7:3} {8:3} {9:3} {10:3} {11:3}".format("Pos","Name"," Pts", " M", " GF", " GA", " SF", " SA", " CF", " CA", " FF", " FA"))
	print("---------------------------------------------------------------------------------")
	for index,team in enumerate(teamsList, start=1):
		print("{0:3} | {1:18}|{2:4} | {3:2} {4:3} {5:3} {6:3} {7:3} {8:3} {9:3} {10:3} {11:3}".format(index,team.name,team.HP,team.HM,team.HGF,team.HGA,team.HSF,team.HSA,team.HCF,team.HCA,team.HFF,team.HFA))

	print("")

def printAwayTable(data, teamList):
	teamsList.sort(key=lambda x: x.AP, reverse=True)
	print("{0:3} | {1:18}|{2:4} | {3:2} {4:3} {5:3} {6:3} {7:3} {8:3} {9:3} {10:3} {11:3}".format("Pos","Name"," Pts", " M", " GF", " GA", " SF", " SA", " CF", " CA", " FF", " FA"))
	print("---------------------------------------------------------------------------------")
	for index,team in enumerate(teamsList, start=1):
		print("{0:3} | {1:18}|{2:4} | {3:2} {4:3} {5:3} {6:3} {7:3} {8:3} {9:3} {10:3} {11:3}".format(index,team.name,team.AP,team.AM,team.AGF,team.AGA,team.ASF,team.ASA,team.ACF,team.ACA,team.AFF,team.AFA))

	print("")

def printAllTables(data, teamList):
	print("HOME TABLE:\n")
	printHomeTable(data, teamsList)
	print("AWAY TABLE:\n")
	printAwayTable(data, teamsList)
	print("TOTAL TABLE:\n")
	printTable(data, teamsList)

'''---------------------------------------------
---------MAKING THE DIFFERENT MODELS------------
------------------------------------------------'''

noReprGames = 91 # Number of no-representative games. First N games will be deleted#kkkkkkkkkkkkkkkkk
test_size = 0.06 # % of matches used to size the accuracy of the model

# Function to delete the first games of the training files as they are not very representative
def deleteHeadToTrain(data:DataFrame, rows:int):
	#rows_to_drop = min(rows, len(data))#kkkkkkkkkkkkkkkkkkkk
	print("Number of rows to drop:", rows)#kkkkkkkkkkkkkkkkkk
	print("Total rows in DataFrame:", len(data))#kkkkkkkkkkkkkkkk
	data = data.drop(range(0,rows), axis=0) #kkkkkkkkkkkkkkkkk
	for x in range(len(data.index)):
		if x < len(data['HM'].values) and (data['HM'].values[x]<3 or data['P1'].values[x]<4 or data['AM'].values[x]<3 or data['P2'].values[x]<4):
			if x in data.index:
				data.drop(x, axis=0, inplace=True)

	return data

# Function to generate a new row (a new match) at the end of the test file, to predict the user desire.
# Return a new df with only one row, that will be concatenated with the test df
def newRowToTest(homeTeam:Team, awayTeam:Team):
	newDf = pd.DataFrame(
		{
			'THG': [homeTeam.HGF/homeTeam.HM],
			'THGA': [homeTeam.HGA/homeTeam.HM],
			'TG1': [homeTeam.GF/homeTeam.M],
			'TGA1': [homeTeam.GA/homeTeam.M],
			'TAG': [awayTeam.AGF/awayTeam.AM],
			'TAGA': [awayTeam.AGA/awayTeam.AM],
			'TG2': [awayTeam.GF/awayTeam.M],
			'TGA2': [awayTeam.GA/awayTeam.M],

			'THS': [homeTeam.HSF/homeTeam.HM],
			'THSA': [homeTeam.HSA/homeTeam.HM],
			'TS1': [homeTeam.SF/homeTeam.M],
			'TSA1': [homeTeam.SA/homeTeam.M],
			'TAS': [awayTeam.ASF/awayTeam.AM],
			'TASA': [awayTeam.ASA/awayTeam.AM],
			'TS2': [awayTeam.SF/awayTeam.M],
			'TSA2': [awayTeam.SA/awayTeam.M],

			'THST': [homeTeam.HSTF/homeTeam.HM],
			'THSTA': [homeTeam.HSTA/homeTeam.HM],
			'TST1': [homeTeam.STF/homeTeam.M],
			'TSTA1': [homeTeam.STA/homeTeam.M],
			'TAST': [awayTeam.ASTF/awayTeam.AM],
			'TASTA': [awayTeam.ASTA/awayTeam.AM],
			'TST2': [awayTeam.STF/awayTeam.M],
			'TSTA2': [awayTeam.STA/awayTeam.M],

			'THC': [homeTeam.HCF/homeTeam.HM],
			'THCA': [homeTeam.HCA/homeTeam.HM],
			'TC1': [homeTeam.CF/homeTeam.M],
			'TCA1': [homeTeam.CA/homeTeam.M],
			'TAC': [awayTeam.ACF/awayTeam.AM],
			'TACA': [awayTeam.ACA/awayTeam.AM],
			'TC2': [awayTeam.CF/awayTeam.M],
			'TCA2': [awayTeam.CA/awayTeam.M],

			'THF': [homeTeam.HFF/homeTeam.HM],
			'THFA': [homeTeam.HFA/homeTeam.HM],
			'TF1': [homeTeam.FF/homeTeam.M],
			'TFA1': [homeTeam.FA/homeTeam.M],
			'TAF': [awayTeam.AFF/awayTeam.AM],
			'TAFA': [awayTeam.AFA/awayTeam.AM],
			'TF2': [awayTeam.FF/awayTeam.M],
			'TFA2': [awayTeam.FA/awayTeam.M],

			'THY': [homeTeam.HYF/homeTeam.HM],
			'THYA': [homeTeam.HYA/homeTeam.HM],
			'TY1': [homeTeam.YF/homeTeam.M],
			'TYA1': [homeTeam.YA/homeTeam.M],
			'TAY': [awayTeam.AYF/awayTeam.AM],
			'TAYA': [awayTeam.AYA/awayTeam.AM],
			'TY2': [awayTeam.YF/awayTeam.M],
			'TYA2': [awayTeam.YA/awayTeam.M],

			'THR': [homeTeam.HRF/homeTeam.HM],
			'THRA': [homeTeam.HRA/homeTeam.HM],
			'TR1': [homeTeam.RF/homeTeam.M],
			'TRA1': [homeTeam.RA/homeTeam.M],
			'TAR': [awayTeam.ARF/awayTeam.AM],
			'TARA': [awayTeam.ARA/awayTeam.AM],
			'TR2': [awayTeam.RF/awayTeam.M],
			'TRA2': [awayTeam.RA/awayTeam.M],

			'LG1': [homeTeam.LG],
			'LG2': [awayTeam.LG]
		},
		index=[9999],
	)
	newDf = newDf.fillna(0) # Fill NaN with zeros. Case of divide a number by zero
	return newDf

def printTestPredictions(X_test, prediction_test, prediction_test2, Y_test, Y2_test):
	#Creating new dataframe to print the predictions
	matches_prediction = []
	i=0
	for row in X_test.index:
		if row != 9999:
			match_data = []
			match_data.append(original_data['HomeTeam'].values[row])
			match_data.append(original_data['AwayTeam'].values[row])
			match_data.append(prediction_test[i])
			match_data.append(prediction_test2[i])
			match_data.append(Y_test[i])
			match_data.append(Y2_test[i])
			match_data = tuple(match_data)
			matches_prediction.append(match_data)
			i=i+1

	print("\nPredictions done to test the model: ")
	df_prediction = pd.DataFrame(matches_prediction, columns=['HomeTeam', 'AwayTeam', 'PHG', 'PAG','RHG', 'RAG'])
	print (df_prediction)
	print("\nHere are the matches used to measure the performance of the model. This is the test file, used in most ML models")

def printBestAttr(X, model):
	print("\nBest Attributes:")
	feature_list = list(X.columns)
	features_imp = pd.Series(model.feature_importances_, index=feature_list).sort_values(ascending=False)
	print(features_imp.head())
	print("\nWorst Attributes:")
	print(features_imp.tail())

# Function that determinate the varibles to predict
# Return list with [Y,Y2,X]. Y and Y2 will be the two variable to predict, dependent on X
def preModel():
	data = deleteHeadToTrain(original_data, noReprGames)

	#Variables to predict. Dependent variables
	Y = data['FTHG'].values
	Y = Y.astype('int')
	Y2 = data['FTAG'].values
	Y2 = Y2.astype('int')

	#Indepiendent variables. Can not have data of the actual match
	X = data[['THG','TAG','THGA','TAGA','TG1','TG2','TGA1','TGA2','THS','TAS','THSA','TASA','TS1','TS2','TSA1','TSA2',
	'THST','TAST','THSTA','TASTA','TST1','TST2','TSTA1','TSTA2','THC','TAC','THCA','TACA','TC1','TC2','TCA1','TCA2',
	'THF','TAF','THFA','TAFA','TF1','TF2','TFA1','TFA2','THY','TAY','THYA','TAYA','TY1','TY2','TYA1','TYA2',
	'THR','TAR','THRA','TARA','TR1','TR2','TRA1','TRA2','LG1','LG2']]
	#X = data[['THG','TAG','THGA','TAGA','TG1','TG2','TGA1','TGA2','ELOG1', 'ELOG2','LG1','LG2']]
	
	return [Y,Y2,X]

# Return the probability of X according to the Poisson Distribution
def poissonDistr(mean:float, X:int):
	result = math.exp((-1)*mean) * (mean**X)
	result = result / math.factorial(X)
	return result

#This is not AI. Thanks to https://www.sbo.net/strategy/football-prediction-model-poisson-distribution/
def teamStrenghtsModel():
	total_matches = 0
	total_home = 0
	total_away = 0
	#Select the teams to predict and get the means
	for index,team in enumerate(teamsList, start=1):
		print(index, team.name)
		total_matches = total_matches + team.M
		total_home = total_home + team.HGF
		total_away = total_away + team.AGF
	mean_home = total_home/total_matches
	mean_away = total_away/total_matches
	homeTeamToPredict = int(input("Select the home team number: "))
	awayTeamToPredict = int(input("Select the away team number: "))
	homeTeam = teamsList[homeTeamToPredict-1]
	awayTeam = teamsList[awayTeamToPredict-1]

	#Get the strenghts
	homeTeamAtt = (homeTeam.HGF/team.HM) / mean_home
	homeTeamDef = (homeTeam.HGA/team.HM) / mean_away
	awayTeamAtt = (awayTeam.AGF/team.AM) / mean_away
	awayTeamDef = (awayTeam.AGA/team.AM) / mean_home

	#Predictions
	homePredict = homeTeamAtt*awayTeamDef*mean_home
	awayPredict = awayTeamAtt*homeTeamDef*mean_away
	print("\nPrediction for","{0:15}".format(str(teamsList[homeTeamToPredict-1].name) + ": "), '{:.2f}'.format(homePredict))
	print("Prediction for", "{0:15}".format(str(teamsList[awayTeamToPredict-1].name) + ": "), '{:.2f}'.format(awayPredict))


def randomForest():
	variables = preModel()
	Y = variables[0]
	Y2 = variables[1]
	X = variables[2]
	X2 = variables[2]

	print("\n ---------------------------------")
	print("Making random forest.............\n")

	#Split data into train and test datasets
	from sklearn.model_selection import train_test_split
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=20)
	X2_train, X2_test, Y2_train, Y2_test = train_test_split(X2, Y2, test_size=test_size, random_state=20)

	#Add match to predict
	for index,team in enumerate(teamsList, start=1):
		print(index, team.name)
	homeTeamToPredict = int(input("Select the home team number: "))
	awayTeamToPredict = int(input("Select the away team number: "))
	newDf = newRowToTest(teamsList[homeTeamToPredict-1], teamsList[awayTeamToPredict-1])
	X_test = pd.concat([X_test, newDf])
	X2_test = pd.concat([X2_test, newDf])

	#Get the model
	from sklearn.ensemble import RandomForestRegressor
	model = RandomForestRegressor(n_estimators=180, min_samples_leaf=2, min_samples_split=3, random_state=20)

	model.fit(X_train, Y_train)
	prediction_test = model.predict(X_test) #Results of the predictions in a list[]

	model.fit(X2_train, Y2_train)
	prediction_test2 = model.predict(X2_test)
	
	from sklearn import metrics
	# We have to do [:-1] to delete the last row that we introduced manually.
	print ("\nMean sq. error for the home team->", '{:.2f}'.format(100*round(metrics.mean_squared_error(Y_test, prediction_test[:-1]),2)), "%")
	#print ("Mean abs. error for the home team->", '{:.2f}'.format(100*round(metrics.mean_absolute_error(Y_test, prediction_test),2)), "%")
	print ("Mean sq. error for the away team->", '{:.2f}'.format(100*round(metrics.mean_squared_error(Y2_test, prediction_test2[:-1]),2)), "%")
	#print ("Mean abs. error for the away team->", '{:.2f}'.format(100*round(metrics.mean_absolute_error(Y2_test, prediction_test2),2)), "%")
	
	print("\nPrediction for","{0:15}".format(str(teamsList[homeTeamToPredict-1].name) + ": "), '{:.2f}'.format(prediction_test[-1]))
	print("Prediction for", "{0:15}".format(str(teamsList[awayTeamToPredict-1].name) + ": "), '{:.2f}'.format(prediction_test2[-1]))
	
	sel = '0'
	while sel != 'n':
		print("\nDo you want to have more data of this model?")
		print("   1-Yes, show me the predictions of the test file")
		print("   2-Yes, show me the more relevant attributes of the tree")
		print("   3-Yes, show me the generated trees")
		print("   n-No, quit\n")
		sel = input("Type an option from the ones above and hit enter: ")
		
		if sel=='n':
			return
		sel = int(sel)
		if sel==1:
			printTestPredictions(X_test, prediction_test, prediction_test2, Y_test, Y2_test)
		if sel==2:
			printBestAttr(X, model)		
		if sel==3:
			print_decision_rules(model)

# Function to print the trees generates in randomForest
def print_decision_rules(rf):

    for tree_idx, est in enumerate(rf.estimators_):
        tree = est.tree_
        assert tree.value.shape[1] == 1 # no support for multi-output

        print('TREE: {}'.format(tree_idx))

        iterator = enumerate(zip(tree.children_left, tree.children_right, tree.feature, tree.threshold, tree.value))
        for node_idx, data in iterator:
            left, right, feature, th, value = data

            # left: index of left child (if any)
            # right: index of right child (if any)
            # feature: index of the feature to check
            # th: the threshold to compare against
            # value: values associated with classes            

            # for classifier, value is 0 except the index of the class to return
            class_idx = numpy.argmax(value[0])

            if left == -1 and right == -1:
                print('{} LEAF: return class={}'.format(node_idx, class_idx))
            else:
                print('{} NODE: if feature[{}] < {} then next={} else next={}'.format(node_idx, feature, th, left, right))    

def multilayerPerceptron():
	variables = preModel()
	Y = variables[0]
	Y2 = variables[1]
	X = variables[2]
	X2 = variables[2]

	print("\n ---------------------------------")
	print("Making multilayer perceptron.............\n")

	#Split data into train and test datasets
	from sklearn.model_selection import train_test_split
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=20)
	X2_train, X2_test, Y2_train, Y2_test = train_test_split(X2, Y2, test_size=test_size, random_state=20)

	#Add match to predict
	for index,team in enumerate(teamsList, start=1):
		print(index, team.name)
	homeTeamToPredict = int(input("Select the home team number: "))
	awayTeamToPredict = int(input("Select the away team number: "))
	newDf = newRowToTest(teamsList[homeTeamToPredict-1], teamsList[awayTeamToPredict-1])
	X_test = pd.concat([X_test, newDf])
	X2_test = pd.concat([X2_test, newDf])

	#Get the model
	from sklearn.neural_network import MLPRegressor
	model = MLPRegressor(random_state=20, max_iter=5000, hidden_layer_sizes=100, activation='tanh')

	model.fit(X_train, Y_train)
	prediction_test = model.predict(X_test) #Results of the predictions in a list[]

	model.fit(X2_train, Y2_train)
	prediction_test2 = model.predict(X2_test)
	
	from sklearn import metrics
	# We have to do [:-1] to delete the last row that we introduced manually.
	print ("\nMean sq. error for the home team->", '{:.2f}'.format(100*round(metrics.mean_squared_error(Y_test, prediction_test[:-1]),2)), "%")
	#print ("Mean abs. error for the home team->", '{:.2f}'.format(100*round(metrics.mean_absolute_error(Y_test, prediction_test),2)), "%")
	print ("Mean sq. error for the away team->", '{:.2f}'.format(100*round(metrics.mean_squared_error(Y2_test, prediction_test2[:-1]),2)), "%")
	#print ("Mean abs. error for the away team->", '{:.2f}'.format(100*round(metrics.mean_absolute_error(Y2_test, prediction_test2),2)), "%")
	
	print("\nPrediction for","{0:15}".format(str(teamsList[homeTeamToPredict-1].name) + ": "), '{:.2f}'.format(prediction_test[-1]))
	print("Prediction for", "{0:15}".format(str(teamsList[awayTeamToPredict-1].name) + ": "), '{:.2f}'.format(prediction_test2[-1]))

	sel = '0'
	while sel != 'n':
		print("\nDo you want to have more data of this model?")
		print("   1-Yes, show me the predictions of the test file")
		print("   n-No, quit\n")
		sel = input("Type an option from the ones above and hit enter: ")
		
		if sel=='n':
			return
		sel = int(sel)
		if sel==1:
			printTestPredictions(X_test, prediction_test, prediction_test2, Y_test, Y2_test)
		if sel==2:
			pass

print("Let's start! What do you want to do?")
selContinue = 'y'
while selContinue != 'n':
	print("   1-Print league standings and statistics")
	print("   2-Get some predictions with AI")
	print("   q-Quit the program\n")
	sel = input("Type an option from the ones above and hit enter: ")

	if sel=='q':
		sys.exit()

	sel = int(sel)
	if sel==1:
		print("What do you want me to show you?")
		print("   1-Print league clasification")
		print("   2-Print league clasification (Only home matches)")
		print("   3-Print league clasification (Only away matches)")
		print("   123-Print the 3 clasifications of above")
		print("   q-Return/Quit\n")
		sel2 = input("Type an option from the ones above and hit enter: ")
		if sel2 != 'q':
			sel2 = int(sel2)
			if sel2 == 1:
				printTable(original_data, teamsList)
			elif sel2 == 2:
				printHomeTable(original_data, teamsList)
			elif sel2 == 3:
				printAwayTable(original_data,teamsList)
			elif sel2 == 123:
				printAllTables(original_data, teamsList)
	elif sel==2:
		print("What model do you want to use?")
		print("   1-Random Forest")
		print("   2-Multilayer Perceptron")
		print("   3-Team Strenghts Model")
		print("   q-Return/Quit\n")
		sel2 = input("Type an option from the ones above and hit enter: ")
		if sel2 != 'q':
			sel2 = int(sel2)
			if sel2 == 1:
				randomForest()
			elif sel2 == 2:
				multilayerPerceptron()
			elif sel2 == 3:
				teamStrenghtsModel()

	selContinue = input("Done! Any other operation (y/n): ")
	if selContinue=='n':
		print("\nAllright, been a pleasure!\n")
		sys.exit()