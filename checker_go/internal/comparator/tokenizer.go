package comparator

import (
	"strings"
	"text/scanner"
)

func Tokenize(rawCode, fileName string) []string {
	tokens := make([]string, 0)

	fileName = strings.ToLower(fileName)
	ext := ""
	if extBegin := strings.LastIndex(fileName, "."); extBegin != -1 {
		ext = fileName[extBegin+1:]
	}

	var s scanner.Scanner
	s.Init(strings.NewReader(rawCode))

	//s.Mode ^= scanner.ScanComments

	if strings.Contains(".py", ext) {
		s.Whitespace ^= 1<<'\t' | 1<<'\n' // don't skip tabs and new lines
	}

	for tok := s.Scan(); tok != scanner.EOF; tok = s.Scan() {
		if tok != scanner.Comment {
			tokens = append(tokens, s.TokenText())
		}
	}

	switch {
	case strings.Contains(".cpp|.c", ext):
		tokens = removeTokens(tokens, []string{"#", "include"}, ">")
	case strings.Contains(".java", ext):
		tokens = removeTokens(tokens, []string{"import"}, ";")
		tokens = removeBadWords(tokens, map[string]int{"public": 1, "private": 1, "@Override": 1, "final": 1, "static": 1, "throws": 1, "{": 1, "}": 1})
	case strings.Contains(".py", ext):
		tokens = removeTokens(tokens, []string{"#"}, "\n")
		tokens = removeTokens(tokens, []string{"\"\"\""}, "\"\"\"")
		tokens = removeTokens(tokens, []string{"from"}, "\n")
		tokens = removeTokens(tokens, []string{"import"}, "\n")
	}

	return tokens
}

func removeBadWords(tokens []string, badWords map[string]int) []string {
	writeIdx := 0
	for i := 0; i < len(tokens); i++ {
		if _, ok := badWords[tokens[i]]; !ok {
			tokens[writeIdx] = tokens[i]
			writeIdx++
		}
	}

	return tokens[:writeIdx]
}

func removeTokens(tokens, prefix []string, suffix string) []string {
	writeIdx := 0
	for i := 0; i < len(tokens); i++ {
		samePrefix := true
		for j := 0; j < len(prefix) && samePrefix; j++ {
			if i+j >= len(tokens) || tokens[i+j] != prefix[j] {
				samePrefix = false
			}
		}
		if samePrefix {
			j := i + len(prefix)
			for j < len(tokens) && j-i < 10 && tokens[j] != suffix {
				j++
			}
			if j < len(tokens) && tokens[j] == suffix {
				i = j
				continue
			}
		}

		tokens[writeIdx] = tokens[i]
		writeIdx++
	}

	return tokens[:writeIdx]
}
