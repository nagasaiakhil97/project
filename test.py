import pandas as pd

name="Ram"
email="ram@gmail.com"
phone=9999999999
password="user@123"


df=pd.read_csv('user.csv')
print(df)

samp=pd.DataFrame([[name,email,phone,password]],columns=['Name', 'Email', 'Phone', 'Password'])
df=df.append(samp)
print(df)
df.to_csv('user.csv')

def check(email):
	df=pd.read_csv('user.csv')
	if(df['Email']):
		print("yes")

check(email)