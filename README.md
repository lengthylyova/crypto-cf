<h1>Crypto Correlation Finder</h1>
<h3>This is a job test.</h3>

This is a program that analyzes the <b>correlation of two crypto-symbols</b>. If the correlation coefficient is within the <i>normal range</i> of <b>-0.5 < C < 0.5</b>, the primary symbol will be checked for a change of 1 percent. If the check is successful, <b>"1% CHANGE"</b> will be printed to the console.

You can set the <i>primary</i> and <i>secondary keys</i>, the <i>period of checking for correlation</i> and the <i>frequency of requests to the Binance server</i> in the file "app/settings.py ".

The files "primary.txt" and "secondary.txt" store <b>temporary</b> data with the values of crypto-symbols for the <i>period</i> specified in "app/settings.py".