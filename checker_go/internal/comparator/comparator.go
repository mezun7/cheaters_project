package comparator

func SourcesCompare(lhs, rhs []string) float64 {
	if len(lhs) > len(rhs) {
		lhs, rhs = rhs, lhs
	}

	dp := make([][]int, len(lhs)+1)
	dp[0] = make([]int, len(rhs)+1)
	for i := 0; i < len(lhs); i++ {
		dp[i+1] = make([]int, len(rhs)+1)
		for j := 0; j < len(rhs); j++ {
			if lhs[i] == rhs[j] {
				dp[i+1][j+1] = dp[i][j] + 1
			} else {
				dp[i+1][j+1] = dp[i+1][j]
				if dp[i+1][j+1] < dp[i][j+1] {
					dp[i+1][j+1] = dp[i][j+1]
				}
			}
		}
		dp[i] = nil
	}

	diff := len(lhs) + len(rhs) - 2*dp[len(lhs)][len(rhs)]
	eval := float64(diff) / float64(len(lhs)+len(rhs))

	return eval
}
