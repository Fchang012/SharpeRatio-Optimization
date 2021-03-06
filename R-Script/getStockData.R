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
           'TRSGX',
           'PRISX',
           'SPY')

# Get stock info
for (i in 1:length(ticker)){
  tickerList[[i]] <- getSymbols(ticker[i], from = as.Date("2005-01-01"), auto.assign = FALSE, src='google')
}

# Write them to CSV files
for (j in 1:length(tickerList)){
  #Rename Col
  colnames(tickerList[[j]])[1] <- "Open"
  colnames(tickerList[[j]])[2] <- "High"
  colnames(tickerList[[j]])[3] <- "Low"
  colnames(tickerList[[j]])[4] <- "Close"
  colnames(tickerList[[j]])[5] <- "Volume"
  colnames(tickerList[[j]])[6] <- "Adj Close"
  
  #Change to DF
  tempDF <- data.frame(Date=index(tickerList[[j]]), coredata(tickerList[[j]]))
  # row.names(tempDF) <- tempDF$Dates
  # tempDF$Dates <- NULL
  
  #Write
  toCSV(tempDF, ticker[j])
}