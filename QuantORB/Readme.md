This project is for implementing an Opening Range Breakout (ORB) strategy as described in a specific research paper. The strategy involves selecting the top 20 US equities with the highest relative volume after the first 5 minutes of trading, based on comparing the volume with the last 14 days of trading volume. These selected stocks are then traded using a 5-minute ORB strategy.

The implementation is done using Python for the QuantConnect LEAN backtesting platform. QuantConnect provides an environment for algorithmic trading research and backtesting, allowing users to test trading strategies using historical market data. The algorithm is designed to simulate trading in a realistic market environment and evaluate its performance over a specified period.


How to use:

# Opening Range Breakout (ORB) Strategy Implementation

## Overview

This project implements an Opening Range Breakout (ORB) strategy described in a research paper using Python for QuantConnect LEAN backtesting platform.

## Setup

1. **Clone Repository**: Download or clone the repository to your computer.

2. **Install Dependencies**: Ensure you have QuantConnect and required dependencies installed.

3. **Open Script**: Open the provided Python script in a text editor or IDE.

4. **Adjust Settings**: Customize the start and end dates, universe selection criteria, etc., as needed.

5. **Run Script**: Execute the script using QuantConnect or Python environment.

## Usage

1. **Customize Parameters**: Modify algorithm parameters based on your preferences.

2. **Run Algorithm**: Execute the algorithm to backtest the ORB strategy.

3. **Analyze Results**: Review backtest results to evaluate strategy performance.

4. **Refine Strategy**: Adjust parameters and refine strategy based on analysis.

## Notes

- Ensure you have necessary data subscriptions for Interactive Brokers data.
- Test the algorithm thoroughly before deploying in live trading.
- Consider consulting a financial advisor before making investment decisions.
