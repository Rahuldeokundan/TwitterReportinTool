from django.shortcuts import render
from django.http import HttpResponse
from twitter_ads.client import Client
from twitter_ads.enum import ENTITY, GRANULARITY, METRIC_GROUP, PLACEMENT
from twitter_ads.http import Request
from twitter_ads.error import Error
from datetime import date, timedelta
from datetime import datetime
from .models import DataSet

# Create your views here.


def home(request):
    Accounts=['18ce559z5re','18ce559wc04','18ce557t3m2','18ce552xv0y']
    for AccountID in Accounts:
        CONSUMER_KEY = 'HDoSqCGCB3myJNoMP5RziL97w'
        CONSUMER_SECRET = '1WUOTQZsbNxIyVFpjCfSK4NslZqGUsvroYF4UdPFhGIVA4QPsh'
        ACCESS_TOKEN = '786549565717491713-3Qd2klEkIroIHYZ7f78ACd36qutNVHx'
        ACCESS_TOKEN_SECRET = '0aFaWFTpgXnrnhUCB2yZyGbcs8LF48Q1LQJiUt1VSvadn'
        ACCOUNT_ID = AccountID

        # initialize the client
        client = Client(
            CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                options={
                            'handle_rate_limit': True,
                            'retry_max': 3,
                            'retry_delay': 10,
                            'retry_on_status': [404, 500, 503]
                        })

        # load the advertiser account instance
        account = client.accounts(ACCOUNT_ID)
        # print(account.name) 


        yesterday = ("2020-03-05") + ("T00:00:00+08:00")
        today = ("2020-03-07") + ("T00:00:00+08:00")

        SpendList=[]
        DateList=[]
        # iterate through campaigns
        for camp in account.campaigns():

            if camp.id:

                resource = f"/8/stats/accounts/"+AccountID+"/" #Enter Account Id Here
                params = {
                    "entity": ENTITY.CAMPAIGN,
                    "entity_ids": camp.id,
                    "start_time": yesterday,
                    "end_time": today,
                    "granularity": GRANULARITY.TOTAL,
                    "metric_groups": METRIC_GROUP.BILLING,
                    "placement": PLACEMENT.ALL_ON_TWITTER
                    }

                req = Request(client=client, method="GET", resource=resource, params=params)

                response = req.perform()
                spend_in_micros_value = response.body["data"][0]["id_data"][0]["metrics"]["billed_charge_local_micro"]


                if spend_in_micros_value != None:
                    spendAll= response.body["data"][0]["id_data"][0]["metrics"]["billed_charge_local_micro"][0]

                    spend = round((spendAll / 1000000),2)
                    SpendList.append(spend)
                else:
                    spend=0
                    SpendList.append(spend)

                StartTime = response.body["request"]["params"]["start_time"]
    #           Subtraction one Day
                x = slice(10)
                startTime=(StartTime[x])
                start = datetime.strptime(startTime, "%Y-%m-%d")
                Start = start + timedelta(days = 1) 
                
                EndTime = response.body["request"]["params"]["end_time"]

    #           Subtraction one Day
                x = slice(10)
                endTime=(EndTime[x])
                end = datetime.strptime(endTime, "%Y-%m-%d")
                End = end - timedelta(days = 0) 
                
                DateList.append(Start)
                DateList.append(End)

                
            else:
                print("No Camp")

        total = 0
        for OneMonth in range(0,len(SpendList)):
            total = total + SpendList[OneMonth]
        account=(account.name)    
        print("Total Spend= ", total)
        StartDate= (DateList[0])
        EndDate= (DateList[1])
        
        currentDate = datetime.today()
        print("Current Date= ", currentDate)

        DataFrame=DataSet(currentDate=currentDate,account=account, spend=total,StartDate= StartDate, EndDate= EndDate)
        DataFrame.save()    
    return render( request, "index.html")


def dbtest(request):
    account="Rahul"
    DateFrame=DataSet(account=account)
    DateFrame.save()

    return render(request, 'test.html')