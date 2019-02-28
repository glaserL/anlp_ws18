library(ggplot2)
library(reshape2)
library(RSQLite)

######################################################
# old freq distribution plot directly from db
######################################################

# make queries
con <- dbConnect(RSQLite::SQLite(), "../db/database.db")
p1 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year NOT LIKE "2%" OR year IS "2000" GROUP BY genre;')
p2 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" GROUP BY genre;')
p3 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" GROUP BY genre;')
dbDisconnect(con)

# plot even pruned distributions
a <- p1[,2]
b <- p2[,2]
c <- p3[,2]
ls1 <- list("<=2000" = a,"2001-2010" = b,"2011-2019" = c)

# mapping to combine country/rock, as well as hiphop groups
ls1 <- sapply(ls1, function(x) return(c("country" = x[1], "hip" =  x[2], "pop" = x[3])))
ls1 <- melt(ls1)
colnames(ls1) <- c("genre", "year", "frequency")

# make png
png(filename = "../../data/img/freqDis.png", width = 800, height = 600)
p <- ggplot(ls1, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) + 
  theme(text = element_text(size=20)) + facet_grid(cols = vars(year))
q <- p +  scale_fill_brewer(palette="Dark2")
print(q)
dev.off()