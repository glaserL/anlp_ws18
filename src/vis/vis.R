# country, dance_pop, hiphop_group, hiphop_musician, rock
# combine to rock, pop, hiphop
# 1990s and before, 2000s, 2010s

library(ggplot2)
library(reshape2)
library(RSQLite)

# base

a <- c(182,1191,0,1774,1011)
b <- c(378, 2471, 146, 14311, 1179)
c <- c(673, 9207, 176, 34744, 1392)
d <- c(1486, 20306, 130, 112123, 1893)
ls <- list("<=1999" = a+b,"2000-2009" = c,"2010-2019" = d)

# mapping to combine country/rock, as well as hiphop groups
ls <- sapply(ls, function(x) return(c("rock" = x[1]+x[5],"pop" =  x[2], "hip" = x[3]+x[4])))
ls <- melt(ls)
colnames(ls) <- c("genre", "year", "frequency")

png(filename = "../../data/img/freqTest.png", width = 800, height = 600)
p <- ggplot(ls, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) + 
  theme(text = element_text(size=20)) + ylim(0,120000) + facet_grid(cols = vars(year))
q <- p +  scale_fill_brewer(palette="Dark2")
print(q)
dev.off()

# start new

con <- dbConnect(RSQLite::SQLite(), "../db/database.db")

p1 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year NOT LIKE "2%" OR year IS "2000" GROUP BY genre;')
p2 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" GROUP BY genre;')
p3 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" GROUP BY genre;')
q1 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year LIKE "200%" OR year LIKE "199%" OR year IS "2010" GROUP BY genre;')
q2 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" GROUP BY genre;')

dbDisconnect(con)

# plot 1

a <- p1[,2]
b <- p2[,2]
c <- p3[,2]
ls1 <- list("<=2000" = a,"2001-2010" = b,"2011-2019" = c)

# mapping to combine country/rock, as well as hiphop groups
ls1 <- sapply(ls1, function(x) return(c("country" = x[1],"pop" =  x[2], "hip" = x[3]+x[4], "rock" = x[5])))
ls1 <- melt(ls1)
colnames(ls1) <- c("genre", "year", "frequency")

png(filename = "../../data/img/freqTest2.png", width = 800, height = 600)
p <- ggplot(ls1, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) + 
  theme(text = element_text(size=20)) + ylim(0,120000) + facet_grid(cols = vars(year))
q <- p +  scale_fill_brewer(palette="Dark2")
print(q)
dev.off()

# plot 2
  
a <- q1[,2]
b <- q2[,2]
ls2 <- list("<=2010" = a,"2011-2019" = b)

# mapping to combine country/rock, as well as hiphop groups
ls2 <- sapply(ls2, function(x) return(c("country" = x[1],"pop" =  x[2], "hip" = x[3]+x[4], "rock" = x[5])))
ls2 <- melt(ls2)
colnames(ls2) <- c("genre", "year", "frequency")

png(filename = "../../data/img/freqTest3.png", width = 800, height = 600)
p <- ggplot(ls, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) + 
  theme(text = element_text(size=20)) + ylim(0,120000) + facet_grid(cols = vars(year))
q <- p +  scale_fill_brewer(palette="Dark2")
print(q)
dev.off()

# plot 3

ls <- sapply(unique(as.character(ls1[,1])), function(x) min(ls1[which(ls1[,1]==x),3])*3)
ls <- rbind(ls, sapply(unique(as.character(ls2[,1])), function(x) min(ls2[which(ls2[,1]==x),3])*2))
rownames(ls) <- c("3_step", "2_step")

# mapping to combine country/rock, as well as hiphop groups
ls <- melt(ls)
colnames(ls) <- c("type", "genre", "frequency")

png(filename = "../../data/img/freqTest4.png", width = 800, height = 600)
p <- ggplot(ls, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) + 
  theme(text = element_text(size=20)) + ylim(0,120000) + facet_grid(cols = vars(type))
q <- p +  scale_fill_brewer(palette="Dark2")
print(q)
dev.off()