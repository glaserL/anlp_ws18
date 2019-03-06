library(ggplot2)
library(reshape2)
library(RSQLite)
library(grid)
library(gtable)
library(extrafont)
library(latex2exp)

# use latex fonts
# font_import()
# par(family = "LM Roman 10")

######################################################
# retrieve distribution plot directly from db
######################################################

# make queries
con <- dbConnect(RSQLite::SQLite(), "../db/database.db")
p1 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year NOT LIKE "2%" OR year IS "2000" GROUP BY genre;')
p2 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" GROUP BY genre;')
p3 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" GROUP BY genre;')
dbDisconnect(con)

# make queries
con <- dbConnect(RSQLite::SQLite(), "../../data/backup/database_new_unproc_dupRemove.db")
q1 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year NOT LIKE "2%" OR year IS "2000" GROUP BY genre;')
q2 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" GROUP BY genre;')
q3 = dbGetQuery(con,'SELECT genre, COUNT(*) FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" GROUP BY genre;')
dbDisconnect(con)

######################################################
# plot freq distributions for unpruned data
######################################################

# plot old database which was unpruned no duplicates

a <- q1[,2]
b <- q2[,2]
c <- q3[,2]
ls1 <- list("<=2000" = a,"2001-2010" = b,"2011-2019" = c)

# mapping to combine country/rock, as well as hiphop groups
ls1 <- sapply(ls1, function(x) return(c("Country" = x[1], "Hip-Hop" =  x[3], "Pop" = x[2]+x[4])))
ls1 <- melt(ls1)
colnames(ls1) <- c("genre", "year", "frequency")
levels(ls1$year) <- c(TeX("$\\mathbf{T_1}$ $\\[\\leq 2000\\]$"),
                      TeX("$\\mathbf{T_2}$ $\\[\\2001-2010\\]$"), 
                      TeX("$\\mathbf{T_3}$ $\\[\\2011-2019\\]$"))

# make png
png(filename = "../../data/img/freqDisOld.png", width = 800, height = 600)
p <- ggplot(ls1, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) +
  theme_bw() + theme(text = element_text(size=20)) + facet_grid(. ~ year, labeller = label_parsed) +
  guides(fill=FALSE) + ylab("Frequency\n") + xlab("") + ylim(0,31000)
q <- p +  scale_fill_brewer(palette = "Dark2")
dev.off()

######################################################
# plot freq distributions for pruned data
######################################################

# plot even pruned distributions
a <- p1[,2]
b <- p2[,2]
c <- p3[,2]
ls1 <- list("<=2000" = a,"2001-2010" = b,"2011-2019" = c)

# mapping to combine country/rock, as well as hiphop groups
ls1 <- sapply(ls1, function(x) return(c("Country" = x[1], "Hip-Hop" =  x[2], "Pop" = x[3])))
ls1 <- melt(ls1)
colnames(ls1) <- c("genre", "year", "frequency")
levels(ls1$year) <- c(TeX("$\\mathbf{T_1}$ $\\[\\leq 2000\\]$"),
                      TeX("$\\mathbf{T_2}$ $\\[\\2001-2010\\]$"), 
                      TeX("$\\mathbf{T_3}$ $\\[\\2011-2019\\]$"))

# make png
png(filename = "../../data/img/freqDis.png", width = 800, height = 600)
p <- ggplot(ls1, aes(genre, frequency, fill = genre)) + geom_col(colour = "black", size = 0.35) + 
  theme_bw() + theme(text = element_text(size=20), legend.position = "none") + facet_grid(. ~ year, labeller = label_parsed) + 
  guides(fill=FALSE) + ylab("Frequency\n") + xlab("") + ylim(0,31000)
q <- p +  scale_fill_brewer(palette="Dark2")
grid::grid.text(unit(0.5,"npc"),unit(.98,'npc'),label = 'label at top', rot = 0) 
print(q)
dev.off()
