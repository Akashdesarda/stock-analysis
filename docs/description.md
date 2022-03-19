# Momentum Portfolio

### Many trading strategies that the traders use, one of the most popular strategies is the momentum strategy. Traders measure momentum in many different ways to identify opportunity pockets. The core idea across all these strategies remains the same i.e to identify momentum and ride the wave.

## What is Momentum

‘Momentum’ is a physics term, it refers to the quantity of motion that an object has. If you look at this definition in the context of stocks markets, then everything remains the same, except that you will have to replace ‘object’ by stocks or the index.

Simply put, momentum is the rate of change of returns of the stock or the index. If the rate of change of returns is high, then the momentum is considered high and if the rate of change of returns is low, the momentum is considered low.

This leads us to to the next obvious question i.e is what is the rate of change of returns?.

The rate of change of return, as it states the return generated  (or eroded) between two reference time period. For the sake of this discussion, let’s stick to the rate of change of return on an end of day basis. So in this context, the rate of change of returns simply means the speed at which the daily return of the stock varies.

## ** Momentum Portfolio **

Before we discuss this strategy,below few things need to be taken into consideration –

- The agenda here is to highlight how a momentum portfolio can be set up. However, this is not the only way to build a momentum portfolio
- You will need programming skills to implement this strategy or to build any other momentum strategy.

Given the above, here is a systematic guide to building a ‘Momentum Portfolio’.

### **Step 1** **– Define your stock universe**

As you may know, there are close to 4000 listed stocks on BSE and about 1800 on NSE. This includes highly valuable companies like TCS and absolute thuds such as pretty much all the Z category stocks on BSE. Companies such as these form the two extreme ends of the spectrum.  The question is, do have to track all these stocks to build a momentum portfolio?

Not really, doing so would be a waste of time.

One has to filter out the stocks and create something called as the ‘tracking universe’. The tracking universe will consist of a large basket of stocks within which we will pick stocks to constitute the momentum portfolio. This means the momentum portfolio will always be a subset of the tracking universe.

The tracking universe can be quite straightforward – it can be the Nifty 50 stocks or the BSE 500 stocks. Therefore, the momentum portfolio will always be a subset of either the Nifty 50 or BSE 500 stocks. Keeping the BSE 500 stocks as your tracking universe is a good way to start, however, if you feel a little adventurous, you can custom create your tracking universe.

Custom creation can be on any parameter – for example, out of the entire 1800 stocks on NSE, I could use a filter to weed out stocks, which has a market cap of at least 1000Crs. This filter alone will shrink the list to a much smaller, manageable set. Further, I may add other criteria such as the price of the stock should be less than 2000. So on and so forth.

I am just randomly sharing few filter ideas, but you get the point. Using the custom creation techniques helps you filter out and build a tracking universe that exactly matches your requirement.

Lastly, from my personal experience, I would suggest you have at least 150-200 stocks in your tracking universe if you wish to build a momentum portfolio of 12-15 stock.

### **Step 2** **– Set up the data**

Assuming your tracking universe is set up, you are now good to proceed to the 2nd step. In this step, you need to ensure you get the closing prices of all the stocks in your tracking universe. Ensure the data set that you have is clean and adjusted for corporate actions like the bonus issue, splits, special dividends, and other corporate actions. Clean data is the key building block to any trading strategy. There are plenty of data sources from where you can download the data free, including the NSE/BSE websites.Here we used yahoo finance API for collecting daily stock price data.

The question is – what is the look back period? How many historical data points are required? To run this strategy, you only need 1-year data point. For example, today is 2nd March 2021, then I’d need data point from 1st March 2020 to 2nd March 2021.

Please note, once you have the data points for last one-year set, you can update this on a daily basis, which means the daily closing prices are recorded.

### **Step 3** **– Calculate returns**

This is a crucial part of the strategy; in this step, we calculate the returns of all the stocks in the tracking universe. As you may have already guessed, we calculate the return to get a sense of the momentum in each of the stocks.

As we discussed earlier in this chapter, one can calculate the returns on any time frequency, be it daily/weekly/monthly or even yearly returns. We will stick to yearly returns for the sake of this discussion, however, please note; you can add your own twist to the entire strategy and calculate the returns on any time frequency you wish. Instead of yearly, you could calculate the half-yearly, monthly, or even fortnightly returns.

So, at this stage, you should have a tracking universe consisting of about 150-200 stocks. All these stocks should have historical data for at least 1 year. Further, you need to calculate the yearly return for each of these stocks in your tracking universe.

Return = \[ending value/starting value\]-1

\= \[1244.55/1435.55\]-1

\= **\-13.31%**

Quite straightforward, I guess.

### **Step 4 – Rank the returns**

Once the returns are calculated, you need to rank the returns from the highest to the lowest returns.

So what does this ranking tell us?

If you think about it, the ranking reorders our tracking universe to give us a list of stocks from the highest return stock to the lowest.

### **Step 5 – Create the portfolio**

A typical tracking universe will have about 150-200 stocks, and with the help of the previous step, we would have reordered the tracking universe. Now, with the reordered tracking universe, we are good to create a momentum portfolio.

Remember, momentum is the rate of change of return and the return itself is measured on a yearly basis.

A good momentum portfolio contains about 10-12 stocks. I’m personally comfortable with up to 15 stocks in the portfolio, not more than that. For the sake of this discussion, let us assume that we are building a 12 stocks momentum portfolio.

The momentum portfolio is now simply the top 12 stocks in the reordered tracking universe. In other words, we buy all the stocks starting from rank 1 to rank 12. In the example we were dealing with.The rest of the stocks would not constitute the portfolio but will continue to remain in the tracking universe.

What is the logic of selecting this subset of stocks within the tracking universe, you may ask?

Well, read this carefully – if the stock has done well (in terms of returns generated) for the last 12 months, then it implies that the stock has good momentum for the defined time frame. The expectation is that this momentum will continue onto the 13th month as well, and therefore the stock will continue to generate higher returns.  So if you were to buy such stocks, then you are to benefit from the expected momentum in the stock.

Clearly, this is a claim. I do not have data to back this, but I have personally used this exact technique for a couple of years with decent success. It is easy to back-test this strategy, and I encourage you to do so.

Once the momentum portfolio stocks are identified, the idea is to buy all the momentum stocks in equal proportion. So if the capital available is Rs.200,000/- and there are 12 stocks, then the idea is to buy Rs.16,666/- worth of each stock (200,000/12).

By doing so, you create an equally weighted momentum portfolio. Of course, you can tweak the weights to create a skewed portfolio, there is no problem with it, but then you need to have a solid reason for doing so.  This reason should come from backtested results.

If you like to experiment with skewed portfolios, here are few ideas –

- 50% of capital allocation across the top 5 momentum stocks (rank 1 to 5), and 50% across the remaining 7 stocks
- Top 3 stocks get 40% and the balance 60% across 9 stocks
- If you are a contrarian and expect the lower rank stocks to perform better than the higher rank stocks, then allocate more to last 5 stocks

So on and so forth. Ideally, the approach to capital allocation should come from your backtesting process, this also means you will have to backtest various capital allocation techniques to figure out which works well for you.

### **Step 6 – Rebalance the portfolio**

So far, we have created a tracking universe, calculated the 12-month returns, ranked the stocks in terms of the 12-month returns, and created a momentum portfolio by buying the top 12 stocks. The momentum portfolio was built based on the 12-month performance, with a hope that it will continue to showcase the same performance for the 13th month.

There are few assumptions here –

- The portfolio is created and bought on the 1st trading day of the month
- The above implies that all the number crunching happens on the last day of the month, post-market close
- Once the portfolio is created and bought, you hold on to the stocks till the last day of the month

Now the question is, what really happens at the end of the month?

At the end of the month, you re-run the ranking engine and figure out the top 10 or 12 stocks which have performed well over the last 12 month. Do note, at any point we consider the latest 12 months of data.

So, we now buy the stocks from rank 1 to 12, just like the way we did in the previous month. From my experience, chances are that out of the initial portfolio, only a hand full of stocks would have changed positions. So based on the list, you sell the stocks which no longer belongs in the portfolio and buy the new stocks which have featured in the latest momentum portfolio. In essence, you rebalance the portfolio and you do this at the end of every month.

So on and so forth.

## **16.4 – Momentum Portfolio variations**

The returns have been calculated on a 12-month portfolio and the stocks are held for a month. However, you don’t have to stick to this. You can try out various options, like –

- Calculate return and rank the stocks based on their monthly performance and hold the portfolio for the month
- Calculate return and rank the stocks based on fortnightly performance and hold the portfolio for 15 days
- Rank on a weekly basis and hold for a week
- Calculate on a daily basis and even do an intraday momentum portfolio

As you can see, the options are plenty and it’s only restricted by your imagination. If you think about what we have discussed so far, the momentum portfolio is price based. However, you can build a fundamental based momentum strategy as well. Here are a few ideas –

- Build a tracking universe of fundamentally good stocks
- Note the difference in quarterly sales number (% wise)
- Rank the stocks based on quarterly sales. Company with the highest jump in sales gets rank one and so on
- Buy the top 10 – 12 stocks
- Rebalance at the end of the quarter

You can do this on any fundamental parameter – EPS growth, profit margin, EBITDA margin etc. The beauty of these strategies is that the data is available, hence backtesting gets a lot easier.

## **16.5 – Word of caution**

As good as it may seem, the price based momentum strategy works well only when the market is trending up. When the markets turn choppy, the momentum strategy performs poorly, and when the markets go down, the momentum portfolio bleeds heavier than the markets itself.

Understanding the strategy’s behavior with respect to market cycle is quite crucial to the eventual success of this portfolio. I learned it the hard way. I had a great run with this strategy in 2009 and ’10 but took a bad hit in 2011. So before you execute this strategy, do your homework (backtesting) right.

Having said all of that let me reassure you – a price based momentum strategy, if implemented in the right market cycle can give you great returns, in fact, better more often than not, better than the market returns.
