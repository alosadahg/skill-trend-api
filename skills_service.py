import pandas as pd
from pytrends.request import TrendReq
from scipy.stats import linregress

class Skills_Service:

    @staticmethod
    def getSkillData(keyword, startDate, endDate):
        returnMsg = {'skill': keyword, 'startDate': startDate, 'endDate': endDate}

        pytrend = TrendReq()

        pytrend.build_payload(kw_list=[keyword], timeframe=f'{startDate} {endDate}')

        df = pytrend.interest_over_time()
        df = df.reset_index()

        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year

        yearly_data = df.groupby('year')[keyword].mean().reset_index()

        yearly_table = df.groupby('year')[keyword].mean().reset_index()
        
        yearly_table = yearly_table.rename(columns={keyword: 'skillFrequency'})

        yearly_table['demandChange'] = yearly_table['skillFrequency'].pct_change() * 100
        yearly_table = yearly_table.fillna(0)  

        avg_demand_change = yearly_table['demandChange'].mean()

        yearly_data_dict = yearly_table.to_dict(orient='records')

        slope, _, _, _, _ = linregress(yearly_data['year'], yearly_data[keyword])

        trend = ''
        demand_std = yearly_table['skillFrequency'].std()
        if demand_std < 10:
            trend = 'Stable Demand'
        elif slope > 0 and demand_std > 20:
            trend = 'Emerging Skill'
        elif slope < 0:
            trend = 'Downward Trend'
        elif slope > 0:
            trend = 'Upward Trend'

        avg_demand_change = yearly_table['demandChange'].mean()

        returnMsg['prediction'] = trend
        returnMsg['avg_demand_change'] = avg_demand_change
        returnMsg['yearly_data'] = yearly_data_dict

        return returnMsg
