library(lingtypology)
library(rjson)

wals_to_glottocode = vector()
features <- scan("data/feature_list.txt", what=" ")
for(feature in features) {
    print(paste("Download ", feature, "..."))
    x <- wals.feature(feature)
    for (row in 1:nrow(x)) {
        if (!is.element(x[row, "wals.code"], wals_to_glottocode)) {
            wals_to_glottocode[x[row, "wals.code"]] = x[row, "glottocode"]
        }
    }
    print("Done.")
}

file <- file("data/wals_to_glottocode.csv")
lines = c("walscode,glottocode")
for(name in names(wals_to_glottocode)) { 
    lines[length(lines) + 1] <- paste(name, wals_to_glottocode[name], sep=",")
} 
writeLines(lines, file) 
close(file)