#include <iostream>
#include <vector>
using namespace std;

int n;

// Check whether placing a queen is safe
bool isSafe(vector<vector<int>>& board, int row, int col){
    // Check upper column
    for (int i = 0; i < row; i++){
        if (board[i][col] == 1)
            return false;
    }

    // Check upper left diagonal
    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--){
        if (board[i][j] == 1)
            return false;
    }

    // Check upper right diagonal
    for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++){
        if (board[i][j] == 1)
            return false;
    }

    return true;
}

// Solve N-Queens using backtracking
bool solveNQueens(vector<vector<int>>& board, int row){
    // All queens are placed
    if (row == n)
        return true;

    for (int col = 0; col < n; col++){
        if (isSafe(board, row, col)){
            // Place queen
            board[row][col] = 1;

            if (solveNQueens(board, row + 1))
                return true;

            // Backtrack
            board[row][col] = 0;
        }
    }
    return false;
}

int main(){
    cout << "Enter the value of N: ";
    cin >> n;

    vector<vector<int>> board(n, vector<int>(n, 0));

    // Place first queen at position (0, 0)
    board[0][0] = 1;

    if (solveNQueens(board, 1)){
        cout << "\nN-Queens Solution:\n";
        for (int i = 0; i < n; i++){
            for (int j = 0; j < n; j++){
                cout << board[i][j] << " ";
            }
            cout << endl;
        }
    }
    else{
        cout << "No solution exists with first queen at (0, 0).";
    }
}
