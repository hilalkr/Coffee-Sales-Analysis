import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

def categorize_coffee(coffee):
    if coffee in ['Latte', 'Cappuccino', 'Americano with Milk']:
        return 'Milk Based'
    elif coffee in ['Americano', 'Espresso', 'Cortado']:
        return 'Black Coffee'
    elif coffee in ['Hot Chocolate', 'Cocoa']:
        return 'Specialty'
    else:
        return 'Other'



def coffee_monthly_sales():
    df= pd.read_csv("coffee_sales.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df.fillna({'card':'Unknown'}, inplace=True)
    
    grouped = df.groupby(pd.PeriodIndex(df['date'],freq='M'))['money'].sum()


    grouped.plot(color='blue', marker='o',ylabel='Money', xlabel='Month', title='Coffee Monthly Sales Data')    
    plt.show()

        

#Time Based Analyses

def time_of_day(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'
      
def coffee_time_based_category():
    df= pd.read_csv("coffee_sales.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['time_of_day'] = df['hour'].apply(time_of_day)
    df.fillna({'card':'Unknown'}, inplace=True)
    

    grouped = df.groupby(['coffee_name', 'time_of_day']).size().reset_index(name='count')
    # result = grouped.loc[grouped.groupby('coffee_name')['count'].idxmax()] for max coffee count value
    # print(result)
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x='coffee_name', y='count', hue='time_of_day', data=grouped, palette='viridis')
    plt.xlabel('Coffee Name', fontsize=14)
    plt.ylabel('Count of Sales Coffee', fontsize=14)
    plt.title('Most Popular Hour for Each Coffee')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def coffee_name_category():
    df= pd.read_csv("coffee_sales.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    # Fill missing card data with 'Unknown' for consistent analysis
    df.fillna({'card': 'Unknown'}, inplace=True)
    df['coffee_category'] = df['coffee_name'].apply(categorize_coffee)
    
    # Group and analyze
    grouped = df.groupby(['coffee_category', 'hour']).size().reset_index(name='count')
    result = grouped.loc[grouped.groupby('coffee_category')['count'].idxmax()]
    

    #Pie Chart: To show the percentage distribution of orders by hour
    plt.pie(result['count'], labels = result['coffee_category'])
    plt.title('Coffee Data')
    plt.show()

#Sales Distribution by Payment Methods
def average_expenditure_by_payment():
    df = pd.read_csv("coffee_sales.csv")
    df.fillna({'cash_type': 'Unknown'}, inplace=True)
    df.fillna({'money': '0'}, inplace=True)
    df['cash_type']= df['cash_type'].apply(lambda x: 'Other' if x == 'Unknown' else x)
    
    avg_expenditure= df.groupby('cash_type')['money'].mean()
    
    plt.figure(figsize=(10,6))
    avg_expenditure.plot(kind='bar', color = 'skyblue', edgecolor = 'black')
    
    #customization chart
    plt.title('Average Expenditure by Payment Method')
    plt.xlabel('Payment Method')
    plt.ylabel('Average Expenditure')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for index,value in enumerate(avg_expenditure):
        plt.text(index, value + 0.5, f'{value:.2f}', ha='center', fontsize= 10)
    
    plt.tight_layout()
    plt.show()
    
#Average Expenditure Breakdown
def average_expenditure_by_client():
    df = pd.read_csv("coffee_sales.csv")
    customer_summary = df.groupby('card').agg({'money': ['sum', 'count']})
    customer_summary.columns = ['Total Spent', 'Purchase Count']
    
#Customers have been divided into 3 different groups using the KMeans Algorithm, ranging from Low (0) to High (2).
    kmeans = KMeans(n_clusters=3, random_state = 0)
    customer_summary['Cluster'] = kmeans.fit_predict(customer_summary)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Purchase Count', y='Total Spent', hue='Cluster', data=customer_summary, palette='viridis')
    plt.title('Customer Segmentation Based on Spending and Purchase Frequency')
    plt.xlabel('Number of Purchases')
    plt.ylabel('Total Spending')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    average_expenditure_by_client()
    
    



