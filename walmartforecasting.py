import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import SimpleExpSmoothing, seasonal_decompose 

FILE_NAME = r'C:\Users\Zain Farooqi\Desktop\DAtasks\TASK7\Walmart_with_Region.csv'
print(f"Loading data from {FILE_NAME}...")

try:
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()
except FileNotFoundError:
    print(f"Error: {FILE_NAME} not found. Please ensure the file is in the same directory.")
    exit()

monthly_sales = df['Weekly_Sales'].resample('M').sum()
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales, label='Monthly Sales', color='C0')
ma_window = 3
ma_3 = monthly_sales.rolling(window=ma_window).mean()
plt.plot(ma_3, label=f'{ma_window}-Month Moving Average', color='red', linestyle='--')

plt.title('Walmart Total Monthly Sales Trend and 3-Month Moving Average')
plt.xlabel('Date')
plt.ylabel('Total Sales ($)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('total_sales_trend_ma.png')
plt.show() 
plt.close()
print("Generated 'total_sales_trend_ma.png': Monthly Sales Trend and Moving Average.")


try:
    decomposition = seasonal_decompose(monthly_sales, model='additive', period=12)

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    decomposition.observed.plot(ax=axes[0]); axes[0].set_title('Observed Monthly Sales')
    decomposition.trend.plot(ax=axes[1]); axes[1].set_title('Trend Component')
    decomposition.seasonal.plot(ax=axes[2]); axes[2].set_title('Seasonal Component (Yearly)')
    decomposition.resid.plot(ax=axes[3]); axes[3].set_title('Residuals'); axes[3].set_xlabel('Date')

    plt.tight_layout()
    plt.savefig('seasonal_decomposition.png')
    plt.show() 
    plt.close()
    print("Generated 'seasonal_decomposition.png': Seasonal Decomposition.")

except ValueError as e:
    print(f"Could not perform seasonal decomposition: {e}")


FORECAST_PERIODS = 6 

fit_ses = SimpleExpSmoothing(monthly_sales, initialization_method="estimated").fit(
    optimized=True,
    remove_bias=False
)

fitted_values = fit_ses.fittedvalues.rename("Fitted SES")
forecast = fit_ses.forecast(FORECAST_PERIODS).rename(f"SES Forecast ({FORECAST_PERIODS} Months)")


plt.figure(figsize=(12, 6))
monthly_sales.plot(label='Historical Monthly Sales', color='C0')
fitted_values.plot(label='Simple Exponential Smoothing Fit', color='orange', linestyle='--')
forecast.plot(label=forecast.name, color='green', marker='o', linestyle='-')

plt.axvspan(monthly_sales.index[-1], forecast.index[-1], color='grey', alpha=0.1, label='Forecast Horizon')

plt.title(f'Monthly Sales Forecasting using Simple Exponential Smoothing (Next {FORECAST_PERIODS} Months)')
plt.xlabel('Date')
plt.ylabel('Total Sales ($)')
plt.legend(loc='lower left')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('sales_ses_forecast.png')
plt.show() 
plt.close()

print("\n--- Forecast Summary (Next 6 Months) ---")
forecast_summary = forecast.to_frame()
forecast_summary.index = forecast_summary.index.to_period('M')
forecast_summary.columns = ['Forecasted Sales']
formatter = "{:,.0f}".format

print("Sales are displayed in US dollars, rounded to the nearest whole number.")
print(forecast_summary.to_string(formatters={'Forecasted Sales': formatter}))
print("\n--- Analysis Complete ---")