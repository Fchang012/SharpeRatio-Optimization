library(quantmod)

setwd("E:\\Shared_Files\\Fchang012\\SharpeRatio-Optimization\\R-Script")

# toCSV Function
toCSV <- function(sym, ticker){
  fileURL = paste(getwd(),"/CSV/",ticker, ".csv", sep="")
  write.zoo(sym, file=fileURL, sep=",")
}

# Stocks
tickerList <- list()

ticker = c('VGSTX',
           'PRGTX',
           'PRGFX',
           'PRMTX',
           'PRGTX',
           'TRSGX')

# Get stock info
for (i in 1:length(ticker)){
  tickerList[[i]] <- getSymbols(ticker[i], from = as.Date("2010-01-01"), auto.assign = FALSE)
}

# Write them to CSV files
for (j in 1:length(tickerList)){
  toCSV(tickerList[[j]], ticker[j])
}