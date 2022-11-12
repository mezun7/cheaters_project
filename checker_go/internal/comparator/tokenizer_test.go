package comparator

import (
	"fmt"
	"testing"
)

func TestTokenize(t *testing.T) {
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
	fmt.Printf("Tokens LHS: %v\n", tokensL)
	fmt.Printf("Tokens RHS: %v\n", tokensR)
}
