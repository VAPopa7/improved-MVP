# Improved Mean-Variance Portfolio
The **Mean-Variance Portfolio (MVP)** maximizes $w$ in: $w’ \mu - \frac{\lambda}{2}w’ \Sigma w$ subject to $1’w=1$ and $w \ge 0$, where $\mu$ is the expected returns, $\Sigma$ is the covariance matrix, and $\lambda$ is a hyper-parameter that controls how risk averse the investor is. It serves as the foundation of modern portfolio optimization frameworks, yet it is also frequently criticized as an “error maximizer”. This project attempts to overcome its known limitations through several practices.

## Overview
The project investigates several methods that can materially improve the out-of-sample stability of Markowitz' mean-variance portfolios under realistic constraints, while addressing both the problem and suggested solution thoroughly throughout the notebook. The repository serves as an instructive foundation of the world of portfolio optimization, and will be included on my curriculum vitae. 

## Features
Subject to long-only and fully invested constraints, the following improvements are explored:
- **Diversification constraint**:  A Herfindahl-type constraint on portfolio weights, limiting concentration and discouraging extreme allocations.
- **Cross-validation of the risk aversion parameter ($\lambda$)**: $\lambda$ is selected using out-of-sample Sharpe ratio to avoid static tuning and improve robustness across market regimes.
- **Shrinkage estimation**: Shrinkage is applied to reduce estimation error and improve stability.
- **Heavy-tailed maximum likelihood estimators**: Expected returns and covariance are estimated under a multivariate Student-t distribution to better capture fat tails and outliers.

Several MVP variants are constructed using combinations of the suggestions above. These are:
- **Vanilla MVP**, the standard MVP with $\lambda = 1$
- **Vanilla MVP w/ div**, the MVP with diversification constraint $||w||^2_2 \le \frac{5}{N}$ and $\lambda = 1$
- **MVP w/ div. + cv lmd**, the MVP with cross-validation for $lambda$ and diversification constraint $||w||^2_2 \le \frac{5}{N}$.
- **Shr. MVP w/ div. + cv lmd**, the MVP with shrinkage, cross-validation for $lambda$ and with diversification constraint $||w||^2_2 \le \frac{5}{N}$ 
- **Shr. Heavy ML MVP w/ div. + cv lmd**, Heavy Tailed MVP with shrinkage, cross-validation for $lambda$ and with diversification constraint $||w||^2_2 \le \frac{5}{N}$ 

Additionally, an **Equal Weight Portfolio (EWP)** was included as a benchmark to the MVP variants. 

Finally, **transactional costs**, **turnover** and **weight drift** are incorporated during backtesting to better reflect real world trading and defy ideal backtesting conditions.

## Setup
Make sure to install all required packages for the library through pip before running any cell. 

## Usage
Navigate to backtest_MVP.ipynb and select the “Run All” option. 

## Results
Performance is evaluated relative to the classical MVP using a walk-forward backtesting framework with fixed estimation windows of 3 years and monthly rebalancing over the period 2009-2024. Evaluation metrics focus on out-of-sample behavior of the following models.

The plots below illustrate the cumulative returns and drawdowns.
![image alt](https://github.com/VAPopa7/improved-MVP/blob/75b38b12031ca1723cef297847eb2084de90f494/plots/cumrets.png)
![image alt](https://github.com/VAPopa7/improved-MVP/blob/75b38b12031ca1723cef297847eb2084de90f494/plots/drawdowns.png)

The table below contains the annualized returns, annualized volatility, annualized Sharpe ratio, maximum drawdown and average turnover.
| Strategy | Annualized Return | Annualized Volatility | Sharpe Ratio | Max Drawdown | Average Turnover |
| :--- | :---: | :---: | :---: | :---: | :---: |
| EWP | 0.157933 | 0.193822 | 0.814833 | -0.395514 | 0.010893 |
| Vanilla MVP | -0.002726 | 0.396686 | -0.006871 | -0.837959 | 0.147690 |
| Vanilla MVP w/ div. | 0.076726 | 0.189489 | 0.404908 | -0.353526 | 0.079953 |
| MVP w/ div. + cv lmd | 0.071377 | 0.162478 | 0.439304 | -0.335171 | 0.084195 |
| Shr. MVP w/ div. + cv lmd | 0.074352 | 0.153524 | 0.484305 | -0.337083 | 0.074296 |
| Shr. hML MVP w/ div. + cv lmd | 0.082421 | 0.147038 | 0.560541 | -0.348399 | 0.063884 |

The most significant improvement arises from the diversification constraint, which substantially reduces volatility and turnover while improving risk-adjusted returns. Cross-validating $\lambda$ further stabilizes performance across market regimes. Shrinkage and heavy-tailed estimators provide incremental gains, improving robustness and tail behavior. 

Unsurprisingly, the EWP outperforms all MVP variants in terms of raw performance, but exhibits higher drawdowns and volatility. Among optimized portfolios, the shrinkage heavy-tailed MVP with diversification and cross-validated $\lambda$ emerges as the most conservative and stable specification with the lowest turnover among MVPs. 

## Limitations
Due to data availability constraints of Yahoo Finance, historical S&P 500 constituents (2009-2024) without reliable price histories (e.g., bankrupt firms, index placeholders, and certain pre-merger tickers) are excluded. Therefore, the asset universe is restricted to those with complete return histories over the sample period in order to ensure accounting consistency, and avoid spurious portfolio returns arising from dynamic universe changes. While this induces survivorship bias, it provides a controlled environment to compare estimation robustness across the proposed portfolio construction methods.

## Afterword
The Markowitz portfolio, as goes for any portfolio optimization function, is NOT a forecasting model, and should be taken with a huge caveat. Portfolio optimization consumes forecasts, and should therefore be treated as the foundation for portfolio construction instead of financial advice. That includes all models proposed in this repository!

A special thanks for Daniel P. Palomar’s “Portfolio Optimization: Theory and Application” which has been useful all throughout the documentation and code of this project.
Make sure to check it out: https://portfoliooptimizationbook.com/book/ 
