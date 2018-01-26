## look at test.tsv: due to a value 'Not available', the second column is interpreted as factor
test <- read.table("test.tsv", sep="\t", header=TRUE)
test$Value

## Noe that if header=TRUE is not given, the second column will also be coerced as factor

## possibility 1: force conversion: empty and non-numeric values are coereced into NA
as.numeric(as.character(test$Value))
## question: why as.numeric(as.character(test$Value))? What happens if one uses as.numeric(test$Value)?

## possibility 2: check which values in the file do not look like numbers
looksLikeNum <- function(str) grepl("^[-]?[0-9\\.]*$", str)
test$Value[!looksLikeNum(test$Value)]

## possibility 3: use the readr package, parsing error will be printed but the code won't break
library(readr)
read_tsv("test.tsv", col_types = list(col_integer(), col_number()))

## possibility 4: force numeric type during read in - the code will break if the specified class is not correct 
read.table("test.tsv", sep="\t", header=TRUE, colClasses=c("integer", "numeric"))



