package main

import (
    "fmt"
    "strings"
    "text/scanner"
)

/*
type Source struct {
    file string
    relativePath string
    userId string
    problemId string
    runId string
    attempt int
    score int
    tokens []string
    compare bool
}
*/

func SourcesCompare(lhs, rhs []string) float64 {
    if len(lhs) > len(rhs) {
        lhs, rhs = rhs, lhs
    }

    dp := make([][]int, len(lhs) + 1)
    dp[0] = make([]int, len(rhs) + 1)
    for i := 0; i < len(lhs); i++ {
        dp[i + 1] = make([]int, len(rhs) + 1)
        for j := 0; j < len(rhs); j++ {
            if lhs[i] == rhs[j] {
                dp[i + 1][j + 1] = dp[i][j] + 1
            } else {
                dp[i + 1][j + 1] = dp[i + 1][j]
                if dp[i + 1][j + 1] < dp[i][j + 1] {
                    dp[i + 1][j + 1] = dp[i][j + 1]
                }
            }
        }
        dp[i] = nil
    }

    diff := len(lhs) + len(rhs) - 2 * dp[len(lhs)][len(rhs)]
    eval := float64(diff) / float64(len(lhs) + len(rhs))

    return eval
}

func Tokenize(rawCode, fileName string) []string {
    tokens := make([]string, 0)

    fileName = strings.ToLower(fileName)
    ext := ""
    if extBegin := strings.LastIndex(fileName, "."); extBegin != -1 {
        ext = fileName[extBegin + 1:]
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
            if i + j >= len(tokens) || tokens[i + j] != prefix[j] {
                samePrefix = false
            }
        }
        if samePrefix {
            j := i + len(prefix)
            for j < len(tokens) && j - i < 10 && tokens[j] != suffix {
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

func main() {
    srcL := `#include <bits/stdc++.h>
 
using namespace std;
 
int n,k;
vector<int> a;
//YES - если можно расположить грузы требуемым способом;
// NO- еслли нельзя;
 
void rec(int left,int right=0,int i=0){
    if(i==n){
        if(left==right){
            cout<<"YES"<<endl;
            exit(0);
        }
    }else {
        rec(left + a[i], right, i + 1);
        rec(left, right + a[i], i + 1);
        rec(left, right, i + 1);
    }
}
 
int main() {
 
    cin>>k;
    cin>>n;
    a.resize(n);
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    rec(k);
    cout<<"NO"<<endl;
    return 0;
}`
    srcR := `#include <iostream>
#include <cmath>
#include <vector>
#include <bits/stdc++.h>
 
using namespace std;
 
int n,k;
vector <int> a;
 
 
void rec(int left,int right=0, int i=0){
    if(i==n){
        if (left==right){
            cout<<"YES"<<endl;
            exit(0);
        }
    }else{
        rec(left+a[i],right,i+1);
        rec(left,right+a[i],i+1);
        rec(left,right,i+1);}
}
int main(){
    cin>>k;
    cin>>n;
    a.resize(n);
    for (int i=0; i<n; i++){
        cin>>a[i];
    }
    rec(k);
    cout<<"NO"<<endl;
}`

    tokensL := Tokenize(srcL, "main.cpp")
    tokensR := Tokenize(srcR, "pages.cpp")
    fmt.Println("Tokens LHS:\n", tokensL)
    fmt.Println("Tokens RHS:\n", tokensR)
    fmt.Println("Diff\n", SourcesCompare(tokensL, tokensR))
}
